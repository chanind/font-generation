from font_generation.fontutils.Font import Font
from typing import List
from torch.utils.data import IterableDataset
from torchvision import transforms
import torch
import random


tensorify = transforms.Compose(
    [
        transforms.ToTensor(),
        transforms.Normalize(mean=(0.5, 0.5, 0.5, 0.5), std=(0.5, 0.5, 0.5, 0.5)),
    ]
)


def pil_to_tensor(img):
    return tensorify(img)[3, :, :].unsqueeze(0)


class FontStylesDataset(IterableDataset):
    def __init__(
        self,
        fonts: List[Font],
        total_samples: int,
        n_style: int = 8,
        size_px=64,
        static: bool = False,
    ):
        super().__init__()
        self.n_style = n_style
        self.size_px = size_px
        self.total_samples = total_samples
        self.fonts = fonts

        self.pregenerated_samples = None
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
        target_style_chars = random.sample(
            target_font.glyph_keys_list(), k=self.n_style
        )
        content_style_chars = random.sample(
            content_font.glyph_keys_list(), k=self.n_style
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
