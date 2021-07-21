from font_generation.fontutils.Font import Font
from typing import List
from torch.utils.data import IterableDataset
from torchvision import transforms
import torch
import random


tensorify = transforms.ToTensor()


def pil_to_tensor(img):
    return tensorify(img)[3, :, :].unsqueeze(0)


class FontStylesDataset(IterableDataset):
    def __init__(
        self,
        fonts: List[Font],
        total_samples: int,
        n_styles: int = 8,
        size_px=64,
        static: bool = False,
    ):
        super().__init__()
        self.n_styles = n_styles
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
        style_font, content_font = random.sample(self.fonts, k=2)
        common_glyph_keys = list(
            style_font.glyph_keys_set().intersection(content_font.glyph_keys_set())
        )
        target_char = random.choice(common_glyph_keys)
        style_chars = random.sample(style_font.glyph_keys_list(), k=self.n_styles)

        content_img = content_font.glyphs_map[target_char].to_pil(self.size_px)
        content_tensor = pil_to_tensor(content_img)

        target_img = style_font.glyphs_map[target_char].to_pil(self.size_px)
        target_tensor = pil_to_tensor(target_img)

        style_imgs = [
            style_font.glyphs_map[char].to_pil(self.size_px) for char in style_chars
        ]
        style_tensors = [pil_to_tensor(style_img) for style_img in style_imgs]
        styles_tensor = torch.stack(style_tensors, dim=0)
        return {
            "content": content_tensor,
            "target": target_tensor,
            "styles": styles_tensor,
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
