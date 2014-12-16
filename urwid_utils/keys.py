# -*- coding: utf-8 -*-

import urwid
from urwid_utils.util import is_valid_identifier, get_const_identifiers
from urwid.escape import input_sequences, _keyconv

class KeySequence(str):

    def __init__(self, value=''):
        str.__init__(self, value)

keys = [k for s,k in input_sequences] + _keyconv.values()

keys = set([k for k in keys if isinstance(k, str)])

key_const = {}
for key in keys:
    attr_name = key.replace(' ', '_').upper()
    if is_valid_identifier(attr_name):
        key_const[attr_name] = KeySequence(key)

key_const.update(get_const_identifiers(urwid.escape))
key_const.pop('ESC')         # FIXME: is this necessary?
key_const['ESCAPE'] = 'esc'  # FIXME: is this necessary?
globals().update(key_const)
__all__ = key_const.keys()
