import sys
import os

from pycocotools import mask as cocomask
import cv2
import torch
from segment_anything import sam_model_registry, SamAutomaticMaskGenerator

from nerfstudio.utils.rich_utils import CONSOLE
from PIL import Image


def generate_depths(images, method="marigold", device="cpu"):
    if method == "marigold":
        from toon3d.generative.marigold import Marigold

        marigold = Marigold(device=device)
    elif method == "zoedepth":
        torch.hub.help("intel-isl/MiDaS", "DPT_BEiT_L_384", force_reload=False)  # Triggers fresh download of MiDaS repo
        zoe = torch.hub.load("isl-org/ZoeDepth", "ZoeD_NK", pretrained=True, _verbose=False).to(device)
    else:
        CONSOLE.log(f"[bold red]Invalid depth method: {method}")
        sys.exit(1)

    depths = []
    for i, image in enumerate(images):
        image_tensor = (torch.from_numpy(images[i]).permute(2, 0, 1).to(device).unsqueeze(0) / 255.0).float()
        if method == "marigold":
            depth_tensor = torch.from_numpy(marigold.pipe(Image.fromarray(image)).depth_np)[..., None]
        elif method == "zoedepth":
            depth_tensor = zoe.infer(image_tensor).detach().cpu()[0].permute(1, 2, 0)
        depths.append(depth_tensor)

    return depths


def generate_segments(images, device="cpu"):
    sam_checkpoint = "data/sam-checkpoints/sam_vit_b_01ec64.pth"
    model_type = "vit_b"

    if not os.path.exists(sam_checkpoint):
        CONSOLE.log(f"[bold yellow]File not found: {sam_checkpoint}")
        CONSOLE.log(f"[bold yellow]Downloading `vit_b` from https://github.com/facebookresearch/segment-anything")
        os.system(
            "wget https://dl.fbaipublicfiles.com/segment_anything/sam_vit_b_01ec64.pth && mkdir data/sam-checkpoints/ && mv sam_vit_b_01ec64.pth data/sam-checkpoints/"
        )
    try:
        sam = sam_model_registry[model_type](checkpoint=sam_checkpoint)
        sam.to(device=device)
    except FileNotFoundError as e:
        CONSOLE.log(f"[bold red]{e}")
        CONSOLE.log(f"[bold red]Problem Downloading `vit_b` from https://github.com/facebookresearch/segment-anything")
        sys.exit(1)

    mask_generator = SamAutomaticMaskGenerator(
        model=sam,
        points_per_side=64,
        pred_iou_thresh=0.85,
        stability_score_thresh=0.88,
        stability_score_offset=1,
        box_nms_thresh=0.9,
        output_mode="coco_rle",
    )

    image_segments = []
    for image in images:
        segments = mask_generator.generate(image)

        for idx in range(len(segments)):
            mask_array = cocomask.decode(segments[idx]["segmentation"])
            contours, _ = cv2.findContours(mask_array, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
            polygons = []
            for contour in contours:
                if contour.size >= 6:
                    polygon = [point[0] for point in contour.tolist()]
                    polygons.append(polygon)
            segments[idx]["polygons"] = polygons

        image_segments.append(segments)
    return image_segments
