
from .constants import (
    RGB_tuple,
)


def hex_to_rgb(_hex):
    """
    Convert a HEX color representation to an RGB color representation.
    hex :: hex -> [000000, FFFFFF]
    :param _hex: The 3- or 6-char hexadecimal string
    representing the color value.
    :return: RGB representation of the input HEX value.
    :rtype: RGB_tuple

    >>> hex_to_rgb('#FF0000')
    RGB_tuple(red=1.0, green=0.0, blue=0.0)
    >>> hex_to_rgb('#000000')
    RGB_tuple(red=0.0, green=0.0, blue=0.0)
    """
    _hex = _hex.strip('#')
    n = len(_hex) // 3
    if len(_hex) == 3:
        r = int(_hex[:n] * 2, 16)
        g = int(_hex[n:2 * n] * 2, 16)
        b = int(_hex[2 * n:3 * n] * 2, 16)
    else:
        r = int(_hex[:n], 16)
        g = int(_hex[n:2 * n], 16)
        b = int(_hex[2 * n:3 * n], 16)
    return RGB_tuple(*(k/255 for k in (r, g, b)))


def rgb_to_hex(rgb):
    """
    Convert an RGB color representation to a HEX color representation.
    (r, g, b) :: r -> [0.0, 1.0]
                 g -> [0.0, 1.0]
                 b -> [0.0, 1.0]
    :param rgb: A tuple of three numeric values corresponding to the red,
    green, and blue value.
    :return: HEX representation of the input RGB value.
    :rtype: str
    >>> rgb_to_hex((1.0, 0.0, 0.0))
    '#FF0000'
    """
    r, g, b = (k*255 for k in rgb)
    return "#{0}{1}{2}".format(
        *(hex(int(k))[2:].zfill(2) for k in (r, g, b))
    ).upper()
