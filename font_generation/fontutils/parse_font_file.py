from typing import Dict, List
from fontTools.ttLib.sfnt import readTTCHeader
from fontTools.ttLib import TTFont
from fontTools.pens.svgPathPen import SVGPathPen
from os.path import basename

from .Font import Font
from .Glyph import Glpyh


def parse_ttc_font_file(font_path: str) -> List[TTFont]:
    font_name = basename(font_path)
    fonts: List[Font] = []
    with open(font_path, "rb") as file:
        font_header = readTTCHeader(file)
        for font_num in range(font_header.numFonts):
            ttfont = TTFont(file, fontNumber=font_num)
            glpyhs_map: Dict[str, Glpyh] = {}
            glyphSet = ttfont.getGlyphSet()
            for glyph_name in ttfont.getGlyphNames():
                glyph_id = ttfont.getGlyphID(glyph_name)
                glyph = glyphSet[glyph_name]
                if glyph and glyph_id:
                    svgpen = SVGPathPen(glyphSet)
                    glyph.draw(svgpen)
                    glpyhs_map[glyph_id] = Glpyh(
                        unicode=glyph_id,
                        path=svgpen.getCommands(),
                        width=glyph.width,
                        height=glyph.height,
                        lsb=glyph.lsb,
                        tsb=glyph.tsb,
                    )
            fonts.append(Font(name=font_name, number=font_num, glyphs_map=glpyhs_map))
    return fonts
