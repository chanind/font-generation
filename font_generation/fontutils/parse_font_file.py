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
            fonts.append(parse_ttfont(ttfont, font_name, font_num))
    return fonts


def parse_ttf_font_file(font_path: str) -> List[TTFont]:
    font_name = basename(font_path)
    with open(font_path, "rb") as file:
        ttfont = TTFont(file)
    return [parse_ttfont(ttfont, font_name)]


def get_unicode_mapping_for_ttfont(ttfont: TTFont) -> Dict[str, int]:
    mapping: Dict[str, int] = {}
    for cmap_table in ttfont["cmap"].tables:
        for (unicode, name) in cmap_table.cmap.items():
            mapping[name] = unicode
    return mapping


def parse_ttfont(ttfont: TTFont, font_name: str, font_num: int = 0) -> Font:
    glpyhs_map: Dict[int, Glpyh] = {}
    os2 = ttfont["OS/2"]
    glyphSet = ttfont.getGlyphSet()
    unicode_mapping = get_unicode_mapping_for_ttfont(ttfont)
    for glyph_name in ttfont.getGlyphNames():
        glyph = glyphSet[glyph_name]
        unicode = unicode_mapping.get(glyph_name)
        if glyph and unicode and glyph.width > 0:
            svgpen = SVGPathPen(glyphSet)
            glyph.draw(svgpen)
            glpyhs_map[unicode] = Glpyh(
                unicode=unicode,
                path=svgpen.getCommands(),
                width=glyph.width,
                height=glyph.height,
                lsb=glyph.lsb,
                tsb=glyph.tsb,
                ascender=os2.sTypoAscender,
                descender=os2.sTypoDescender,
            )
    return Font(name=font_name, number=font_num, glyphs_map=glpyhs_map)
