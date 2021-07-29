import random
import torch

from .model.model import Generator
from .fontutils.Font import Font
from .data.transform import pil_to_norm_tensor


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

        content_tensor = pil_to_norm_tensor(
            source_font.glyphs_map[target_char_code].to_pil(size_px)
        )

        target_style_tensors = [
            pil_to_norm_tensor(target_font.glyphs_map[char].to_pil(size_px))
            for char in target_style_chars
        ]
        target_styles_tensor = torch.stack(target_style_tensors, dim=1)

        source_style_tensors = [
            pil_to_norm_tensor(source_font.glyphs_map[char].to_pil(size_px))
            for char in source_style_chars
        ]
        source_styles_tensor = torch.stack(source_style_tensors, dim=1)

        model.to(device)
        return model(
            content_tensor.unsqueeze(0).to(device),
            source_styles_tensor.unsqueeze(0).to(device),
            target_styles_tensor.unsqueeze(0).to(device),
        ).squeeze(0)
