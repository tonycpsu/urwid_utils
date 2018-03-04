# -*- coding: utf-8 -*-
"""
``urwid_utils`` provides some light wrappers, and object-oriented interfaces to some parts of `urwid
<http://urwid.org/>`_ that are otherwise less-so.

urwid_utils.colors
     Mostly color-related constants.

urwid_utils.keys
     Mostly key/escape sequence related constants.

urwid_utils.const
     Miscellaneous constants.

urwid_utils.palette
     An object-oriented interface to the "palette" objects used by ``urwid``.

urwid_utils.dialog
     Very simple, straightforward dialog widgets: Yes/No, text value retrieval, etc.

urwid_utils.util
     Mostly internal-used utilities.
"""

from .palette import *
from .colors import *
from .keys import *
from .const import *
