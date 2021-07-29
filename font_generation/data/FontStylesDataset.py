from typing import List
from torch.utils.data import IterableDataset
import torch
import random
import albumentations as A

from font_generation.fontutils.Font import Font
from .transform import BASE_TRANSFORMS, pil_to_numpy


def image_index_to_transform_key(index: int) -> str:
    return f"image{index}"


def transform_image_and_styles(transform, image, style_images):
    """Helper to deal with albumentations not working with plain lists of images to be transformed"""
    style_image_keys = {
        image_index_to_transform_key(i): img for i, img in enumerate(style_images)
    }
    results = transform(image=image, **style_image_keys)
    image_tensor = results["image"]
    style_tensors = [
        results[image_index_to_transform_key(i)] for i in range(len(style_images))
    ]
    return image_tensor, style_tensors


class FontStylesDataset(IterableDataset):
    def __init__(
        self,
        fonts: List[Font],
        total_samples: int,
        n_style: int = 4,
        size_px=64,
        static: bool = False,
        enable_transforms: bool = False,
    ):
        super().__init__()
        self.n_style = n_style
        self.size_px = size_px
        self.total_samples = total_samples
        self.fonts = fonts
        self.pregenerated_samples = None

        transform_parts = BASE_TRANSFORMS
        if enable_transforms:
            transform_parts = [
                A.Rotate(limit=15, p=0.8),
                A.RandomScale(scale_limit=0.1, p=0.8),
                A.Affine(translate_px=7, shear=[-10, 10], p=0.8),
                A.PadIfNeeded(min_width=size_px, min_height=size_px, p=1.0),
                A.CenterCrop(height=size_px, width=size_px, p=1.0),
            ] + transform_parts

        # annoyingly it doesn't seem like it's possible to pass a list of images into a transform, it needs
        # to be done via individual keys
        style_image_transform_targets = {
            image_index_to_transform_key(i): "image" for i in range(n_style)
        }
        self.transform = A.Compose(
            transform_parts, p=1.0, additional_targets=style_image_transform_targets
        )

        if static:
            print("pregenerating samples")
            self.pregenerated_samples = [
                self.generate_sample() for _ in range(total_samples)
            ]

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

        content_img = pil_to_numpy(
            content_font.glyphs_map[target_char].to_pil(self.size_px)
        )

        target_img = pil_to_numpy(
            target_font.glyphs_map[target_char].to_pil(self.size_px)
        )

        target_style_imgs = [
            pil_to_numpy(target_font.glyphs_map[char].to_pil(self.size_px))
            for char in target_style_chars
        ]

        content_style_imgs = [
            pil_to_numpy(content_font.glyphs_map[char].to_pil(self.size_px))
            for char in content_style_chars
        ]

        content_tensor, content_style_tensors = transform_image_and_styles(
            self.transform,
            content_img,
            content_style_imgs,
        )

        target_tensor, target_style_tensors = transform_image_and_styles(
            self.transform,
            target_img,
            target_style_imgs,
        )

        return {
            "content": content_tensor,
            "target": target_tensor,
            "content_styles": torch.stack(content_style_tensors, dim=0),
            "target_styles": torch.stack(target_style_tensors, dim=0),
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
