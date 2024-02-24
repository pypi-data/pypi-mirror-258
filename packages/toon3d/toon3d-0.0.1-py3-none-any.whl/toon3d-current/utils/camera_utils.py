"""
Camera utilities
"""

import torch
import torch.nn as nn


class Cameras(nn.Module):
    def __init__(self, n, fxs=None, fys=None, quats=None, ts=None):
        super().__init__()

        self.n = n

        # camera intrinsics
        if fxs is None: fxs = torch.full([n], 1.0)
        if fys is None: fys = torch.full([n], 1.0)

        self.fxs = nn.Parameter(fxs)
        self.fys = nn.Parameter(fys)

        # camera extrinsics
        if quats is None: quats = torch.tensor([[1, 0, 0, 0]], dtype=torch.float32).repeat(self.n, 1)
        if ts is None: ts = torch.zeros([self.n, 3], dtype=torch.float32)

        self.quats = nn.Parameter(quats)
        self.ts = nn.Parameter(ts)
        
    @property
    def Rs(self):
        qr, qi, qj, qk = self.quats.split(1, -1)

        Rs = (
            torch.stack(
                [
                    torch.stack([0.5 - (qj**2 + qk**2), (qi * qj) - (qr * qk), (qi * qk) + (qr * qj)], -1),
                    torch.stack([(qi * qj) + (qr * qk), 0.5 - (qi**2 + qk**2), (qj * qk) - (qr * qi)], -1),
                    torch.stack([(qi * qk) - (qr * qj), (qj * qk) + (qr * qi), 0.5 - (qi**2 + qj**2)], -1),
                ],
                -1,
            ).mT
            * 2
        )

        return Rs.squeeze(1)

    def forward(self, us, vs, zs):
        """
        us (batch, num_pts)
        vs (batch, num_pts)
        zs (batch, num_pts)

        returns points_3d (batch, num_points, 3)
        """
        points_backprojected = self.backproject(us, vs, zs).permute(0, 2, 1) # (batch, 3, num_points)
        points_3d = (self.Rs @ points_backprojected) + self.ts[...,None]  # (batch, 3, num_points)

        return points_3d.permute(0, 2, 1)  # (batch, num_points, 3)
    
    def backproject(self, us, vs, zs):
        """
        us (batch, num_pts)
        vs (batch, num_pts)
        zs (batch, num_pts)

        returns points_backprojected (batch, num_points, 3)
        """
        points_intrinsics = torch.stack([us / self.fxs[...,None], vs / self.fys[...,None]], -1) # (batch, num_points, 2)
        points_homogenous = nn.functional.pad(points_intrinsics, (0, 1, 0, 0), mode="constant", value=1) # (batch, num_points, 3)
        points_backprojected = points_homogenous * zs[...,None] # (batch, num_points, 3)

        return points_backprojected
