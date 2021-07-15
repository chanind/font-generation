from dataclasses import dataclass

from PIL import Image
from .svg_to_pil import svg_to_pil

PADDING_PERCENT = 20


@dataclass
class Glpyh:
    unicode: str
    path: str
    width: int
    height: int
    lsb: int
    tsb: int
    ascender: int
    descender: int

    @property
    def svg(self) -> str:
        # based on https://github.com/fonttools/fonttools/issues/2087
        view_box_height = self.ascender - self.descender
        padding = self.width * (PADDING_PERCENT) / 100
        view_box = f"{self.lsb - padding} 0 {self.width + 2 * padding} {view_box_height + 2 * padding}"
        return (
            f'<svg xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink" version="1.1" viewBox="{view_box}">\n'
            f'<g transform="matrix(1 0 0 -1 0 {self.ascender + padding})">'
            f'<path d="{self.path}" />\n'
            f"</g>"
            "</svg>"
        )

    def to_pil(self, size: int) -> Image:
        return svg_to_pil(self.svg, size, size)
