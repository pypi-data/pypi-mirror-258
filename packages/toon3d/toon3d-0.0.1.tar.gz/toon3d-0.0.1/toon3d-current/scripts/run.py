"""
Main script.
"""

from pathlib import Path
import json
from datetime import datetime
import io

import mediapy
import numpy as np
import plotly.graph_objects as go
import torch
import torch.nn as nn
from tqdm import tqdm
import shutil
import cv2

import tyro
import viser
from toon3d.utils.draw_utils import get_images_with_keypoints
from toon3d.utils.camera_utils import Cameras
from toon3d.warp.warp_mesh import WarpMesh, draw_tris, draw_points, create_triangulations
from toon3d.warp.warp_losses import constant_triangulation_loss
from toon3d.warp.arap_utils import face_verts_arap_loss
from toon3d.warp.tri_rasterize import rasterize_texture

from nerfstudio.utils.rich_utils import CONSOLE

def optimize_mesh(
    mesh,
    iters=400,
    split_iters=200,
    tri_loss_mult=1,
    tri_reg_mult=1,
    lr=0.5,
    num_fixed_points=None,
    split_faces=True,
    flip_edges=True,
    show_triangulation=True,
):
    if not num_fixed_points:
        num_fixed_points = mesh.num_fixed_points
    optim = torch.optim.Adam([mesh.points], lr=lr)

    image_np = mesh.image[0].detach().cpu().numpy()

    frames = []
    error_frames = []
    wire_frames = []

    pbar = tqdm(range(iters))
    for p in pbar:
        optim.zero_grad()

        # photometric loss
        if show_triangulation:
            tri_loss, to_split, tri_image = constant_triangulation_loss(mesh, return_image=True)

            tri_image = tri_image.cpu().detach().numpy()
            ref_image = mesh.image[0].cpu().detach().numpy()

            frames.append(draw_tris(mesh, image=tri_image))
            error_frames.append((tri_image - ref_image) ** 2)
            wire_frames.append(draw_tris(mesh, image=image_np))
        else:
            tri_loss, to_split = constant_triangulation_loss(mesh, return_image=False)

        # regularization
        tri_reg = mesh.laplacian_smoothing_loss()

        loss = tri_loss_mult * tri_loss + tri_reg_mult * tri_reg
        loss.backward()

        # mask grad for corners
        # print(mesh.points.grad)
        mesh.points.grad[:52] = 0
        optim.step()

        with torch.no_grad():
            if p < split_iters and split_faces and len(to_split) > 0:
                mesh.split_face(to_split[0])
                optim.param_groups[0]["params"][0] = mesh.points

            mesh.points[mesh.points < 0] = 0
            mesh.points[:, 0][mesh.points[:, 0] > mesh.width - 1] = mesh.width - 1
            mesh.points[:, 1][mesh.points[:, 1] > mesh.height - 1] = mesh.height - 1

            if flip_edges:
                while (to_flip := mesh.find_edge_flips()) and to_flip > -1:
                    mesh.flip_edge(to_flip)

        pbar.set_description(f"loss: {loss:.2e}, tri_loss: {tri_loss:.2e}, tri_reg: {tri_reg:.2e}", refresh=True)

    if show_triangulation:
        return frames, error_frames, wire_frames


def make_transforms_json(fxs, fys, Rs, ts, widths, heights):
    fxs, fys, Rs, ts = fxs.detach().cpu(), fys.detach().cpu(), Rs.detach().cpu(), ts.detach().cpu()
    transforms = {
        "camera_model": "OPENCV",
        "ply_file_path": "plys/all.ply",
        "points": "points/points.pt",
        "points_mask": "points/points_mask.pt",
        "meshes_points": "meshes/meshes_points.pt",
        "warped_meshes_points": "meshes/warped_meshes_points.pt",
        "simplices": "meshes/simplices.pt",
    }

    frames = []
    for i, (R, t) in enumerate(zip(Rs, ts)):
        flip = torch.tensor([[1, 0, 0], [0, -1, 0], [0, 0, -1]]).float()
        R = R @ flip
        transform_matrix = torch.cat([torch.cat([R, t[...,None]], 1), torch.tensor([[0, 0, 0, 1]])], 0)
        width = widths[i].item()
        height = heights[i].item()
        fx = fxs[i] / 2 * widths[i]
        fy = fys[i] / 2 * heights[i]
        frame = {
            "file_path": f"images/{i:05d}.png",
            "fl_x": fx.item(),
            "fl_y": fy.item(),
            "cx": width // 2,
            "cy": height // 2,
            "w": int(width),
            "h": int(height),
            "transform_matrix": transform_matrix.tolist(),
            "depth_file_path": f"depths/{i:05d}.npy",
            "mask_path": f"masks/{i:05d}.png",
        }
        frames.append(frame)
    transforms["frames"] = frames

    return transforms

