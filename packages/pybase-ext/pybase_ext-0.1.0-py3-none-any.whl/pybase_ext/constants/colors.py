"""Module with enumerations containing color codes."""
from pybase_ext.enum import TupleEnum


class RGB(TupleEnum):
    """
    Enumeration in which members are RGB color codes.
    """

    BLACK = (0, 0, 0)
    WHITE = (255, 255, 255)
    RED = (255, 0, 0)
    GREEN = (0, 255, 0)
    BLUE = (0, 0, 255)
    YELLOW = (255, 255, 0)
    CYAN = (0, 255, 255)
    AQUA = (0, 255, 255)
    MAGENTA = (255, 0, 255)
    FUCHSIA = (255, 0, 255)
    SILVER = (192, 192, 192)
    GRAY = (128, 128, 128)
    MAROON = (128, 0, 0)
    OLIVE = (128, 128, 0)
    DARK_GREEN = (0, 128, 0)
    PURPLE = (128, 0, 128)
    TEAL = (0, 128, 128)
    NAVY = (0, 0, 128)


class BGR(TupleEnum):
    """
    Enumeration in which members are BGR color codes.
    """

    BLACK = (0, 0, 0)
    WHITE = (255, 255, 255)
    RED = (0, 0, 255)
    GREEN = (0, 255, 0)
    BLUE = (255, 0, 0)
    YELLOW = (0, 255, 255)
    CYAN = (255, 255, 0)
    AQUA = (255, 255, 0)
    MAGENTA = (255, 0, 255)
    FUCHSIA = (255, 0, 255)
    SILVER = (192, 192, 192)
    GRAY = (128, 128, 128)
    MAROON = (0, 0, 128)
    OLIVE = (0, 128, 128)
    DARK_GREEN = (0, 128, 0)
    PURPLE = (128, 0, 128)
    TEAL = (128, 128, 0)
    NAVY = (128, 0, 0)
