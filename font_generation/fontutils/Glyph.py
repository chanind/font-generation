from dataclasses import dataclass
from .svg_to_pil import svg_to_pil


@dataclass
class Glpyh:
    unicode: str
    path: str
    width: int
    height: int
    lsb: int
    tsb: int

    def svg(self):
        return (
            f'<svg xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink" version="1.1" viewBox="0 0 {self.width} {self.height}">\n'
            f"{self.path}\n"
            "</svg>"
        )

    def to_pil(self, size: int):
        return svg_to_pil(self.svg, size, size)
