def make_metadata(masks_batch):
    metadata = {}

    frames = []
    for i, masks in enumerate(masks_batch):
        frame = {
            "file_path": f"images/{i:05d}.png",
            "depth_file_path": f"depths/{i:05d}.pt",
            "depth_image_file_path": f"depth-images/{i:05d}.png",
            "masks": masks,
        }
        frames.append(frame)
    metadata["frames"] = frames

    return metadata
