# Just a-zA-Z0-9
ALPHANUM_UNICODE_RANGES = [
    range(48, 58),
    range(65, 91),
    range(97, 123),
]


def is_alphanum_char_code(code: int) -> bool:
    return any([code in code_range for code_range in ALPHANUM_UNICODE_RANGES])
