"""
Code for warping losses.
"""

import torch
import torch.nn as nn
from tqdm import tqdm

from pytorch3d.ops.interp_face_attrs import interpolate_face_attributes
from pytorch3d.renderer.blending import hard_rgb_blend, BlendParams

from toon3d.warp.tri_rasterize import rasterize_constant_color

def constant_triangulation_loss(mesh, return_image=False):
    points = mesh.points
    return ConstantTriangulationLoss.apply(points, mesh, return_image)

class ConstantTriangulationLoss(torch.autograd.Function):
    @staticmethod
    def forward(ctx, points, mesh, return_image=False):
        # Implement the forward pass computations here
        # Save any tensors you need for the backward pass in the ctx object
        # Return the output tensors

        fragments = mesh.rasterize(variations=True)
        tri_rast, tri_counts, tri_errors = rasterize_constant_color(mesh.image, fragments, return_errors=True)

        num_faces = len(mesh.faces)

        indices = torch.arange(num_faces).to(mesh.device)
        errors = tri_errors[:num_faces]
        counts = tri_counts[:num_faces]
        
        face_var = torch.nan_to_num(errors / counts)
        var_sorted = face_var.argsort(descending=True)

        indices = indices[var_sorted]
        var_bool = face_var[var_sorted] > (16/255)
        counts_bool = counts[var_sorted] > ((mesh.width * mesh.height) / 200)

        to_split_bool = torch.logical_and(var_bool, counts_bool)
        to_split = indices[to_split_bool]
        
        rms = torch.sqrt(torch.sum(face_var))
        derrors = tri_errors[num_faces:]

        ctx.save_for_backward(torch.tensor(len(mesh.points)), mesh.faces, derrors)

        if return_image:
            # get image
            pix_to_face = fragments.pix_to_face
            mask = torch.logical_and(pix_to_face < len(mesh.faces), pix_to_face > -1)

            tri_rast[~mask[...,None].repeat(1,1,1,1,3)] = 0
            render = (tri_rast.sum(3) / mask.float().sum(3)[...,None])[0]
            return rms, to_split, render.detach().cpu()
        else:
            return rms, to_split

    @staticmethod
    def backward(ctx, grad_output, split_output=None, v_out_image=None):
        # Implement the backward pass computations here
        # Use tensors saved in ctx from the forward pass

        # Your code goes here
        # ...
        num_points, faces, derrors = ctx.saved_tensors

        dEdvx = (derrors[::4] - derrors[1::4]) / 2
        dEdvy = (derrors[2::4] - derrors[3::4]) / 2

        dEdv = torch.zeros([num_points, 2], device=derrors.device)

        dEdv[faces.flatten(), 0] += dEdvx / 3
        dEdv[faces.flatten(), 1] += dEdvy / 3

        return dEdv, None, None