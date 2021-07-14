from dataclasses import dataclass
from typing import Dict
from .Glyph import Glpyh


@dataclass
class Font:
    name: str
    number: int
    glyphs_map: Dict[str, Glpyh]
