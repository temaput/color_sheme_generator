# -*- coding: utf-8 -*-


from colorsys import hsv_to_rgb, rgb_to_hsv
from .utils import hex_to_rgb, rgb_to_hex
from .constants import RGB_tuple, HSV_tuple


class Color:
    """
    Color universal container

    >>> mycolor = Color()
    >>> mycolor.hex
    '#FF0000'

    >>> mycolor = Color(rgb=(1.0, 1.0, 1.0))
    >>> mycolor.hex
    '#FFFFFF'

    >>> mycolor = Color(hex="#FF5858")
    >>> mycolor.hex
    '#FF5858'
    >>> round(mycolor.rgb.green, 3)
    0.345
    >>> round(mycolor.hsv.saturation, 3)
    0.655
    """
    def __init__(self, **kwargs):
        if 'hsv' in kwargs:
            self.from_hsv(kwargs['hsv'])
        elif 'rgb' in kwargs:
            self.from_rgb(kwargs['rgb'])
        elif 'hex' in kwargs:
            self.from_hex(kwargs['hex'])
        else:
            # default - red
            self.__hsv = HSV_tuple(0, 1, 1)

    def from_hsv(self, hsv):
        self.__hsv = HSV_tuple(*hsv)

    def from_rgb(self, rgb):
        self.__hsv = HSV_tuple(*rgb_to_hsv(*RGB_tuple(*rgb)))

    def from_hex(self, hex_color):
        self.from_rgb(hex_to_rgb(hex_color))

    @property
    def rgb(self):
        return RGB_tuple(*hsv_to_rgb(*self.hsv))

    @property
    def hex(self):
        return rgb_to_hex(self.rgb)

    @property
    def hsv(self):
        return self.__hsv


def generate_palette(hsv=HSV_tuple(0, 1, 1), scheme='mono', preset='pastel'):
    return (
    )
