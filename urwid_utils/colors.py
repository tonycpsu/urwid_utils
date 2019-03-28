# -*- coding: utf-8 -*-

import re
import urwid
import math
from urwid.display_common import _BASIC_COLORS as BASIC_COLORS
from urwid.display_common import _BASIC_COLOR_VALUES as BASIC_COLOR_VALUES
from urwid.display_common import _ATTRIBUTES as STYLES
from urwid_utils.util import get_const_identifiers

STYLES = list(zip([n.upper() for n in STYLES], STYLES))

BASIC_COLOR_MAP = dict(zip(BASIC_COLOR_VALUES, BASIC_COLORS))

def rgb_distance(c1, c2):
    (r1,g1,b1) = c1
    (r2,g2,b2) = c2
    return math.sqrt((r1 - r2)**2 + (g1 - g2) ** 2 + (b1 - b2) **2)

def nearest_basic_color(high_color):

    closest_colors = sorted(
        BASIC_COLOR_MAP.keys(),
        key=lambda color: rgb_distance(color, high_color)
    )
    return BASIC_COLOR_MAP[closest_colors[0]]


color_const = get_const_identifiers(urwid.display_common, STYLES)
color_const['STYLES'] = STYLES
globals().update(color_const)
__all__ = list(color_const.keys())
