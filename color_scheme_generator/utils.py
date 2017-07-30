
import logging as log
log.basicConfig(level=log.DEBUG)

from color_scheme_generator.constants import (
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
        *(hex(int(round(k)))[2:].zfill(2) for k in (r, g, b))
    ).upper()


def ryb_to_rgb_nishita(R, Y, B):
    """
    Convert between RYB and RGB colorspace
    0 <= R,Y,B,R,G,B <= 1
    Formulas taken from here:
    http://nishitalab.org/user/UEI/publication/Sugita_SIG2015.pdf
    Is not compatible with paletton.com color_wheel

    The opposite of red is not cyan but green
    >>> from colorsys import hsv_to_rgb
    >>> opposite_of_red = hsv_to_rgb(0.5, 1, 1)
    >>> supposedly_green = ryb_to_rgb_nishita(*opposite_of_red)
    >>> print(supposedly_green)
    RGB_tuple(red=0.0, green=1.0, blue=0.0)
    >>> red = ryb_to_rgb_nishita(*hsv_to_rgb(0, 1, 1))
    >>> print(red)
    RGB_tuple(red=1.0, green=0.0, blue=0.0)
    """

    # check for black and white
    RYB = (R, Y, B)
    if max(RYB) == 0:
        return RGB_tuple(1, 1, 1)
    elif min(RYB) == 1:
        return RGB_tuple(0, 0, 0)

    # (5) take black component from each of RYB
    r, y, b = (float(k) - min(RYB) for k in RYB)
    RYB1 = (r, y, b)

    # (6) obtain rgb
    rgb_r = r + y - min(y, b)
    rgb_g = y + 2*min(y, b)
    rgb_b = 2*(b - min(y, b))
    rgb1 = (rgb_r, rgb_g, rgb_b)

    # (7) normalize rgb
    n = max(rgb1)/max(RYB1)
    rgb2 = (k/n for k in rgb1)

    # (8) finally add white component
    Iw = min(1-k for k in RYB)
    return RGB_tuple(*(k + Iw for k in rgb2))


# ------------------------ taken from stackoverflow ------------------
def ryb_to_rgb(r, y, b):  # Assumption: r, y, b in [0, 1]

    def _cubic(t, a, b):
        weight = t * t * (3 - 2*t)
        return a + weight * (b - a)

    # red
    x0, x1 = _cubic(b, 1.0, 0.163), _cubic(b, 1.0, 0.0)
    x2, x3 = _cubic(b, 1.0, 0.5), _cubic(b, 1.0, 0.2)
    y0, y1 = _cubic(y, x0, x1), _cubic(y, x2, x3)
    red = _cubic(r, y0, y1)

    # green
    x0, x1 = _cubic(b, 1.0, 0.373), _cubic(b, 1.0, 0.66)
    x2, x3 = _cubic(b, 0., 0.), _cubic(b, 0.5, 0.094)
    y0, y1 = _cubic(y, x0, x1), _cubic(y, x2, x3)
    green = _cubic(r, y0, y1)

    # blue
    x0, x1 = _cubic(b, 1.0, 0.6), _cubic(b, 0.0, 0.2)
    x2, x3 = _cubic(b, 0.0, 0.5), _cubic(b, 0.0, 0.0)
    y0, y1 = _cubic(y, x0, x1), _cubic(y, x2, x3)
    blue = _cubic(r, y0, y1)

    return (red, green, blue)

# ------------------------- taken from color-scheme.js ----------------


def from_paletton_hue_to_rgbvs(hue, color_wheel):
    """
    generate rgbsv tuples from the given 0 <= hue <=359
    >>> from .constants import COLOR_WHEEL
    >>> for a in range(240, 256):
    ...     print(from_paletton_hue_to_rgbvs(a, COLOR_WHEEL))
    (0, 51, 204, 1.0, 0.8)
    (2, 49, 202, 1.0, 0.79)
    (3, 48, 201, 1.0, 0.79)
    (5, 46, 199, 1.0, 0.78)
    (7, 44, 197, 1.0, 0.77)
    (8, 42, 195, 1.0, 0.77)
    (10, 41, 194, 1.0, 0.76)
    (12, 39, 192, 1.0, 0.75)
    (13, 37, 190, 1.0, 0.75)
    (15, 35, 188, 1.0, 0.74)
    (17, 34, 187, 1.0, 0.73)
    (18, 32, 185, 1.0, 0.73)
    (20, 30, 183, 1.0, 0.72)
    (22, 28, 181, 1.0, 0.71)
    (23, 27, 180, 1.0, 0.71)
    (25, 25, 178, 1.0, 0.7)
    """

    def avrg(a, b, k):
        return a + round((b - a) * k)

    hue = round(hue % 360)

    d = hue % 15
    k = d / 15.
    derivative1 = hue - d
    derivative2 = (derivative1 + 15) % 360
    colorset1 = color_wheel[derivative1]
    colorset2 = color_wheel[derivative2]

    rgbv = tuple(avrg(c1, c2, k) for c1, c2 in zip(colorset1, colorset2))

    return rgbv[:-1] + (1., rgbv[-1]/100)