def make_dense_points_3d(cameras, depths, factor=4):
    dense_points_3d = []

    for ndx, depth_map in enumerate(depths): 
        height, width = depth_map.shape
        xs = torch.arange(width)
        ys = torch.arange(height)
        grid_x, grid_y = torch.meshgrid(xs, ys, indexing="ij")

        grid_x = (grid_x / (width - 1) * 2) - 1
        grid_y = (grid_y / (height - 1) * 2) - 1

        x = grid_x[::factor, ::factor].flatten()
        y = grid_y[::factor, ::factor].flatten()
        z = depth_map[::factor, ::factor].T.flatten()

        dense_points_3d.append(cameras(x, y, z)[ndx])

    return dense_points_3d


def make_plys(images_colors, points_3d):
    n = len(images_colors)
    plys = []
    for i in range(n):
        image_colors = images_colors[i]
        ply_points = points_3d[i]

        ply = io.StringIO()
        ply.write("ply\n")
        ply.write("format ascii 1.0\n")
        ply.write(f"element vertex {len(ply_points)}\n")
        ply.write("property float x\n")
        ply.write("property float y\n")
        ply.write("property float z\n")
        ply.write("property uint8 red\n")
        ply.write("property uint8 green\n")
        ply.write("property uint8 blue\n")
        ply.write("end_header\n")

        for point, color in zip(ply_points, image_colors):
            x, y, z = point.to(torch.float)
            r, g, b = (color * 255).to(torch.uint8)
            ply.write(f"{x:8f} {y:8f} {z:8f} {r} {g} {b}\n")

        plys.append(ply.getvalue())
        ply.close()

    return plys

def load_dataset(data_prefix, dataset):
    images_path = data_prefix / f"{dataset}/images"
    metadata_path = data_prefix / f"{dataset}/metadata.json"
    points_path = data_prefix / f"{dataset}/points.json"
    depths_path = data_prefix / f"{dataset}/depths"

    metadata_json = json.loads(metadata_path.read_text())

    points_json = json.loads(points_path.read_text())
    valid_images = points_json["validImages"]
    points_list = [[[p["x"], p["y"]] for p in points] for points in points_json["points"]]
    valid_points_list = points_json["validPoints"]
    valid_polygons = points_json["polygons"]
    image_filenames = sorted(list(images_path.glob("*.png")))

    # only keep the valid indices, based on valid_images
    metadata_json["frames"] = [
        metadata_json["frames"][i] for i in range(len(metadata_json["frames"])) if valid_images[i]
    ]
    points_list = [points_list[i] for i in range(len(points_list)) if valid_images[i]]
    valid_points_list = [valid_points_list[i] for i in range(len(valid_points_list)) if valid_images[i]]
    valid_polygons = [valid_polygons[i] for i in range(len(valid_polygons)) if valid_images[i]]
    image_filenames = [image_filenames[i] for i in range(len(image_filenames)) if valid_images[i]]

    images = [torch.from_numpy(mediapy.read_image(imf)[:, :, :3] / 255.0).float() for imf in image_filenames]
    n = len(images)
    heights = torch.tensor([image.shape[0] for image in images])
    widths = torch.tensor([image.shape[1] for image in images])

    m = max([len(p) for p in points_list])

    points = torch.full([n, m, 2], -1)
    for i in range(n):
        for j in range(len(points_list[i])):
            points[i, j, 0] = points_list[i][j][0]
            points[i, j, 1] = points_list[i][j][1]

    # points_mask padded with False
    points_mask = torch.zeros_like(points[:, :, 0]) == 1
    for i in range(n):
        for j in range(len(points_list[i])):
            points_mask[i, j] = valid_points_list[i][j]

    depths = []
    for i in range(len(valid_images)):
        depths.append(torch.load(depths_path / f"{i:05d}.pt").squeeze())
    # only keep the valid indices, based on valid_images
    depths = [depths[i] for i in range(len(depths)) if valid_images[i]]
    max_depth = max([torch.max(depth) for depth in depths])
    depths = [depth / max_depth for depth in depths]

    masks = []
    for i in range(n):
        mask_image = np.ones((heights[i], widths[i]), dtype=np.uint8) * 255
        for j in range(len(metadata_json["frames"][i]["masks"])):
            mask = metadata_json["frames"][i]["masks"][j]
            for k in range(len(mask["polygons"])):
                contour = np.array(mask["polygons"][k]).reshape(-1, 2).astype(np.int32)
                if valid_polygons[i][j][k]:
                    cv2.fillPoly(mask_image, [contour], 0)
        masks.append(mask_image)

    shapes = torch.cat([widths[:, None], heights[:, None]], -1).unsqueeze(1).repeat(1, m, 1)
    points_normed = (points / shapes) * 2 - 1

    return images, heights, widths, points, points_normed, points_mask, depths, masks


