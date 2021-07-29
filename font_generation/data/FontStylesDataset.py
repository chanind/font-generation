from typing import List
from torch.utils.data import IterableDataset
import torch
import random

from font_generation.fontutils.Font import Font
import albumentations as A
from albumentations.pytorch.transforms import ToTensorV2
from .pil_to_tensor import pil_to_tensor


class FontStylesDataset(IterableDataset):
    def __init__(
        self,
        fonts: List[Font],
        total_samples: int,
        n_style: int = 8,
        size_px=64,
        static: bool = False,
        enable_transforms: bool = False,
    ):
        super().__init__()
        self.n_style = n_style
        self.size_px = size_px
        self.total_samples = total_samples
        self.fonts = fonts
        self.enable_transforms = enable_transforms

        self.pregenerated_samples = None
        if static:
            print("pregenerating samples")
            self.pregenerated_samples = [
                self.generate_sample() for _ in range(total_samples)
            ]

        self.transform = A.Compose(
            [
                A.Rotate(limit=5, p=0.8),
                A.RandomScale(scale_limit=0.05, p=0.8),
                A.Affine(translate_px=4, shear=[-5, 5], p=0.8),
                ToTensorV2(p=1.0),
            ],
            p=1.0,
            additional_targets={
                "glyph_image": "image",
                "style_images": "images",
            },
        )

    def generate_sample(self):
        target_font, content_font = random.sample(self.fonts, k=2)
        common_glyph_keys = list(
            target_font.glyph_keys_set().intersection(content_font.glyph_keys_set())
        )
        target_char = random.choice(common_glyph_keys)
        # Try using only alphanum chars for both target and source styles
        target_style_chars = random.sample(
            target_font.alphanum_glyph_keys_list(), k=self.n_style
        )
        # we're always going to only have alphanum chars for the source styles, ex comic sans
        content_style_chars = random.sample(
            content_font.alphanum_glyph_keys_list(), k=self.n_style
        )

        content_img = content_font.glyphs_map[target_char].to_pil(self.size_px)
        content_tensor = pil_to_tensor(content_img)

        target_img = target_font.glyphs_map[target_char].to_pil(self.size_px)
        target_tensor = pil_to_tensor(target_img)

        target_style_imgs = [
            target_font.glyphs_map[char].to_pil(self.size_px)
            for char in target_style_chars
        ]
        target_style_tensors = [
            pil_to_tensor(style_img) for style_img in target_style_imgs
        ]
        target_styles_tensor = torch.stack(target_style_tensors, dim=0)

        content_style_imgs = [
            content_font.glyphs_map[char].to_pil(self.size_px)
            for char in content_style_chars
        ]
        content_style_tensors = [
            pil_to_tensor(style_img) for style_img in content_style_imgs
        ]
        content_styles_tensor = torch.stack(content_style_tensors, dim=0)

        if self.enable_transforms:
            content_tensor, content_styles_tensor = self.transform(
                glyph_image=content_tensor.numpy(),
                style_images=content_style_tensors.numpy(),
            )
            target_tensor, target_styles_tensor = self.transform(
                glyph_image=target_tensor.numpy(),
                style_images=target_style_tensors.numpy(),
            )

        return {
            "content": content_tensor,
            "target": target_tensor,
            "content_styles": content_styles_tensor,
            "target_styles": target_styles_tensor,
        }

    @property
    def total_per_worker(self):
        worker_info = torch.utils.data.get_worker_info()
        num_workers = worker_info.num_workers if worker_info else 1
        return int(self.total_samples / num_workers)

    def __iter__(self):
        for i in range(self.total_per_worker):
            if self.pregenerated_samples:
                yield self.pregenerated_samples[i]
            else:
                yield self.generate_sample()

    def __len__(self):
        return self.total_per_worker
