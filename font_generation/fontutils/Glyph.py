from dataclasses import dataclass
from PIL import Image
from functools import lru_cache
from fontTools.pens.svgPathPen import SVGPathPen
from fontTools.ttLib.ttFont import _TTGlyph, _TTGlyphSet

from .svg_to_pil import svg_to_pil

PADDING_PERCENT = 20


@dataclass
class Glpyh:
    unicode: str
    ttglyph: _TTGlyph
    ttglyphset: _TTGlyphSet
    ascender: int
    descender: int

    def __hash__(self):
        return hash(self.ttglyph) + hash(self.unicode)

    def to_svg(self) -> str:
        # based on https://github.com/fonttools/fonttools/issues/2087
        view_box_height = self.ascender - self.descender
        padding = self.ttglyph.width * (PADDING_PERCENT) / 100
        view_box = f"{self.ttglyph.lsb - padding} 0 {self.ttglyph.width + 2 * padding} {view_box_height + 2 * padding}"
        return (
            f'<svg xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink" version="1.1" viewBox="{view_box}">\n'
            f'<g transform="matrix(1 0 0 -1 0 {self.ascender + padding})">'
            f'<path d="{self.path}" />\n'
            f"</g>"
            "</svg>"
        )

    @property
    def path(self) -> str:
        pen = SVGPathPen(self.ttglyphset)
        self.ttglyph.draw(pen)
        return pen.getCommands()

    @lru_cache(maxsize=1)
    def to_pil(self, size: int) -> Image:
        return svg_to_pil(self.to_svg(), size, size)
