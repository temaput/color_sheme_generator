# -*- coding: utf-8 -*-


from colorsys import hsv_to_rgb, rgb_to_hsv
from .utils import hex_to_rgb, rgb_to_hex
from .constants import (
    RGB_tuple,
    HSV_tuple,
    SCHEMES,
    PRESETS,
)


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


def generate_from_scheme(color, scheme):
    scheme = SCHEMES[scheme]
    yield color


def generate_from_preset(color, preset):
    for saturation_ratio, value_ratio in PRESETS[preset]:
        hue, saturation, value = color.hsv
        yield Color(hsv=HSV_tuple(
            hue,
            saturation*saturation_ratio,
            value*value_ratio
        ))


class Palette:
    def __init__(self, palette):
        self.__palette = palette

    def print_hex_values(self):
        for tones in self.__palette:
            for color in tones:
                print(color.hex)


def generate_palette(color, scheme='mono', preset='pastel'):
    """
    Generates color scheme from given parameters
    >>> cs = generate_palette(Color())
    >>> cs.print_hex_values()
    '#550000'
    '#801515'
    '#AA3939'
    '#D46A6A'
    '#FFAAAA'
    """

    palette = (
        (tone for tone in generate_from_preset(base_color, preset))
        for base_color in generate_from_scheme(color, scheme)
    )
    return Palette(palette)
