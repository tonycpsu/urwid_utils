# -*- coding: utf-8 -*-

import re
from urwid_utils.util import is_valid_identifier, get_const_identifiers
from urwid import widget, command_map

MISC_CONST_VAL = [
    'cursor left',
    'cursor max left',
    'fixed bottom',
    'fixed left',
    'fixed right',
    'fixed top',
]
MISC_CONST_NAMES = [v.replace(' ', '_').upper() for v in MISC_CONST_VAL]
MISC_CONST = list(zip(MISC_CONST_NAMES, MISC_CONST_VAL))
MISC_CONST.append(('FOCUS_HEADER', 'header'))
MISC_CONST.append(('FOCUS_BODY', 'body'))
MISC_CONST.append(('FOCUS_FOOTER', 'footer'))

const = get_const_identifiers(widget, command_map, MISC_CONST)
globals().update(const)
__all__ = list(const.keys())
