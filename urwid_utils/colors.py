# -*- coding: utf-8 -*-

import re
import urwid
from urwid.display_common import _BASIC_COLORS as BASIC_COLORS
from urwid.display_common import _ATTRIBUTES as STYLES
from urwid_utils.util import get_const_identifiers

STYLES = list(zip([n.upper() for n in STYLES], STYLES))

color_const = get_const_identifiers(urwid.display_common, STYLES)
color_const['STYLES'] = STYLES
globals().update(color_const)
__all__ = list(color_const.keys())
