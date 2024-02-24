"""Depth utilities."""

import torch
from jaxtyping import Float
from torch import Tensor, nn

def depth_to_disparity(depth: Float[Tensor, "BS 1 H W"], min_percentile: float = 0.05, max_percentile: float = 0.95, eps: float = 1e-6):
    """Convert depth to disparity. We normalize according to Eq. 10 in this paper https://arxiv.org/pdf/2401.05583.pdf."""
    assert depth.dim() == 4, "Depth must be of shape (BS, 1, H, W)"
    BS = depth.shape[0]
    disparity = 1 / (depth + eps)
    if min_percentile == 0 and max_percentile == 1:
        return disparity
    disparity_min = torch.quantile(disparity.view(BS, -1).float(), min_percentile, dim=1, interpolation='nearest')
    disparity_max = torch.quantile(disparity.view(BS, -1).float(), max_percentile, dim=1, interpolation='nearest')
    disparity_min = disparity_min.view(BS, 1, 1, 1)
    disparity_max = disparity_max.view(BS, 1, 1, 1)
    disparity = (disparity - disparity_min) / (disparity_max - disparity_min + eps)
    return disparity