def get_sv_variations(preset, base_saturation, base_value):
    """
    take preset and sv part from rgbsv
    present generator of 4 (saturation, value) pairs

    >>> from .constants import PRESETS
    >>> for var in get_sv_variations(PRESETS['default'], 1, 0.7):
    ...    print([round(v, 2) for v in var])
    [1, 0.7]
    [1, 0.49]
    [0.25, 1]
    [0.5, 1]
    """

    def calc(x, base_data):
        x = -x * base_data if x < 0 else x
        return 1 if x > 1 else 0 if x < 0 else x

    return ((calc(s, base_saturation), calc(v, base_value)) for s, v in preset)


def variations_generator(rgbsv, sv_variations):
    """
    take rgbsv and sc_variations generator from get_sv_variations
    yield 4 rgb tuples according to variations
    >>> from .constants import PRESETS, COLOR_WHEEL
    >>> for a in range(240, 256):
    ...     rgbvs = from_paletton_hue_to_rgbvs(a, COLOR_WHEEL)
    ...     sv_variations = get_sv_variations(PRESETS['default'], *rgbvs[3:])
    ...     print_hex_variations(variations_generator(rgbvs, sv_variations))
    #0033CC #00248F #BFCFFF #809FFF
    #0231C9 #01228D #C0CFFF #819EFF
    #0330C9 #02228D #C0CEFF #819EFF
    #052EC7 #03208B #C1CEFF #839DFF
    #072CC4 #051F89 #C2CDFF #849CFF
    #082AC4 #061E89 #C2CDFF #859BFF
    #0A29C2 #071D88 #C3CDFF #869AFF
    #0C27BF #081B86 #C3CCFF #8799FF
    #0D25BF #091A86 #C4CCFF #8898FF
    #0F23BD #0B1984 #C4CBFF #8A97FF
    #1122BA #0C1882 #C5CBFF #8B97FF
    #1220BA #0D1782 #C5CAFF #8C96FF
    #141EB8 #0E1581 #C6CAFF #8D94FF
    #161CB5 #0F147F #C7C9FF #8F93FF
    #171BB5 #10137F #C7C9FF #9093FF
    #1919B2 #12127D #C8C8FF #9191FF
    """

    max_rgb = max(rgbsv[:3])
    for s, v in sv_variations:
        v *= 255
        k = v / max_rgb if max_rgb > 0 else 0
        yield tuple(
            min(255, round(v - (v - color * k) * s))
            for color in rgbsv[:3]
        )


def print_hex_variations(variations_generator):
    print(*["#" + "".join(["%02X" % k for k in rgb])
            for rgb in variations_generator])


def _from_rgb_to_hsv(r, g, b):

    r, g, b = [k/255. for k in (r, g, b)]
    v = max(r, g, b)
    d = v - min(r, g, b)

    if d > 0:
        s = d / v
    else:
        return 0, 0, v

    if r == v:
        h = (g - b) / d
    elif g == v:
        h = 2 + (b - r) / d
    else:
        h = 4 + (r - g) / d

    h *= 60
    h %= 360
    h = 360 - h if h < 0 else h

    return h, s, v


def from_rgb_to_paletton_hue(r, g, b, color_wheel):
    from colorsys import rgb_to_hsv

    h, s, v = rgb_to_hsv(r, g, b)
    wheel_hues = tuple(
        rgb_to_hsv(*color_wheel[k][:3])[0] for k in sorted(color_wheel.keys())
    )
    if h in wheel_hues:
        paletton_hue = wheel_hues.index(h) * 15
    else:
        i = sorted(wheel_hues + (h,)).index(h)
        wheel_start = (i - 1) * 15
        wheel_end = i * 15 if i < len(wheel_hues) else 360
        h1 = wheel_hues[i-1]
        h2 = wheel_hues[i] if i < len(wheel_hues) else 1.
        k = (h - h1) / (h2 - h1)
        log.debug(
            "k=%s, h=%s, h1=%s, h2=%s, i1=%s, i2=%s",
            k, h, h1, h2, wheel_start, wheel_end
        )
        paletton_hue = round(
            wheel_start + k * (wheel_end - wheel_start)
        )
        paletton_hue %= 360
    return paletton_hue