def view_pcs_cameras(server,
                     images, # images
                     cameras,
                     dense_points_3d, # dense pc
                     images_colors, 
                     sparse_points_3d, # sparse pc
                     point_colors, 
                     mesh_verts_list, # mesh
                     simplices_list,
                     mesh_colors,
                     prefix="data"):

    heights = torch.tensor([image.shape[0] for image in images])

    # from our coords to viser coords X, Y, Z -> -Z, X, -Y
    flip = torch.tensor([[0, 0, -1], [1, 0, 0], [0, -1, 0]]).float()
    for ndx in range(len(images)):
        server.add_mesh_simple(
            f"{prefix}/mesh/img-{ndx}/fill",
            vertices=5 * (flip @ mesh_verts_list[ndx].T).T.cpu().detach().numpy(),
            faces=simplices_list[ndx].cpu().detach().numpy(),
            color=mesh_colors[ndx],
            wxyz=viser.transforms.SO3.from_x_radians(0).wxyz,
            opacity=0.4,
            flat_shading=True,
            side='double',
            visible=False,
        )

        #wireframe
        server.add_mesh_simple(
            f"{prefix}/mesh/img-{ndx}/wireframe",
            vertices=5 * (flip @ mesh_verts_list[ndx].T).T.cpu().detach().numpy(),
            faces=simplices_list[ndx].cpu().detach().numpy(),
            wireframe=True,
            color=(0, 0, 0),
            wxyz=viser.transforms.SO3.from_x_radians(0).wxyz,
            visible=False,
        )

        server.add_point_cloud(
            f"{prefix}/dense-pc/img-{ndx}",
            colors=images_colors[ndx].detach().numpy(),
            points=5 * (flip @ dense_points_3d[ndx].T).T.cpu().detach().numpy(),
            point_size=0.05,
        )

        server.add_point_cloud(
            f"{prefix}/sparse-pc/img-{ndx}",
            colors=point_colors[ndx].detach().numpy(),
            points=5 * (flip @ sparse_points_3d[ndx].T).T.detach().numpy(),
            point_size=0.1,
        )

        server.add_camera_frustum(
            f"{prefix}/cameras/img-{ndx}",
            fov=np.arctan2(heights[ndx] / 2, cameras.fxs[ndx].item()),
            aspect=cameras.fys[ndx].item() / cameras.fxs[ndx].item(),
            scale=0.1,
            wxyz=viser.transforms.SO3.from_matrix(flip @ cameras.Rs[ndx].detach().numpy()).wxyz,
            position=5 * ((flip @ cameras.ts[ndx].flatten().detach().numpy())),
            image=images[ndx].numpy(),
        )


