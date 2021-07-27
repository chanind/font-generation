from pathlib import Path

from .parse_font_file import parse_font_file

FONTS_DIR = (Path(__file__) / ".." / ".." / ".." / "fonts").resolve()
FONT_SUFFIXES = [".ttf", ".ttc", ".otf"]


def load_all_fonts(max_fonts=None, simple_chars_only: bool = False):
    font_files = list(FONTS_DIR.glob("*"))
    fonts = []
    for font_file in font_files[:max_fonts]:
        if font_file.suffix.lower() in FONT_SUFFIXES:
            try:
                font = parse_font_file(font_file, simple_chars_only=simple_chars_only)
                if len(font.glyph_keys_list()) == 0:
                    print(f"Invalid font, no glpyhs: {font.name}")
                    continue
                fonts.append(font)
            except Exception as err:
                print(f"Unable to open font: {font_file}. {err}")
    return fonts
