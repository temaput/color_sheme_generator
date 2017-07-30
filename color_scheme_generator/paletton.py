from constants import (COLOR_WHEEL_V3, PRESETS_V3)

import logging as log
log.basicConfig(level=log.DEBUG)


class Paletton:
    """
    compose color schemes similar to paletton.com
    """

    COLOR_WHEEL = COLOR_WHEEL_V3
    PRESETS = PRESETS_V3
    DEFAULT_PRESET = PRESETS_V3['full_colors']
    HUE_OFFSETS = None
    EXPANDED_COLOR_WHEEL = None

    def __init__(self, **kwargs):
        if 'COLOR_WHEEL' in kwargs:
            self.COLOR_WHEEL = kwargs['COLOR_WHEEL']
        if 'PRESETS' in kwargs:
            self.PRESETS = kwargs['PRESETS']
        self.EXPANDED_COLOR_WHEEL = expand_color_wheel(self.COLOR_WHEEL)
        self.HUE_OFFSETS = calculate_hue_offsets(self.EXPANDED_COLOR_WHEEL)


def calculate_hue_offsets(color_wheel):
    """
    parse color wheel and give hue offsets compared to traditional hsv
    >>> cw = {300: (120, 0, 106)}
    >>> print(calculate_hue_offsets(cw))
    {307: 300}
    """

    from colorsys import rgb_to_hsv
    return {
        round(rgb_to_hsv(*[rgb/255 for rgb in color_wheel[k]])[0] * 360): k
        for k in range(360) if k in color_wheel
    }


def expand_color_wheel(color_wheel=Paletton.COLOR_WHEEL):
    def expand_color(l, rate=15):
        from itertools import chain
        return (
            tuple(
                chain.from_iterable(
                    (linspace(l[i], l[i+1], rate, endpoint=False)
                     for i in range(len(l)-1))
                )
            ) + tuple(linspace(l[-1], l[0], rate, endpoint=False))
        )

    r, g, b = (expand_color(color, 15) for color in
               zip(*(color_wheel[c] for c in sorted(color_wheel.keys()))))
    return {k: v for k, v in enumerate(
        tuple(round(k) for k in rgb) for rgb in zip(r, g, b)
    )}


def make_sv_variations(rgb, preset):
    """
    take preset and sv part from rgbsv
    present generator of 4 (saturation, value) pairs

    >>> from .constants import PRESETS
    >>> for var in make_sv_variations(
    ... (179, 0, 0), PRESETS['default']):
    ...     print([round(float(v), 2) for v in var])
    [1.0, 0.7]
    [1.0, 0.49]
    [0.25, 1.0]
    [0.5, 1.0]
    """

    from colorsys import rgb_to_hsv

    def calc(x, base_data):
        x = -x * base_data if x < 0 else x
        return 1 if x > 1 else 0 if x < 0 else x

    base_saturation, base_value = rgb_to_hsv(
        *[k / 255 for k in rgb])[1:]
    return (
        (calc(s, base_saturation), calc(v, base_value))
        for s, v in preset
    )


def variations_generator(rgb, sv_variations):
    """

    >>> preset = PRESETS_V3['full_colors']
    >>> for rgb in ((255, 0, 0), (0, 204, 0)):
    ...     sv_vars = make_sv_variations(rgb, preset)
    ...     print_hex_variations(variations_generator(rgb, sv_vars))
    #FF6363 #FF3939 #FF0000 #C50000 #9B0000
    #54D954 #2ECF2E #00CC00 #009E00 #007C00
    """
    max_rgb = max(rgb)
    for s, v in sv_variations:
        v *= 255
        k = v / max_rgb if max_rgb > 0 else 0
        yield tuple(
            min(255, round(v - (v - color * k) * s))
            for color in rgb
        )


def print_hex_variations(variations_generator):
    print(*["#" + "".join(["%02X" % k for k in rgb])
            for rgb in variations_generator])


def from_paletton_hue_to_rgb(hue, paletton):
    """
    Gets rgb tuple from hue on paletton color_wheel
    0 <= hue < 360
    >>> p = Paletton()
    >>> from_paletton_hue_to_rgb(255, p)
    (27, 27, 179)
    >>> from_paletton_hue_to_rgb(257, p)
    (31, 26, 178)
    """

    hue = round(hue)
    return paletton.EXPANDED_COLOR_WHEEL[hue]


def from_rgb_to_paletton_hue(rgb, paletton):
    """
    >>> p = Paletton()
    >>> print(from_rgb_to_paletton_hue((120, 0, 106), p))
    318
    """
    from colorsys import rgb_to_hsv
    rhs_hue = round(rgb_to_hsv(*rgb)[0]*360)
    if rhs_hue not in paletton.HUE_OFFSETS:
        keys = sorted(paletton.HUE_OFFSETS.keys())
        closest_offset_index = sorted(keys + [rhs_hue]).index(rhs_hue)
        rhs_hue = keys[closest_offset_index-1]

    return paletton.HUE_OFFSETS[rhs_hue]


def linspace(start, stop, num, endpoint=True):
    step = (stop - start)/(num - (1 if endpoint else 0))
    return (k*step + start for k in range(num))
