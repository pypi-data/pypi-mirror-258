"""
Code for warping a 2D mesh.
"""

import cv2 
import torch
import torch.nn as nn
from scipy.spatial import Delaunay

from pytorch3d.renderer.mesh.rasterizer import Fragments

from toon3d.warp.tri_rasterize import rasterize_face_verts, rasterize_texture


def create_triangulations(points, points_mask, widths, heights):
    corr_points_list = []
    boundary_points_list = [] 
    inner_points_list = []
    simplices_list = []
    for ndx in range(len(points)):
        pts, pts_mask = points[ndx], points_mask[ndx]
        width, height = widths[ndx], heights[ndx]

        corr_points = pts[pts_mask]

        px_len = min(width, height) // 10
        xs, ys = torch.linspace(0, width-1,width//px_len), torch.linspace(0, height-1, height//px_len)
        xx, yy = torch.meshgrid(xs, ys, indexing="ij")
        grid_points = torch.stack([xx.flatten(), yy.flatten()], dim=1)

        keep_grid = torch.full([len(grid_points),], False)
        for i, grid_pt in enumerate(grid_points):
            keep_grid[i] = ~torch.any(torch.sqrt(((grid_pt - corr_points) ** 2).sum(-1)) < px_len)

        grid_points = grid_points[keep_grid]

        # find boundary points
        bound_0 = (grid_points == 0)
        bound_width = (grid_points == width - 1)
        bound_height = (grid_points == height - 1)

        bound_0 = torch.logical_or(bound_0[...,0], bound_0[...,1])
        bound_width = torch.logical_or(bound_width[...,0], bound_width[...,1])
        bound_height = torch.logical_or(bound_height[...,0], bound_height[...,1])

        bound_bool = torch.logical_or(torch.logical_or(bound_height, bound_width), bound_0)

        boundary_points = grid_points[bound_bool]
        inner_points = grid_points[~bound_bool]

        # make simplices
        mesh_points = torch.cat([corr_points, boundary_points, inner_points])
        simplices = get_simplices(mesh_points)

        corr_points_list.append(corr_points)
        boundary_points_list.append(boundary_points)
        inner_points_list.append(inner_points)
        simplices_list.append(simplices)
    
    return corr_points_list, boundary_points_list, inner_points_list, simplices_list

def find_shared_edge_face_pairs(faces):
    device = faces.device

    # Step 1: Create the edges
    edges = torch.cat((faces[:, [0, 1]], faces[:, [1, 2]], faces[:, [2, 0]]), dim=0)

    # Step 2: Sort the edges
    edges = torch.sort(edges, dim=1).values

    # Step 3: Find unique edges and their first occurrence indices
    unique_edges, first_occurrences = torch.unique(edges, dim=0, return_inverse=True)

    # Step 4: Identify matching edges
    face_ndxs = torch.arange(len(faces)).repeat(3).to(device)
    expanded_occurrences = first_occurrences.view(-1, 1).expand(-1, len(first_occurrences))
    matches = expanded_occurrences == expanded_occurrences.T

    # Step 5: Filter out self-matches
    diagonal = torch.eye(matches.shape[0], dtype=torch.bool)
    matches[diagonal] = False

    # Step 6: Extract matching face pairs
    matched_faces = torch.nonzero(matches)
    face_pairs = face_ndxs[matched_faces]

    return face_pairs

def find_inclusive_exclusive(face_pairs, faces):
    num_pairs = len(face_pairs)

    # size (num_pairs, 3, 3)
    # each entry of size (3, 3) is a matrix whose columns align with the verts of face 0 and rows align with verts of face 1
    # if True, that means the entry [f0, f1] is the same, False otherwise
    matches = torch.stack(
        [
            torch.stack([faces[face_pairs][:, 0, v1] == faces[face_pairs][:, 1, v2] for v2 in range(3)])
            for v1 in range(3)
        ]
    ).permute(2, 1, 0)

    matches_1 = matches.any(1).sum(dim=1) != 1
    matches_3 = matches.any(1).sum(dim=1) != 3
    assert torch.all(matches_1), f"element duplicate: {torch.arange(len(matches_3)).to(faces.device)[~matches_1]}"
    assert torch.all(matches_3), f"element duplicate: {torch.arange(len(matches_3)).to(faces.device)[~matches_3]}"

    face_pair_0 = faces[face_pairs][:, 0]  # (num_pairs, 3)
    face_pair_1 = faces[face_pairs][:, 1]  # (num_pairs, 3)

    # verts belonging to the pair of faces that are shared
    inclusive = face_pair_0[matches.any(1)].reshape(num_pairs, 2)
    # not shared
    exclusive = torch.stack(
        [face_pair_0[~matches.any(1)].reshape(num_pairs), face_pair_1[~matches.any(2)].reshape(num_pairs)]
    ).T

    return inclusive, exclusive


def get_simplices(points):
    tri = Delaunay(points.detach().cpu().numpy(), qhull_options="QJ")
    simplices = torch.tensor(tri.simplices, device=points.device)
    return simplices

def draw_tris(mesh, image=None):
    edges = mesh.half_edges.sort(1).values.unique(dim=0)
    edge_points = mesh.points[edges]

    if image is None:
        image = mesh.image[0].cpu().numpy()

    image = image.copy()

    for edge_point in edge_points:
        x1, y1, x2, y2 = edge_point.flatten().int()
        x1, y1, x2, y2 = x1.item(), y1.item(), x2.item(), y2.item()
        image = cv2.line(image, (x1, y1), (x2, y2), (0, 0, 0), thickness=1, lineType=cv2.LINE_AA)
    
    return image

def draw_points(mesh, image=None, points=None, colors=None):

    if image is None:
        image = mesh.image[0].cpu().numpy()

    image = image.copy()
    
    if colors is None:
        colors = [(1.0, 0, 0) * len(points)]

    for point, color in zip(points, colors):
        x, y = point[0].int().item(), point[1].int().item()
        image = cv2.circle(image, (x, y), 2, color, thickness=5)
    return image


class WarpMesh(nn.Module):
    def __init__(self, points, simplices, height, width, uv_points=None, device="cpu"):
        """
        Creates a Mesh designed to fit an input image with triangulation
        """
        super().__init__()

        self.height = height
        self.width = width

        self.points = points.to(device).float()
        self.faces = simplices.to(device)

        if uv_points is None:
            uv_points = self.points.clone()
        self.uv_points = uv_points.to(device)

        self.half_edges, self.edge_twins = self.get_half_edges(self.faces)

        self.device = device

        self.dpx = 1 / min(self.height - 1, self.width - 1)
        self.faces_per_pixel = 16

    @property
    def normalized_points(self):
        points = self.points
        points_normed = points / torch.tensor([self.width - 1, self.height - 1], device=self.device) * 2 - 1
        ratio = self.width / self.height

        if ratio > 1:
            points_normed[..., 0] *= ratio
        elif ratio < 1:
            points_normed[..., 1] /= ratio

        return points_normed

    @property
    def verts(self):
        points_normed = self.normalized_points
        zs = torch.ones(len(points_normed), 1).to(self.device)
        verts = torch.cat([points_normed, zs], 1)

        return verts

    @property
    def face_verts(self):
        return self.verts[self.faces]
    
    @property
    def verts_uvs(self):
        uv_points_normed = self.uv_points / torch.tensor([self.width - 1, self.height - 1], device=self.device)
        return uv_points_normed[self.faces]

    def laplacian_smoothing_loss(self):
        edge_ids, edge_neighbors = torch.cat([self.half_edges, self.half_edges[self.edge_twins < 0].roll(1, dims=1)]).T
        num_neighbors = torch.bincount(edge_ids)[edge_ids]

        points_normed = self.normalized_points

        diffs = ((points_normed[edge_ids] - points_normed[edge_neighbors].detach()) ** 2).sum(-1)
        loss = torch.sum(diffs / num_neighbors)

        return loss

    def rasterize(self, variations=False):
        face_verts = self.face_verts.clone()

        # make variations
        if variations:
            face_verts = torch.cat([face_verts, self.face_verts_variations])

        # rasterize
        while True:
            fragments = rasterize_face_verts(face_verts, (self.height, self.width), self.faces_per_pixel)
            
            # want to make sure there are enough k-dims in rasterization for all faces
            if torch.any(fragments.pix_to_face[...,-1] > -1):
                self.faces_per_pixel += 1
            else:
                return fragments

    def render(self, image, fragments=None):
        if len(image.shape) == 2:
            image = image[None,...,None]
        if len(image.shape) == 3:
            image = image[None]

        assert image.shape[1] == self.height and image.shape[2] == self.width
        assert len(image.shape) == 4, "must be of size (1, height, width, c)"
        if fragments is None:
            fragments = self.rasterize()

        rendered_image = rasterize_texture(image, self.verts_uvs, fragments)[0]

        return rendered_image

    def get_half_edges(self, faces):
        half_edges = torch.stack((faces[:, [0, 1]], faces[:, [1, 2]], faces[:, [2, 0]]), dim=0).permute(1, 0, 2).flatten(0, 1)

        unique, occurances = torch.unique(half_edges.sort().values, dim=0, return_inverse=True)
        expanded_occurances = occurances[...,None].expand(-1, len(occurances))
        matches = expanded_occurances == expanded_occurances.T

        diagonal = torch.eye(3 * len(faces), dtype=torch.bool) # don't let it match to itself
        matches[diagonal] = False

        matched = matches.nonzero().T

        twins = torch.full((3 * len(faces),), -1).to(faces.device)
        twins[matched[0]] = matched[1]
        twins[matched[1]] = matched[0]
        
        return half_edges, twins

    def split_face(self, face_id):
        face_id = face_id % len(self.faces)

        target_face =  self.faces[face_id]
        target_half_edges = self.half_edges[3 * face_id: 3 * (face_id + 1)]
        target_edge_twins = self.edge_twins[3 * face_id: 3 * (face_id + 1)]

        # make and append new point
        new_point_id = torch.tensor([len(self.points)]).to(self.device)
        new_point = self.points[target_face].sum(0).unsqueeze(0) / 3
        self.points = torch.cat([self.points, new_point])

        # create new faces
        new_face_0 = torch.cat([target_half_edges[0], new_point_id])
        new_face_1 = torch.cat([target_half_edges[1], new_point_id])
        new_face_2 = torch.cat([target_half_edges[2], new_point_id])

        new_faces = torch.stack([new_face_0, new_face_1, new_face_2])

        # calculate new half_edges and edge_twins
        new_half_edges, new_edge_twins = self.get_half_edges(new_faces)

        # offset new_edge_twins and reassign
        new_edge_twins[new_edge_twins >= 0] += len(self.edge_twins)
        new_edge_twins[[0, 3, 6]] = target_edge_twins
        
        to_reassign = target_edge_twins >= 0
        reassign_twins =  target_edge_twins[to_reassign]

        reassign_vals = len(self.edge_twins) + torch.tensor([0, 3, 6], device=self.device)
        reassign_vals = reassign_vals[to_reassign]

        # add target face, half_edges, edge_twins
        self.faces = torch.cat([self.faces, new_faces])
        self.half_edges = torch.cat([self.half_edges, new_half_edges])
        self.edge_twins = torch.cat([self.edge_twins, new_edge_twins])
        self.edge_twins[reassign_twins] = reassign_vals

        # remove target face, half_edges, edge_twins
        self.faces = torch.cat([self.faces[:face_id], self.faces[face_id + 1 :]])
        self.half_edges = torch.cat([self.half_edges[:3 * face_id], self.half_edges[3 * (face_id + 1):]])
        self.edge_twins = torch.cat([self.edge_twins[:3 * face_id], self.edge_twins[3 * (face_id + 1):]])
        self.edge_twins[self.edge_twins >= 3 * (face_id + 1)] -= 3
    
    def calc_edge_angles(self, edge_ndxs):
        BC_ndx = edge_ndxs
        CA_ndx = (BC_ndx // 3) * 3 + (BC_ndx + 1) % 3 # base_ndx + tri_pos
        AB_ndx = (BC_ndx // 3) * 3 + (BC_ndx + 2) % 3 # base_ndx + tri_pos  

        BC = self.half_edges[BC_ndx].T
        CA = self.half_edges[CA_ndx].T
        AB = self.half_edges[AB_ndx].T

        B_coord = self.points[BC[0]]
        C_coord = self.points[CA[0]]
        A_coord = self.points[AB[0]]

        B_A = (B_coord - A_coord)
        C_A = (C_coord - A_coord)

        deg_A = torch.acos((B_A * C_A).sum(-1) / (B_A.norm(p=2, dim=-1) * C_A.norm(p=2, dim=-1)))

        return deg_A

    def find_edge_flips(self):
        BC_ndx = self.edge_twins[self.edge_twins >= 0]
        CB_ndx = self.edge_twins[BC_ndx]

        CA_ndx = (BC_ndx // 3) * 3 + (BC_ndx + 1) % 3 # base_ndx + tri_pos 
        BD_ndx = (CB_ndx // 3) * 3 + (CB_ndx + 1) % 3 # base_ndx + tri_pos 

        AB_ndx = (BC_ndx // 3) * 3 + (BC_ndx + 2) % 3 # base_ndx + tri_pos 
        DC_ndx = (CB_ndx // 3) * 3 + (CB_ndx + 2) % 3 # base_ndx + tri_pos 

        # edges
        BC = self.half_edges[BC_ndx].T
        CA = self.half_edges[CA_ndx].T
        AB = self.half_edges[AB_ndx].T

        CB = self.half_edges[CB_ndx].T
        BD = self.half_edges[BD_ndx].T
        DC = self.half_edges[DC_ndx].T

        # coords 
        B_coord = self.points[BC[0]]
        C_coord = self.points[CA[0]]
        A_coord = self.points[AB[0]]
        D_coord = self.points[DC[0]]

        # finding opposite angles
        B_A = -(B_coord - A_coord)
        C_A = -(C_coord - A_coord)

        B_D = -(B_coord - D_coord)
        C_D = -(C_coord - D_coord)

        deg_A = torch.acos((B_A * C_A).sum(-1) / (B_A.norm(p=2, dim=-1) * C_A.norm(p=2, dim=-1))).rad2deg()
        deg_D = torch.acos((B_D * C_D).sum(-1) / (B_D.norm(p=2, dim=-1) * C_D.norm(p=2, dim=-1))).rad2deg()

        deg = deg_A + deg_D

        # TODO: batch code for only allowing valid flips
        flip_edge_0 = BC_ndx[deg > 180.5]
        # flip_edge_1 = CB_ndx[deg > 180]

        # flip_edges = torch.stack([flip_edge_0, flip_edge_1]).sort(0).values.unique(dim=1)
        # flip_edge_counts = flip_edges.flatten().bincount()

        # flip_ndxs = flip_edges[0]
        # flip_ndxs_counts = flip_edge_counts[flip_ndxs]
        if len(flip_edge_0) > 0:
            return flip_edge_0[0].item()
        return -1

    def flip_edge(self, edge_ndx):
        #    A           A
        #  /   \       / | \
        # C-----B  -> C  |  B
        #  \   /       \ | /
        #    D           D

        BC_ndx = edge_ndx
        CB_ndx = self.edge_twins[edge_ndx].item()
        
        if BC_ndx < 0 or CB_ndx < 0:
            return None

        face_0_ndx = BC_ndx // 3
        face_1_ndx = CB_ndx // 3
        
        CA_ndx = face_0_ndx * 3 + (BC_ndx + 1) % 3
        AB_ndx = face_0_ndx * 3 + (CA_ndx + 1) % 3
        
        BD_ndx = face_1_ndx * 3 + (CB_ndx + 1) % 3
        DC_ndx = face_1_ndx * 3 + (BD_ndx + 1) % 3

        # print(BC_ndx, CA_ndx, AB_ndx)
        # print(CB_ndx, BD_ndx, DC_ndx)

        # external twins
        AC_ndx = self.edge_twins[CA_ndx].item()
        BA_ndx = self.edge_twins[AB_ndx].item()

        DB_ndx = self.edge_twins[BD_ndx].item()
        CD_ndx = self.edge_twins[DC_ndx].item()

        # print(AC_ndx, BA_ndx)
        # print(DB_ndx, CD_ndx)

        BC = self.half_edges[BC_ndx]
        CA = self.half_edges[CA_ndx]
        AB = self.half_edges[AB_ndx]

        CB = self.half_edges[CB_ndx]
        BD = self.half_edges[BD_ndx]
        DC = self.half_edges[DC_ndx]

        A = AB[0].item()
        B = BC[0].item()
        C = CA[0].item()
        D = DC[0].item()

        AD = torch.tensor([A, D], device=self.device)
        DA = torch.tensor([D, A], device=self.device)

        # reassign half_edges
        new_half_edges_0 = torch.stack([DA, AB, BD])
        new_half_edges_1 = torch.stack([AD, DC, CA])

        self.half_edges[face_0_ndx * 3: face_0_ndx * 3 + 3] = new_half_edges_0
        self.half_edges[face_1_ndx * 3: face_1_ndx * 3 + 3] = new_half_edges_1

        # reassign twins
        new_DA_ndx = face_0_ndx * 3
        new_AB_ndx = face_0_ndx * 3 + 1
        new_BD_ndx = face_0_ndx * 3 + 2

        new_AD_ndx = face_1_ndx * 3
        new_DC_ndx = face_1_ndx * 3 + 1
        new_CA_ndx = face_1_ndx * 3 + 2

        self.edge_twins[new_DA_ndx] = new_AD_ndx
        self.edge_twins[new_AB_ndx] = BA_ndx
        self.edge_twins[new_BD_ndx] = DB_ndx

        self.edge_twins[new_AD_ndx] = new_DA_ndx
        self.edge_twins[new_DC_ndx] = CD_ndx
        self.edge_twins[new_CA_ndx] = AC_ndx

        if BA_ndx > -1:
            self.edge_twins[BA_ndx] = new_AB_ndx
        if AC_ndx > -1:
            self.edge_twins[AC_ndx] = new_CA_ndx

        if CD_ndx > -1:
            self.edge_twins[CD_ndx] = new_DC_ndx
        if DB_ndx > -1:
           self.edge_twins[DB_ndx] = new_BD_ndx

        # reassign faces
        self.faces[face_0_ndx] = torch.tensor([B, D, A], device=self.device)
        self.faces[face_1_ndx] = torch.tensor([C, A, D], device=self.device)

    def collapse_face(self, face_id):
        face_id = face_id % len(self.faces)

        target_face =  self.faces[face_id]
        target_half_edges = self.half_edges[3 * face_id: 3 * (face_id + 1)]
        target_edge_twins = self.edge_twins[3 * face_id: 3 * (face_id + 1)]

        # print(target_face)
        # print(target_half_edges)
        # print(target_edge_twins)

        num_edges_on_boundary = torch.count_nonzero(target_edge_twins == -1)

        # print(num_edges_on_boundary)
        if num_edges_on_boundary == 0: # internal triangle
            # print(self.points[target_half_edges])
            return False

        elif num_edges_on_boundary == 1: # on a single boundary
            # print(self.points[target_half_edges])

            bound_edge_ndx = (target_edge_twins == -1).nonzero().item()
            edge_ndx_0 = (bound_edge_ndx + 1) % 3
            edge_ndx_1 = (bound_edge_ndx + 2) % 3

            bound_pt_0_ndx = target_half_edges[bound_edge_ndx][0].item()
            bound_pt_1_ndx = target_half_edges[bound_edge_ndx][1].item()
            new_bound_pt_ndx = target_half_edges[edge_ndx_0][1].item()

            bound_pt_0 = self.points[bound_pt_0_ndx]
            bound_pt_1 = self.points[bound_pt_1_ndx]
            new_bound_pt = self.points[new_bound_pt_ndx].detach()

            hoz_or_vert = (bound_pt_0 == bound_pt_1).nonzero().item()

            # classify boundary and stick edge to boundary
            if hoz_or_vert == 1: # horizontal boundary
                if bound_pt_0[1] == 0: # top
                    new_bound_pt[1] = 0
                else: # bound_pt_0[1] == self.height - 1 bottom
                    new_bound_pt[1] = self.height - 1
            else: # hoz_or_vert == 0 vertical boundary
                if bound_pt_0[0] == 0: # left
                    new_bound_pt[0] = 0
                else: # bound_pt_0[0] == self.width - 1 right
                    new_bound_pt[0] = self.width - 1

            # reassign twins
            self.edge_twins[target_edge_twins[edge_ndx_0]] = -1
            self.edge_twins[target_edge_twins[edge_ndx_1]] = -1
            
            # remove target face and its half_edges
            self.faces = torch.cat([self.faces[:face_id], self.faces[face_id + 1 :]])
            self.half_edges = torch.cat([self.half_edges[:3 * face_id], self.half_edges[3 * (face_id + 1):]])
            self.edge_twins = torch.cat([self.edge_twins[:3 * face_id], self.edge_twins[3 * (face_id + 1):]])
            self.edge_twins[self.edge_twins >= 3 * (face_id + 1)] -= 3
            
        else: # on multiple boundaries
            return False
        
        return True

    @property
    def face_verts_variations(self):
        face_verts = self.face_verts.clone()

        # make variations
        num_faces = len(face_verts)

        # batches the 12 variations of each triangle
        # 3 points per triangle x 4 directions per point (up, down, left, right) = 12 variations
        batch_ndxs = torch.arange(0, num_faces).repeat_interleave(12)
        face_verts_variations = face_verts[batch_ndxs]  # (num_faces * 12 tris, 3 points / tri, 3D )

        for v in range(3):
            # offset of vertex batch
            vb = v * 4

            face_verts_variations[vb::12, v] += torch.tensor([self.dpx, 0, 0]).to(self.device)  # right
            face_verts_variations[vb + 1 :: 12, v] += torch.tensor([-self.dpx, 0, 0]).to(self.device)  # left
            face_verts_variations[vb + 2 :: 12, v] += torch.tensor([0, self.dpx, 0]).to(self.device)  # down
            face_verts_variations[vb + 3 :: 12, v] += torch.tensor([0, -self.dpx, 0]).to(self.device)  # up

        return face_verts_variations
    