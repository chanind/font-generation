from typing import Dict, List, Sequence, Tuple
from fontTools.ttLib.sfnt import readTTCHeader
from fontTools.ttLib import TTFont
from os.path import basename
from pathlib import Path

from .Font import Font
from .Glyph import Glpyh

# just want to keep latin chars, some punct, and Hanzi
VALID_UNICODE_RANGES = [
    range(33, 94),
    range(97, 127),
    # CJK Unified Ideographs
    range(int("4E00", 16), int("9FFF", 16)),
]

FONT_SPECIFIER_NAME_ID = 4
FONT_SPECIFIER_FAMILY_ID = 1


# from https://gist.github.com/pklaus/dce37521579513c574d0
def get_short_name(font: TTFont) -> Tuple[str, str]:
    """Get the short name from the font's names table"""
    name = ""
    family = ""
    for record in font["name"].names:
        if b"\x00" in record.string:
            name_str = record.string.decode("utf-16-be")
        else:
            name_str = record.string.decode("utf-8")
        if record.nameID == FONT_SPECIFIER_NAME_ID and not name:
            name = name_str
        elif record.nameID == FONT_SPECIFIER_FAMILY_ID and not family:
            family = name_str
        if name and family:
            break
    return name, family


def find_best_ttfont(ttfonts: Sequence[TTFont]) -> TTFont:
    for ttfont in ttfonts:
        name, family = get_short_name(ttfont)
        # SC for Simplified Chinese, ex in Noto fonts
        # CN for ukai
        if "SC" in name.upper() or "CN" in name.upper():
            return ttfont
    # can't find a good fit, just return the first item
    return ttfonts[0]


def should_keep_char(code: int) -> bool:
    return any([code in code_range for code_range in VALID_UNICODE_RANGES])


def extract_all_ttc_ttfonts(font_path: str) -> List[TTFont]:
    ttfonts: List[TTFont] = []
    with open(font_path, "rb") as file:
        font_header = readTTCHeader(file)
        for font_num in range(font_header.numFonts):
            ttfont = TTFont(file, fontNumber=font_num)
            ttfonts.append(ttfont)
    return ttfonts


def parse_ttc_font_file(font_path: str) -> Font:
    font_name = basename(font_path)
    ttfonts = extract_all_ttc_ttfonts(font_path)
    return parse_ttfont(find_best_ttfont(ttfonts), font_name)


def parse_ttf_font_file(font_path: str) -> Font:
    font_name = basename(font_path)
    with open(font_path, "rb") as file:
        ttfont = TTFont(file)
    return parse_ttfont(ttfont, font_name)


def parse_font_file(font_path: str) -> Font:
    print(f"loading font: {font_path}")
    if Path(font_path).match("*.ttc") or Path(font_path).match("*.TTC"):
        return parse_ttc_font_file(font_path)
    return parse_ttf_font_file(font_path)


def get_unicode_mapping_for_ttfont(ttfont: TTFont) -> Dict[str, int]:
    mapping: Dict[str, int] = {}
    for cmap_table in ttfont["cmap"].tables:
        for (unicode, name) in cmap_table.cmap.items():
            mapping[name] = unicode
    return mapping


def parse_ttfont(ttfont: TTFont, font_name: str, font_num: int = 0) -> Font:
    glpyhs_map: Dict[int, Glpyh] = {}
    os2 = ttfont["OS/2"]
    ttglyphset = ttfont.getGlyphSet()
    unicode_mapping = get_unicode_mapping_for_ttfont(ttfont)
    for glyph_name in ttfont.getGlyphNames():
        ttglyph = ttglyphset[glyph_name]
        unicode = unicode_mapping.get(glyph_name)
        if ttglyph and unicode and ttglyph.width > 0 and should_keep_char(unicode):
            glpyhs_map[unicode] = Glpyh(
                unicode=unicode,
                ttglyph=ttglyph,
                ttglyphset=ttglyphset,
                ascender=os2.sTypoAscender,
                descender=os2.sTypoDescender,
            )
    return Font(name=font_name, number=font_num, glyphs_map=glpyhs_map)
