from collections import namedtuple

HSV_tuple = namedtuple("HSV_tuple", ('hue', 'saturation', 'value'))
RGB_tuple = namedtuple("RGB_tuple", ('red', 'green', 'blue'))

# Different palettes - pastel, dark, default etc
PRESETS = dict(
    pastel=((0.61, 1), (0.77, 1), (1, 1), (1, 0.73), (1, 0.6))
)

SCHEMES = dict(
    mono=(),
    complimentary=(),
)
