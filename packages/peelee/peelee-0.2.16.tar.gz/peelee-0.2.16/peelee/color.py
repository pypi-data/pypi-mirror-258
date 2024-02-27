#!/usr/bin/env python3
"""
Utilities
"""
import colorsys
from enum import Enum

from loguru import logger

HLS_MAX = 10**16


class ColorName(Enum):
    """Color names"""

    RED = 0
    GREEN = 1
    BLUE = 2
    YELLOW = 3
    CYAN = 4
    VIOLET = 5
    BLACK = 6
    RANDOM = 7


def fg(hex_color, msg):
    """Decorate msg with hex_color in foreground."""
    _rgb = hex2rgb(hex_color)
    return f"\x01\x1b[38;2;{_rgb[0]};{_rgb[1]};{_rgb[2]}m\x02{msg}\x01\x1b[0m"


def bg(hex_color, msg):
    """Decorate msg with hex_color in background."""
    _rgb = hex2rgb(hex_color)
    return f"\x01\x1b[48;2;{_rgb[0]};{_rgb[1]};{_rgb[2]}m\x02{msg}\x01\x1b[0m"


def hex2rgb(hex_color):
    """ "Convert."""
    hex_color = hex_color.lstrip("#")
    rgb_color = tuple(int(hex_color[i : i + 2], 16) for i in (0, 2, 4))
    return rgb_color


def hex2hls(hex_color):
    """ "Convert."""
    rgb_color = hex2rgb(hex_color)
    normalized_rgb = (
        rgb_color[0] / 255.0,
        rgb_color[1] / 255.0,
        rgb_color[2] / 255.0,
    )
    hls_color = colorsys.rgb_to_hls(
        normalized_rgb[0], normalized_rgb[1], normalized_rgb[2]
    )
    return hls_color


def hls2hex(hls_color):
    """
    Convert HSL color to HEX code.

    Parameter:
    hls_color - tuple containing hue, lightness, and saturation color codes
    such as (0.5277777777777778, 0.04, 1).
    """
    rgb_color = colorsys.hls_to_rgb(hls_color[0], hls_color[1], hls_color[2])
    scaled_rgb = tuple(int(c * 255) for c in rgb_color)
    return rgb2hex(scaled_rgb)


def rgb2hex(rgb_color):
    """ "Convert."""
    scaled_rgb = rgb_color
    if isinstance(rgb_color[0], float):
        scaled_rgb = tuple(int(c * 255) for c in rgb_color)
    hex_color = f"#{scaled_rgb[0]:02X}{scaled_rgb[1]:02X}{scaled_rgb[2]:02X}"
    return hex_color


def crange(s, t, total):
    if s == t:
        return [s * HLS_MAX] * total
    _start = min(s, t)
    _end = max(s, t)
    _step = (_end - _start) / total
    _list = list(
        range(
            round(_start * HLS_MAX),
            round(_end * HLS_MAX),
            round(_step * HLS_MAX),
        )
    )
    if s not in _list:
        _list.insert(0, s * HLS_MAX)
    if t not in _list:
        _list.append(t * HLS_MAX)
    return _list


def generate_gradient_colors(hex_color_source, hex_color_target, total):
    """Generate gradient colors.

    Parameters:
        hex_color_source - hex color code of the source color
        hex_color_target - hex color code of the target color
        total - total number of colors

    Returns:
        list
    """
    h, l, s = hex2hls(hex_color_source)
    h_target, l_target, s_target = hex2hls(hex_color_target)
    h_list = crange(h, h_target, total)
    l_list = crange(l, l_target, total)
    s_list = crange(s, s_target, total)

    hls_list = [
        (
            h_list[index] / HLS_MAX,
            l_list[index] / HLS_MAX,
            s_list[index] / HLS_MAX,
        )
        for index in range(total)
    ]
    logger.debug(hls_list)
    gradient_colors = [hls2hex(hls) for hls in hls_list]
    if hex_color_source not in gradient_colors:
        gradient_colors.insert(0, hex_color_source)
    if hex_color_target not in gradient_colors:
        gradient_colors.append(hex_color_target)
    return gradient_colors


def calculate_relative_luminance(hex_color):
    """Calculate relative luminance for hex color codes.

    Refer to:
    https://www.w3.org/TR/WCAG20-TECHS/G17.html

    Parameter:
    hex_color - hex color code
    """

    rgb_8bit = hex2rgb(hex_color)
    rgb_srgb = tuple(_8bit / 255.0 for _8bit in rgb_8bit)
    r, g, b = tuple(
        _srgb / 12.92 if _srgb <= 0.03928 else ((_srgb + 0.055) / 1.055) ** 2.4
        for _srgb in rgb_srgb
    )

    return 0.2126 * r + 0.7152 * g + 0.0722 * b


def calculate_contrast_ratio(hex_light_color, hex_dark_color):
    """Calculate contrast ratio for hex color codes.

    Parameter:
    hex_light_color - hex color code of the lighter of the foreground or background color
    hex_dark_color - hex color code of the darker of the foreground or background color

    Refer to:
    https://www.w3.org/TR/WCAG20-TECHS/G17.html
    """
    relative_luminance_light = calculate_relative_luminance(hex_light_color)
    relative_luminance_dark = calculate_relative_luminance(hex_dark_color)
    return (relative_luminance_light + 0.05) / (relative_luminance_dark + 0.05)