def main(
    data_prefix: Path = Path("data/processed"),
    dataset: str = "rick-house",
    device: str = "cpu",
    niters: int = 5000,
    lr: float = 0.01,
    affine_loss_mult: float = 1.0,
    scale_loss_mult: float = 1e3,
    offset_loss_mult: float = 1e3,
    quat_norm_mult: float = 1.0,
    focal_mag_mult: float = 1e-3,
    focal_fix_mult: float = 1e-3,
    arap_mult: float = 1, 
    refine_depths_mult: float = 1e-3,
    refine_points_mult: float = 1e-2, 
    refine_pose_mult: float = 1,
    output_prefix: Path = Path("outputs"),
    nerfstudio_folder: Path = Path("data/nerfstudio"),
    ply_downscale_factor: int = 8,
    view_point_cloud: bool = True,
):
    """Script to run our SfM on cartoons."""

    output_folder = output_prefix / dataset / "run" / datetime.now().strftime("%Y-%m-%d_%H%M%S")
    output_folder.mkdir(parents=True)

    images, heights, widths, points, points_normed, points_mask, depths, masks = load_dataset(data_prefix, dataset)
    n, m = points.shape[:2]

    # draw keypoints on image
    point_colors = torch.rand((m, 3))
    colors = point_colors[None].repeat(n, 1, 1).to(device)
    colors[~points_mask] = torch.tensor([1, 1, 1]).to(device).float()
    output_images_dir = Path(output_folder / "images")
    output_images_dir.mkdir(parents=True)
    for i in range(n):
        keypoint_image = get_images_with_keypoints(
            images[i].permute(2, 0, 1)[None], points_normed[i][None], colors[i][None], keypoint_size=5
        )[0].permute(1, 2, 0)
        
        mediapy.write_image(output_images_dir / f"{i:02d}.png", keypoint_image)

    ########################################
    ###### coarse camera optimization ######
    ########################################
    CONSOLE.print("[bold green] Camera optimization")

    # make pairs for comparison in optimization
    pairs = []

    for i in range(n):
        for j in range(i + 1, n):
            pairs.append([i, j])

    pairs = torch.tensor(pairs).T
    pairs_mask = torch.logical_and(points_mask[pairs][0], points_mask[pairs][1])[...,None] * 1

    # extract manual correspodences for optimization
    us = points[..., 0].int()
    vs = points[..., 1].int()

    us_normed = us / (widths[..., None] - 1) * 2 - 1
    vs_normed = vs / (heights[..., None] - 1) * 2 - 1

    zs = torch.stack([depths[ndx][vs[ndx], us[ndx]] for ndx in range(n)])

    dzs = nn.Parameter(torch.zeros([n]).float()) # delta zs
    szs = nn.Parameter(torch.ones([n]).float()) # scale zs

    # make cameras and optimizer
    coarse_cameras = Cameras(n)
    optimizer = torch.optim.Adam(list(coarse_cameras.parameters()) + [szs, dzs], lr=lr)

    # optimization loop
    pbar = tqdm(range(niters))

    for i in pbar:

        new_zs = zs * szs[...,None] + dzs[...,None]
        points_3d = coarse_cameras(us_normed, vs_normed, new_zs)

        paired_points = points_3d[pairs]

        affine_loss = affine_loss_mult * torch.mean(((paired_points[0] - paired_points[1]) ** 2) * pairs_mask)

        scale_loss = scale_loss_mult * ((torch.mean(szs) - 1) ** 2)

        offset_loss = offset_loss_mult * torch.mean(torch.relu(-dzs) ** 2)

        quat_norm = quat_norm_mult * torch.mean((torch.sum(coarse_cameras.quats**2, 1) - 1) ** 2)

        focal_mag = focal_mag_mult * (torch.mean(coarse_cameras.fxs) + torch.mean(coarse_cameras.fys))

        focal_fix = focal_fix_mult * torch.mean((coarse_cameras.fys / coarse_cameras.fxs - widths / heights) ** 2)

        loss = affine_loss + scale_loss + offset_loss + quat_norm + focal_mag + focal_fix

        optimizer.zero_grad()
        loss.backward()
        optimizer.step()

        # keep first point cloud fixed
        with torch.no_grad():
            coarse_cameras.quats[0] = torch.tensor([1, 0, 0, 0])
            coarse_cameras.ts[0] = torch.zeros([3])

            pbar.set_description(f"Loss: {affine_loss:.2e}", refresh=True)

    # rescale depth maps

    # make new cameras

    refined_cameras = Cameras(n, 
                              coarse_cameras.fxs.detach().clone(), 
                              coarse_cameras.fys.detach().clone(), 
                              coarse_cameras.quats.detach().clone(), 
                              coarse_cameras.ts.detach().clone())

    ################################
    ###### make triangulation ######
    ################################
    CONSOLE.print("[bold green] Image triangulation")

    corr_points_list, boundary_points_list, inner_points_list, simplices_list = create_triangulations(points, points_mask, widths, heights)
    edges_list = [torch.unique(torch.stack((simplices[:, [0, 1]], simplices[:, [1, 2]], simplices[:, [2, 0]]), dim=0).flatten(0, 1).sort(1).values, dim=0).T for simplices in simplices_list]

    # number of corr, boundary, and inner points per mesh
    num_corrs_per_mesh = [len(cp) for cp in corr_points_list]
    num_boundary_pts_per_mesh = [len(bp) for bp in boundary_points_list]
    num_inner_pts_per_mesh = [len(ip) for ip in inner_points_list]

    # make original mesh points
    original_mesh_points_list = [torch.cat(omp_triple) for omp_triple in zip(corr_points_list, boundary_points_list, inner_points_list)]
    original_mesh_points_packed = torch.cat(original_mesh_points_list)
    num_points_per_mesh = torch.tensor([len(omp) for omp in original_mesh_points_list])

    # make simplices
    simplices_shifts = torch.cat([torch.tensor([0]), num_points_per_mesh.cumsum(0)[:-1]])
    simplices_shifted_list = [simplices + shift for simplices, shift in zip(simplices_list, simplices_shifts)]
    simplices_shifted_packed = torch.cat(simplices_shifted_list)

    # original face verts
    original_face_verts_packed = original_mesh_points_packed[simplices_shifted_packed].mT

    # make warped points
    warped_boundary_points_list = [nn.Parameter(bp.detach().clone()) for bp in boundary_points_list]
    warped_inner_points_list = [nn.Parameter(ip.detach().clone()) for ip in inner_points_list]
    
    mesh_us_list = []
    mesh_vs_list = []
    mesh_zs_list = []
    zs_diff_list = []

    for ndx in range(n):
        original_mesh_points = original_mesh_points_list[ndx]

        mesh_us = original_mesh_points[...,0].int()
        mesh_vs = original_mesh_points[...,1].int()

        mesh_zs = depths[ndx][mesh_vs, mesh_us].detach()

        edges = edges_list[ndx]

        mesh_us_list.append(mesh_us)
        mesh_vs_list.append(mesh_vs)
        mesh_zs_list.append(mesh_zs)

        zs_diff_list.append(mesh_zs[edges[0]] - mesh_zs[edges[1]])

    ###################################
    ###### epipolar optimization ######
    ###################################
    CONSOLE.print("[bold green] Image Warping")

    # set up optimizer
    dus = nn.Parameter(torch.zeros_like(us).float())
    dvs = nn.Parameter(torch.zeros_like(vs).float())

    pzs = nn.Parameter(torch.zeros_like(zs)) # perturbation zs
    vert_pzs_list = [nn.Parameter(torch.zeros_like(mesh_zs[num_corrs:].detach())) for mesh_zs, num_corrs in zip(mesh_zs_list, num_corrs_per_mesh)]

    optimizer = torch.optim.Adam([pzs, dus, dvs] + [bp for bp in warped_boundary_points_list] + [ip for ip in warped_inner_points_list] + [vp for vp in vert_pzs_list], lr=lr)
    # optimizer = torch.optim.Adam(list(refined_cameras.parameters()) + [pzs, dus, dvs]  + [bp for bp in warped_boundary_points_list] + [ip for ip in warped_inner_points_list], lr=lr)
    
    # optimization loop
    pbar = tqdm(range(niters//2))

    # import pdb; pdb.set_trace()

    for i in pbar:

        # arap loss
        warped_us_packed = (us + dus)[points_mask]
        warped_vs_packed = (vs + dvs)[points_mask]

        warped_corr_points_packed = torch.stack([warped_us_packed, warped_vs_packed]).T.detach() # (sum(all_valid_corrs), 2)
        warped_corr_points_list = warped_corr_points_packed.split(num_corrs_per_mesh) # (n, tensor(valid_corrs, 2))

        warped_mesh_points_list = [torch.cat(wmp_triple) for wmp_triple in zip(warped_corr_points_list, warped_boundary_points_list, warped_inner_points_list)]
        warped_mesh_points_packed = torch.cat(warped_mesh_points_list)

        warped_face_verts_packed = warped_mesh_points_packed[simplices_shifted_packed].mT

        arap_loss = face_verts_arap_loss(original_face_verts_packed, warped_face_verts_packed)

        # 3D arap loss

        # import pdb; pdb.set_trace();
        zs_diff_loss = torch.tensor(0.0)
        for ndx in range(n):
            corr_pzs = pzs[ndx][points_mask[ndx]].detach() # stop gradient
            vert_pzs = vert_pzs_list[ndx]

            mesh_zs = mesh_zs_list[ndx]
            mesh_pzs = torch.cat([corr_pzs, vert_pzs])
            mesh_zs_pzs = (mesh_zs + mesh_pzs) * szs[ndx] + dzs[ndx]

            edges = edges_list[ndx]
            zs_diff = zs_diff_list[ndx] * szs[ndx]
            zs_pzs_diff = mesh_zs_pzs[edges[0]] - mesh_zs_pzs[edges[1]]

            zs_diff_loss += torch.mean((zs_diff - zs_pzs_diff) ** 2) / n

        # affine loss
        dus_normed = dus / (widths[..., None] - 1) * 2
        dvs_normed = dvs / (heights[..., None] - 1) * 2
        
        new_zs = (zs + pzs) * szs[...,None] + dzs[...,None]
        points_3d = refined_cameras(us_normed + dus_normed, vs_normed + dvs_normed, new_zs)

        paired_points = points_3d[pairs]

        affine_loss = torch.mean(((paired_points[0] - paired_points[1]) ** 2) * pairs_mask)

        # regularizations
        refine_depths_reg = refine_depths_mult * torch.mean(pzs ** 2)
        refine_points_reg = refine_points_mult * torch.mean(dus_normed ** 2 + dvs_normed ** 2)

        ts_reg = torch.mean((refined_cameras.ts - coarse_cameras.ts) ** 2)
        fxs_reg = torch.mean((refined_cameras.fxs - coarse_cameras.fxs) ** 2)
        fys_reg = torch.mean((refined_cameras.fys - coarse_cameras.fys) ** 2)

        refine_pose_reg = refine_pose_mult * (ts_reg + fxs_reg + fys_reg)
        
        loss = affine_loss + arap_mult * arap_loss + refine_depths_reg + refine_points_reg + refine_pose_reg + zs_diff_loss

        optimizer.zero_grad()
        loss.backward()
        optimizer.step()

        with torch.no_grad():
            refined_cameras.quats[0] = torch.tensor([1, 0, 0, 0])
            refined_cameras.ts[0] = torch.zeros([3])
            for ndx in range(n):
                # keep boundaries outside of frame
                
                    pts_at_zero = boundary_points_list[ndx] == 0
                    pts_at_width = boundary_points_list[ndx] == (widths[ndx] - 1)
                    pts_at_height = boundary_points_list[ndx] == (heights[ndx] - 1)

                    pt_gthan_zero = warped_boundary_points_list[ndx] > 0
                    pts_lthan_widths = warped_boundary_points_list[ndx] < widths[ndx] - 1
                    pts_lthan_height = warped_boundary_points_list[ndx] < heights[ndx] - 1

                    warped_boundary_points_list[ndx][torch.logical_and(pts_at_zero, pt_gthan_zero)] = 0
                    warped_boundary_points_list[ndx][torch.logical_and(pts_at_width, pts_lthan_widths)] = (widths[ndx] - 1)
                    warped_boundary_points_list[ndx][torch.logical_and(pts_at_height, pts_lthan_height)] = (heights[ndx] - 1)

        pbar.set_description(f"Loss: {affine_loss:.2e}, arap: {arap_loss:.2e}, zs_diff_loss: {zs_diff_loss:.2e}", refresh=True)

    ### create meshes for warping ###

    warped_us_packed = (us + dus)[points_mask]
    warped_vs_packed = (vs + dvs)[points_mask]

    warped_corr_points_packed = torch.stack([warped_us_packed, warped_vs_packed]).T.detach() # (sum(all_valid_corrs), 2)
    warped_corr_points_list = warped_corr_points_packed.split(num_corrs_per_mesh) # (n, tensor(valid_corrs, 2))

    warped_mesh_points_list = [torch.cat(wmp_triple) for wmp_triple in zip(warped_corr_points_list, warped_boundary_points_list, warped_inner_points_list)]
    
    all_meshes = []

    for ndx in range(n):
        uv_points = original_mesh_points_list[ndx]
        warped_mesh_points = warped_mesh_points_list[ndx]
        simplices = simplices_list[ndx]

        mesh = WarpMesh(warped_mesh_points, simplices, heights[ndx], widths[ndx], uv_points, device=device)

        all_meshes.append(mesh)

    # warp images and depths
    
    # rescale depths
    depths = [(depth_map * sz[...,None]) + dz[...,None] for depth_map, dz, sz in zip(depths, dzs, szs)]
        
    warped_images = []
    warped_depths = []
    warped_masks = []

    output_warped_images_dir = Path(output_folder / "warped_images")
    output_warped_depths_dir = Path(output_folder / "warped_depths")
    output_warped_masks_dir = Path(output_folder / "warped_masks")

    output_warped_images_dir.mkdir(parents=True)
    output_warped_depths_dir.mkdir(parents=True)
    output_warped_masks_dir.mkdir(parents=True)

    for ndx in range(len(all_meshes)):
        mesh = all_meshes[ndx]
        image = images[ndx]
        depth_map = depths[ndx]
        mask = torch.from_numpy(masks[ndx]).float()

        fragments = mesh.rasterize()
        warped_image = mesh.render(image, fragments)
        warped_depth = mesh.render(depth_map, fragments)
        warped_mask = mesh.render(mask, fragments)

        warped_image = warped_image.cpu().detach()
        warped_depth = warped_depth.cpu().detach()[...,0]
        warped_mask = warped_mask.cpu().detach()[...,0].to(torch.uint8).numpy()

        wire_img = draw_tris(mesh, image = warped_image.numpy())
        points_img = draw_points(mesh, image=wire_img, points=warped_corr_points_list[ndx], colors=point_colors[points_mask[ndx]].tolist())

        # save warps to outputs
        mediapy.write_image(output_warped_images_dir / f"{ndx:02d}.png", np.concatenate([warped_image.numpy(), points_img], axis=1))
        mediapy.write_image(output_warped_depths_dir / f"{ndx:02d}.png", warped_depth)
        mediapy.write_image(output_warped_masks_dir / f"{ndx:02d}.png", warped_mask)
    
        warped_images.append(warped_image)
        warped_depths.append(warped_depth)
        warped_masks.append(warped_mask)

    # import pdb; pdb.set_trace();


    #######################
    ###### make json ######
    #######################

    nerfstudio_dir = output_folder / "nerfstudio"
    nerfstudio_images_dir = nerfstudio_dir / "images"
    nerfstudio_depths_dir = nerfstudio_dir / "depths"
    nerfstudio_masks_dir = nerfstudio_dir / "masks"
    nerfstudio_points_dir = nerfstudio_dir / "points"
    nerfstudio_meshes_dir = nerfstudio_dir / "meshes"
    nerfstudio_plys_dir = nerfstudio_dir / "plys"

    nerfstudio_dir.mkdir(parents=True, exist_ok=True)
    nerfstudio_images_dir.mkdir(parents=True, exist_ok=True)
    nerfstudio_depths_dir.mkdir(parents=True, exist_ok=True)
    nerfstudio_masks_dir.mkdir(parents=True, exist_ok=True)
    nerfstudio_points_dir.mkdir(parents=True, exist_ok=True)
    nerfstudio_meshes_dir.mkdir(parents=True, exist_ok=True)
    nerfstudio_plys_dir.mkdir(parents=True, exist_ok=True)

    # store mesh points
    
    meshes_points_dict = {"corr_points": corr_points_list, 
                    "boundary_points":boundary_points_list, 
                    "inner_points": inner_points_list}

    warped_meshes_points_dict = {"corr_points": warped_corr_points_list, 
                            "boundary_points":warped_boundary_points_list, # grad still attached to boundary_points
                            "inner_points": warped_inner_points_list} # grad still attached to inner_points

    # json
    transforms = make_transforms_json(
        refined_cameras.fxs,
        refined_cameras.fys,
        refined_cameras.Rs,
        refined_cameras.ts,
        widths,
        heights,
    )
    with open(nerfstudio_dir / "transforms.json", "w", encoding="utf-8") as f:
        json.dump(transforms, f, indent=4)

    # images
    for i, img in enumerate(images):
        mediapy.write_image(nerfstudio_images_dir / f"{i:05}.png", img.cpu().numpy())

    # depths
    for i in range(n):
        np.save(nerfstudio_depths_dir / f"{i:05d}", depths[i][..., None].cpu().detach().numpy())

    # masks
    for i in range(n):
        mediapy.write_image(nerfstudio_masks_dir / f"{i:05}.png", masks[i])

    # points
    torch.save(points, output_folder / "nerfstudio" / "points/points.pt")
    torch.save(points_mask, output_folder / "nerfstudio" / "points/points_mask.pt")

    # mesh points
    torch.save(meshes_points_dict, output_folder / "nerfstudio" / "meshes/meshes_points.pt")
    torch.save(warped_meshes_points_dict, output_folder / "nerfstudio" / "meshes/warped_meshes_points.pt")
    torch.save(simplices_list, output_folder / "nerfstudio" / "meshes/simplices.pt")


    #######################
    ###### make plys ######
    #######################

    # coarse
    valid_points_3d = [mask[::ply_downscale_factor, ::ply_downscale_factor].T.flatten() != 0 for mask in masks]
    
    coarse_dense_points_3d = make_dense_points_3d(coarse_cameras, depths, ply_downscale_factor)
    coarse_dense_points_3d = [coarse_dense_points_3d[ndx][valid_points_3d[ndx]] for ndx in range(n)]
    
    images_colors = [image.permute(1, 0, 2)[::ply_downscale_factor, ::ply_downscale_factor].cpu().flatten(0, 1) for image in images]
    images_colors = [images_colors[ndx][valid_points_3d[ndx]] for ndx in range(n)]

    # refined
    warped_valid_points_3d = [mask[::ply_downscale_factor, ::ply_downscale_factor].T.flatten() != 0 for mask in warped_masks]

    warped_images_colors = [image.permute(1, 0, 2)[::ply_downscale_factor, ::ply_downscale_factor].cpu().flatten(0, 1) for image in warped_images]
    warped_images_colors = [warped_images_colors[ndx][warped_valid_points_3d[ndx]] for ndx in range(n)]
    
    warped_dense_points_3d = make_dense_points_3d(refined_cameras, warped_depths, ply_downscale_factor)
    warped_dense_points_3d = [warped_dense_points_3d[ndx][warped_valid_points_3d[ndx]] for ndx in range(n)] 


    plys = make_plys(warped_images_colors, warped_dense_points_3d)

    for i, ply in enumerate(plys):
        with open(output_folder / "nerfstudio" / "plys" / f"{i:05d}.ply", "w") as f:
            f.write(ply)

    # make a point cloud ply with all the plys combined ...
    with open(output_folder / "nerfstudio" / "plys" / "all.ply", "w") as f:
        f.write("ply\n")
        f.write("format ascii 1.0\n")
        f.write(f"element vertex {sum([len(ply.splitlines()) - 14 for ply in plys])}\n")
        f.write("property float x\n")
        f.write("property float y\n")
        f.write("property float z\n")
        f.write("property uint8 red\n")
        f.write("property uint8 green\n")
        f.write("property uint8 blue\n")
        f.write("end_header\n")

        for ply in plys:
            for line in ply.splitlines()[14:]:
                f.write(line + "\n")

    # remove folder if exists
    if (nerfstudio_folder / dataset).exists():
        shutil.rmtree(nerfstudio_folder / dataset)
    shutil.copytree(output_folder / "nerfstudio", nerfstudio_folder / dataset)

    if view_point_cloud:

        mesh_verts_list = []
        warped_mesh_verts_list = []

        coarse_sparse_points_3d = []
        refined_sparse_points_3d = []

        for ndx in range(n):
            original_mesh_points = original_mesh_points_list[ndx]
            warped_mesh_points = warped_mesh_points_list[ndx]
            simplices = simplices_list[ndx]

            mesh_us = original_mesh_points[...,0].int()
            mesh_vs = original_mesh_points[...,1].int()

            mesh_us_normed = mesh_us / (widths[ndx] - 1) * 2 - 1
            mesh_vs_normed = mesh_vs / (heights[ndx] - 1) * 2 - 1

            mesh_zs = mesh_zs_list[ndx] * szs[ndx] + dzs[ndx]

            warped_mesh_us = warped_mesh_points[..., 0].int().clamp(0, widths[ndx] - 1)
            warped_mesh_vs = warped_mesh_points[..., 1].int().clamp(0, heights[ndx] - 1)

            warped_mesh_us_normed = warped_mesh_us / (widths[ndx] - 1) * 2 - 1
            warped_mesh_vs_normed = warped_mesh_vs / (heights[ndx] - 1) * 2 - 1

            corr_pzs = pzs[ndx][points_mask[ndx]].detach() # stop gradient
            vert_pzs = vert_pzs_list[ndx]

            mesh_pzs = torch.cat([corr_pzs, vert_pzs])
            warped_mesh_zs = mesh_zs + (mesh_pzs * szs[ndx])

            mesh_verts = coarse_cameras(mesh_us_normed[None], mesh_vs_normed[None], mesh_zs[None])[ndx]
            mesh_verts_list.append(mesh_verts)
            coarse_sparse_points_3d.append(mesh_verts[:num_corrs_per_mesh[ndx]])

            warped_mesh_verts = coarse_cameras(warped_mesh_us_normed[None], warped_mesh_vs_normed[None], warped_mesh_zs[None])[ndx]
            warped_mesh_verts_list.append(warped_mesh_verts)
            refined_sparse_points_3d.append(warped_mesh_verts[:num_corrs_per_mesh[ndx]])

        sparse_point_colors = [point_colors[points_mask[ndx]] for ndx in range(n)]
        mesh_colors = [np.random.rand(3) for _ in range(n)]
        
        server = viser.ViserServer()

        view_pcs_cameras(server, 
                         images, # cameras
                         coarse_cameras,
                         coarse_dense_points_3d, # dense pc
                         images_colors, 
                         coarse_sparse_points_3d, # sparse pc
                         sparse_point_colors,
                         mesh_verts_list, # mesh
                         simplices_list,
                         mesh_colors,
                         prefix="coarse")
        
        view_pcs_cameras(server, 
                         warped_images, # cameras
                         refined_cameras,
                         warped_dense_points_3d, # dense pc
                         warped_images_colors, 
                         refined_sparse_points_3d, # sparse pc
                         sparse_point_colors,
                         warped_mesh_verts_list, # mesh
                         simplices_list,
                         mesh_colors,
                         prefix="refined")
        
        # import pdb; pdb.set_trace()
        while True:
            pass


def entrypoint():
    """Entrypoint for use with pyproject scripts."""
    tyro.extras.set_accent_color("bright_yellow")
    tyro.cli(main)


if __name__ == "__main__":
    entrypoint()