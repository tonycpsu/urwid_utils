# -*- coding: utf-8 -*-

import urwid
from urwid_utils.colors import BASIC_COLORS, STYLES, nearest_basic_color
from urwid_utils.util import is_valid_identifier
from urwid.display_common import _parse_color_256, AttrSpec
try:
    from urwid.display_common import _parse_color_true
    URWID_HAS_TRUE_COLOR=True
except ImportError:
    URWID_HAS_TRUE_COLOR=False

COLORS_ALLOWED_MAP = {
    16: lambda val: val in BASIC_COLORS,
    256: lambda val: _parse_color_256(val) is not None,
    1<<24: lambda val: URWID_HAS_TRUE_COLOR and _parse_color_true(val) is not None
}

class PaletteEntry(list):

    attrs = [
        'name',
        'foreground',
        'background',
        'mono',
        'foreground_high',
        'background_high',
    ]

    DEFAULT_FG_MONO = "white"
    DEFAULT_FG_16 = "light gray"
    DEFAULT_BG_16 = "black"
    DEFAULT_FG_256 = DEFAULT_FG_16
    DEFAULT_BG_256 = DEFAULT_BG_16

    def __init__(self, *args, **kwargs):
        list.__init__(self, [None]*len(self.attrs))
        for index, value in enumerate(args):
            key = self.attrs[index]
            kwargs[key] = value
        for name, value in kwargs.items():
            self.__setattr__(name=name, value=value)

    @classmethod
    def from_config(
            cls, cfg,
            default_fg=DEFAULT_FG_16, default_bg=DEFAULT_BG_16,
            default_fg_hi=DEFAULT_FG_256, default_bg_hi=DEFAULT_BG_256,
            max_colors=2**24
    ):
        """
        Build a palette definition from either a simple string or a dictionary,
        filling in defaults for items not specified.

        e.g.:
            "dark green"
                dark green foreground, black background

            {lo: dark gray, hi: "#666"}
                dark gray on 16-color terminals, #666 for 256+ color

        """
        # TODO: mono

        e = PaletteEntry(mono = default_fg,
                         foreground=default_fg,
                         background=default_bg,
                         foreground_high=default_fg_hi,
                         background_high=default_bg_hi)

        if isinstance(cfg, str):
            e.foreground_high = cfg
            if e.allowed(cfg, 16):
                e.foreground = cfg
            else:
                rgb = AttrSpec(fg=cfg, bg="", colors=max_colors).get_rgb_values()[0:3]
                e.foreground = nearest_basic_color(rgb)

        elif isinstance(cfg, dict):

            bg = cfg.get("bg", None)
            if isinstance(bg, str):
                e.background_high = bg
                if e.allowed(bg, 16):
                    e.background = bg
                else:
                    rgb = AttrSpec(fg=bg, bg="", colors=max_colors).get_rgb_values()[0:3]
                    e.background = nearest_basic_color(rgb)
            elif isinstance(bg, dict):
                e.background_high = bg.get("hi", default_bg_hi)
                if "lo" in bg:
                    if e.allowed(bg["lo"], 16):
                        e.background = bg["lo"]
                    else:
                        rgb = AttrSpec(fg=bg["lo"], bg="", colors=max_colors).get_rgb_values()[0:3]
                        e.background = nearest_basic_color(rgb)

            fg = cfg.get("fg", cfg)
            if isinstance(fg, str):
                e.foreground_high = fg
                if e.allowed(fg, 16):
                    e.foreground = fg
                else:
                    rgb = AttrSpec(fg=fg, bg="", colors=max_colors).get_rgb_values()[0:3]
                    e.foreground = nearest_basic_color(rgb)

            elif isinstance(fg, dict):
                e.foreground_high = fg.get("hi", default_fg_hi)
                if "lo" in fg:
                    if e.allowed(fg["lo"], 16):
                        e.foreground = fg["lo"]
                    else:
                        rgb = AttrSpec(fg=fg["lo"], bg="", colors=max_colors).get_rgb_values()[0:3]
                        e.foreground = nearest_basic_color(rgb)
        return e


    def __repr__(self):
        rep = []
        class_name = self.__class__.__name__
        attrs = []
        for index, attr_name in enumerate(self.attrs):
            value = self[index]
            attrs.append('{0}={1}'.format(attr_name, repr(value)))
        rep.append('<')
        rep.append(class_name)
        rep.append('(')
        rep.append(', '.join(attrs))
        rep.append(')>')
        return ''.join(rep)

    def _key(self):
        return tuple(self[:len(self.attrs)])

    def __hash__(self):
        return hash(self._key())

    def allowed(self, value, colors=None):

        color_allowed = lambda val: any([
                COLORS_ALLOWED_MAP[k](val)
            for k in COLORS_ALLOWED_MAP.keys()
            if not colors or k <= colors
        ])
        return any([(
            val is None
            or val in [v for n,v in STYLES]
            or color_allowed(val)
        ) for val in value.split(',')])

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
        raise AttributeError('"{0}": unknown attribute'.format(name))

class Palette(list):

    def __init__(self, name=None, **entries):
        self.name = name
        for name, entry in entries.items():
            entry.name = name
        list.__init__(self, list(entries.values()))

    def __setattr__(self, name, value):
        if isinstance(value, list):
            if not is_valid_identifier(name):
                raise AttributeError('"{0}" is not a legal python identifier.'.format(name))
            for index, entry in enumerate(self):
                if entry[0] == name:
                    self[index] = value
                    break
            else:
                value.name = name  # Only here do we need to set the PaletteEntry()'s name
                self.append(value)
        else:
            list.__setattr__(self, name, value)

    def __getattr__(self, name):
        for entry in self:
            if entry[0] == name:
                return entry
        raise AttributeError('"{0}": unknown attribute'.format(name))

    def __repr__(self):
        rep = []
        class_name = self.__class__.__name__
        rep.append('<')
        rep.append(class_name)
        rep.append('(\n')
        rep.append('    name={0},\n'.format(repr(self.name)))
        rep.extend(['    {0},\n'.format(repr(e)) for e in self])
        rep.append(')>')
        return ''.join(rep)
