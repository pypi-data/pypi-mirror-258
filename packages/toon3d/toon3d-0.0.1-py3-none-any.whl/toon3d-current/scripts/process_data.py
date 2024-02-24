from pathlib import Path
import json
import sys
import os

import numpy as np
import torch
import torch.nn as nn
import mediapy
from skimage import transform

import tyro
from nerfstudio.utils.rich_utils import CONSOLE, status
from nerfstudio.utils.colormaps import apply_depth_colormap
from toon3d.utils.image_processing_utils import generate_depths, generate_segments
from toon3d.utils.json_utils import make_metadata


def main(
    input_path: Path,
    dataset: str,
    data_prefix: Path = Path("data/processed"),
    resize: bool = True,
    max_height: int = 720,
    max_width: int = 960,
    depth_method: str = "zoedepth",
    compute_metadata: bool = True,
):
    """check here"""
    device = torch.device("cuda:0" if torch.cuda.is_available() else "cpu")

    dataset_path = data_prefix / dataset
    images_path = dataset_path / "images"
    depths_path = dataset_path / "depths"
    depth_images_path = dataset_path / "depth-images"

    dataset_path.mkdir(exist_ok=True)
    images_path.mkdir(exist_ok=True)
    depths_path.mkdir(exist_ok=True)
    depth_images_path.mkdir(exist_ok=True)

    image_filenames = sorted(list(input_path.glob("*")))
    images = [mediapy.read_image(imf)[..., :3] for imf in image_filenames]
    # images = (torch.from_numpy(np.array()).permute(0, 3, 1, 2) / 255.0).float()

    # resize and calculate padding
    for i, image in enumerate(images):
        if resize:
            height, width = image.shape[:2]
            height_scale_factor = 1
            width_scale_factor = 1
            if max_height and height > max_height:
                height_scale_factor = max_height / height
            if max_width and width > max_width:
                width_scale_factor = max_width / width
            scale_factor = min(height_scale_factor, width_scale_factor)
            image = transform.resize(image, (scale_factor * height, scale_factor * width), anti_aliasing=True)
            images[i] = (image * 255).astype(np.uint8)

    CONSOLE.log("[bold yellow]Running Depth Estimation...")
    depths = generate_depths(images, method=depth_method, device=device)
    CONSOLE.log("[bold green]:tada: Done Finding Depths.")

    torch.cuda.empty_cache()

    for i, (image, depth) in enumerate(zip(images, depths)):
        # image
        mediapy.write_image(images_path / f"{i:05d}.png", image)
        # depth
        torch.save(depth, depths_path / f"{i:05d}.pt")
        # depth image
        mediapy.write_image(depth_images_path / f"{i:05d}.png", apply_depth_colormap(depth))

    if compute_metadata:
        with status(
            msg="[bold yellow]Running Segment Anything... (This may take a while)",
            spinner="circle",
            verbose=False,
        ):
            segments = generate_segments(images, device)
        CONSOLE.log("[bold green]:tada: Done Segmenting Masks.")
        metadata = make_metadata(segments)
        with open(dataset_path / "metadata.json", "w", encoding="utf-8") as f:
            json.dump(metadata, f, indent=4)


def entrypoint():
    """Entrypoint for use with pyproject scripts."""
    tyro.extras.set_accent_color("bright_yellow")
    tyro.cli(main)


if __name__ == "__main__":
    entrypoint()
