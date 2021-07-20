from dataclasses import dataclass
from functools import lru_cache
from typing import Dict
from .Glyph import Glpyh


@dataclass
class Font:
    name: str
    number: int
    glyphs_map: Dict[str, Glpyh]

    def __hash__(self):
        return hash(self.name + f"{self.number}")

    @lru_cache(maxsize=1)
    def glyph_keys_list(self):
        return list(self.glyphs_map.keys())

    @lru_cache(maxsize=1)
    def glyph_keys_set(self):
        return set(self.glyphs_map.keys())
