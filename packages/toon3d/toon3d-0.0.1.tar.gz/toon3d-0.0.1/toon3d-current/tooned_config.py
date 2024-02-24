"""
Define the toon3d method config.
"""

from __future__ import annotations

from nerfstudio.configs.base_config import ViewerConfig

from nerfstudio.engine.optimizers import AdamOptimizerConfig
from nerfstudio.engine.schedulers import (
    ExponentialDecaySchedulerConfig,
)
from nerfstudio.engine.trainer import TrainerConfig
from toon3d.toon3d_model import toon3dModelConfig
from toon3d.toon3d_pipeline import toon3dPipelineConfig
from toon3d.toon3d_datamanager import toon3dDataManagerConfig
from toon3d.toon3d_dataparser import toon3dDataParserConfig

from nerfstudio.plugins.types import MethodSpecification

toon3d_config = MethodSpecification(
    TrainerConfig(
        method_name="toon3d",
        steps_per_eval_image=100,
        steps_per_eval_batch=100,
        steps_per_save=2000,
        steps_per_eval_all_images=100000,
        max_num_iterations=30000,
        mixed_precision=False,
        gradient_accumulation_steps={"camera_opt": 100},
        pipeline=toon3dPipelineConfig(
            datamanager=toon3dDataManagerConfig(
                dataparser=toon3dDataParserConfig(eval_mode="all", load_3D_points=True, depth_unit_scale_factor=1.0)
            ),
            model=toon3dModelConfig(
                warmup_length=0,
                sh_degree=0,
                num_downscales=0,
                use_scale_regularization=True,
                max_gauss_ratio=1.0,
                scale_reg_mult=10.0,
                output_depth_during_training=True,
            ),
        ),
        optimizers={
            "xyz": {
                "optimizer": AdamOptimizerConfig(lr=1.6e-4, eps=1e-15),
                "scheduler": ExponentialDecaySchedulerConfig(
                    lr_final=1.6e-6,
                    max_steps=30000,
                ),
            },
            "features_dc": {
                "optimizer": AdamOptimizerConfig(lr=0.0025, eps=1e-15),
                "scheduler": None,
            },
            "features_rest": {
                "optimizer": AdamOptimizerConfig(lr=0.0025 / 20, eps=1e-15),
                "scheduler": None,
            },
            "opacity": {
                "optimizer": AdamOptimizerConfig(lr=0.05, eps=1e-15),
                "scheduler": None,
            },
            "scaling": {
                "optimizer": AdamOptimizerConfig(lr=0.005, eps=1e-15),
                "scheduler": None,
            },
            "rotation": {"optimizer": AdamOptimizerConfig(lr=0.001, eps=1e-15), "scheduler": None},
            "camera_opt": {
                "optimizer": AdamOptimizerConfig(lr=1e-3, eps=1e-15),
                "scheduler": ExponentialDecaySchedulerConfig(lr_final=5e-5, max_steps=30000),
            },
        },
        viewer=ViewerConfig(num_rays_per_chunk=1 << 15, camera_frustum_scale=0.5, default_composite_depth=False),
        vis="viewer",
    ),
    description="Method for reconstructing toon3d.",
)
