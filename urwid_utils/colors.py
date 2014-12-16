# -*- coding: utf-8 -*-

import re
import urwid
from urwid.display_common import _BASIC_COLORS as BASIC_COLORS
from urwid_utils.util import get_const_identifiers

color_const = get_const_identifiers(urwid.display_common)
globals().update(color_const)
__all__ = color_const.keys()
