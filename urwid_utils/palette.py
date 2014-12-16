# -*- coding: utf-8 -*-

from urwid_utils.colors import BASIC_COLORS
from urwid_utils.util import is_valid_identifier
import urwid
from collections import OrderedDict

class PaletteEntry(list):

    attrs = [
        u'name',
        u'foreground',
        u'background',
        u'mono',
        u'foreground_high',
        u'background_high',
    ]

    def __init__(self, *args, **kwargs):
        list.__init__(self, [None]*len(self.attrs))
        for index, value in enumerate(args):
            key = self.attrs[index]
            kwargs[key] = value
        for name, value in kwargs.iteritems():
            self.__setattr__(name=name, value=value)

    def __repr__(self):
        rep = []
        class_name = self.__class__.__name__
        attrs = []
        for index, attr_name in enumerate(self.attrs):
            value = self[index]
            attrs.append(u'{0}={1}'.format(attr_name, repr(value)))
        rep.append(u'<')
        rep.append(class_name)
        rep.append(u'(')
        rep.append(u', '.join(attrs))
        rep.append(u')>')
        return u''.join(rep)

    def __str__(self):
        return self.name

    def _key(self):
        return tuple(self[:len(self.attrs)])

    def __hash__(self):
        return hash(self._key())

    def allowed(self, value):
        return value is None or value in BASIC_COLORS

    def __setattr__(self, name, value):
        if name != 'name' and not self.allowed(value):
            raise ValueError('"{0}": value not allowed'.format(value))
        try:
            index = self.attrs.index(name)
            list.__setitem__(self, index, value)
            return
        except ValueError:
            pass
        list.__setattr__(self, name, value)

    def __getattr__(self, name):
        try:
            index = self.attrs.index(name)
            return self[index]
        except ValueError:
            pass
        raise AttributeError(u'"{0}": unknown attribute'.format(name))

class Palette(list):

    def __init__(self, name=None, **entries):
        self.name = name
        for name, entry in entries.iteritems():
            entry.name = name
        list.__init__(self, entries.values())

    def __setattr__(self, name, value):
        if not is_valid_identifier(name):
            raise AttributeError(u'"{0}" is not a legal python identifier.'.format(name))
        for index, entry in enumerate(self):
            if entry[0] == name:
                self[index] = [name] + value
        list.__setattr__(self, name, value)

    def __getattr__(self, name):
        for entry in self:
            if entry[0] == name:
                return entry
        raise AttributeError(u'"{0}": unknown attribute'.format(name))

    def __repr__(self):
        rep = []
        class_name = self.__class__.__name__
        rep.append(u'<')
        rep.append(class_name)
        rep.append(u'(\n')
        rep.append(u'    name={0},\n'.format(repr(self.name)))
        rep.extend([u'    {0},\n'.format(repr(e)) for e in self])
        rep.append(u')>')
        return u''.join(rep)
