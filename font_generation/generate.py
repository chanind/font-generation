import random
import torch

from .model.model import Generator
from .fontutils.Font import Font
from .data.pil_to_tensor import pil_to_tensor


def generate_glyph(
    device: torch.device,
    model: Generator,
    target_char_code: int,
    target_font: Font,
    source_font: Font,
    n_style=4,
    size_px=64,
) -> torch.Tensor:
    with torch.no_grad():
        # Try using only alphanum chars for both target and source styles, possibly not a good idea
        target_style_chars = random.sample(
            target_font.alphanum_glyph_keys_list(), k=n_style
        )
        source_style_chars = random.sample(
            source_font.alphanum_glyph_keys_list(), k=n_style
        )

        content_img = source_font.glyphs_map[target_char_code].to_pil(size_px)
        content_tensor = pil_to_tensor(content_img)

        target_style_imgs = [
            target_font.glyphs_map[char].to_pil(size_px) for char in target_style_chars
        ]
        target_style_tensors = [
            pil_to_tensor(style_img) for style_img in target_style_imgs
        ]
        target_styles_tensor = torch.stack(target_style_tensors, dim=0)

        source_style_imgs = [
            source_font.glyphs_map[char].to_pil(size_px) for char in source_style_chars
        ]
        source_style_tensors = [
            pil_to_tensor(style_img) for style_img in source_style_imgs
        ]
        source_styles_tensor = torch.stack(source_style_tensors, dim=0)

        model.to(device)
        return model(
            content_tensor.unsqueeze(0).to(device),
            source_styles_tensor.unsqueeze(0).to(device),
            target_styles_tensor.unsqueeze(0).to(device),
        ).squeeze(0)
