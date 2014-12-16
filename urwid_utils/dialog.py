# -*- coding: utf-8 -*-

import urwid
from urwid_utils import keys, const
from urwid_utils import PaletteEntry, Palette

BUTTONS_YES_NO = 'yes/no'
BUTTONS_OK_CANCEL = 'ok/cancel'
BUTTONS_OK = 'ok'

class DialogFrame(urwid.Frame):

    def __init__(self, *args, **kwargs):
        self.escape = kwargs.pop(keys.ESCAPE)
        urwid.Frame.__init__(self, *args, **kwargs)
    def keypress(self, size, key):
        if key in (keys.TAB, keys.UP, keys.DOWN):
            if self.focus_part == const.FOCUS_BODY:
                if key in (keys.TAB, keys.DOWN):
                    self.set_focus(const.FOCUS_FOOTER)
            elif self.focus_part == const.FOCUS_FOOTER:
                if key in (keys.TAB, keys.UP):
                    self.set_focus(const.FOCUS_BODY)
        elif key in [keys.ESCAPE,]:
            self.escape()
        return self.__super.keypress(size, key)


class DialogBase(urwid.WidgetWrap):

    palette = Palette()
    palette.body = PaletteEntry()
    palette.footer = PaletteEntry()
    palette.border = PaletteEntry()
    palette.button_normal = PaletteEntry()
    palette.button_select = PaletteEntry()
    palette.reveal_focus = PaletteEntry()

    __metaclass__ = urwid.signals.MetaSignals
    signals = ['commit']

    parent = None
    def __init__(self, width, height, data, loop, header_text=None, buttons=None):

        width = int(width)
        if width <= 0:
            width = (const.RELATIVE, 80)
        height = int(height)
        if height <= 0:
            height = (const.RELATIVE, 80)

        self.loop = loop
        self.parent = self.loop.widget

        self.body = self.make_body(data)
        self.frame = self.make_frame(header_text)
        self.view = self.make_view(width, height)

        self.buttons = buttons
        if self.buttons is None:
            self.buttons = [("OK", True, self.on_affirmative), ("Cancel", False, self.on_negatory)]
        elif isinstance(self.buttons, basestring):
            if self.buttons == BUTTONS_YES_NO:
                self.buttons = [("Yes", True, self.on_affirmative), ("No", False, self.on_negatory)]
            elif self.buttons == BUTTONS_OK_CANCEL:
                self.buttons = [("OK", True, self.on_affirmative), ("Cancel", False, self.on_negatory)]
            elif self.buttons == BUTTONS_OK:
                self.buttons = [("OK", True, self.on_affirmative),]
        self.add_buttons(self.buttons)
        self.exitcode = None
        urwid.WidgetWrap.__init__(self, self.view)

    def make_body(self, data):
        'please implement'

    def make_frame(self, header_text):
        frame = DialogFrame(self.body, focus_part=const.FOCUS_BODY, escape=self.on_negatory)
        if header_text is not None:
            frame.header = urwid.Pile(
                [urwid.Text(header_text),
                 urwid.Divider('=')],
            )
        return frame

    def make_view(self, width, height):
        view = urwid.Padding(self.frame, (const.FIXED_LEFT, 2), (const.FIXED_RIGHT, 2))
        view = urwid.Filler(view, (const.FIXED_TOP, 1), (const.FIXED_BOTTOM, 1))
        view = urwid.AttrWrap(view, self.palette.body)
        view = urwid.LineBox(view)
        view = urwid.Frame(view)
        view = urwid.Overlay(view, self.parent, const.CENTER, width+2, const.MIDDLE, height+2)
        return view

    def callback(self):
        'please implement'

    def add_buttons(self, buttons):
        l = []
        for name, exitcode, callback in buttons:
            b = urwid.Button(name, callback, user_data=exitcode)
            b.exitcode = exitcode
            b = urwid.AttrWrap( b, self.palette.button_normal, self.palette.button_select)
            l.append( b )
        self.buttons = urwid.GridFlow(l, 10, 3, 1, const.CENTER)
        self.frame.footer = urwid.Pile([
            urwid.Divider('-'),
            self.buttons],
            focus_item = 1)

    def _button(self, *args, **kwargs):
        if len(args) == 3:
            _class, button, _status = args
            self.exitcode = button.exitcode
        self.loop.widget = self.parent

    def on_affirmative(self, *args, **kwargs):
        self._button(self, *args, **kwargs)
        urwid.emit_signal(self, 'commit', self.callback())

    def on_negatory(self, *args, **kwargs):
        self._button(self, *args, **kwargs)

    def show(self):
        self.loop.widget = self.view

class YesNoDialog(DialogBase):

    def __init__(self, *args, **kwargs):
        kwargs['buttons'] = 'yes/no'
        DialogBase.__init__(self, *args, **kwargs)

    def make_body(self, data):
        return urwid.Filler(urwid.Text(data))

    def callback(self, *args, **kwargs):
        return self.exitcode

class EditDialog(DialogBase):
    def make_body(self, data):
        edit_text, editor_label = data
        self.edit = urwid.Edit(edit_text=edit_text)
        body = urwid.ListBox(urwid.SimpleListWalker([
            urwid.AttrWrap(urwid.Text(editor_label), None, self.palette.reveal_focus),
            urwid.AttrWrap(self.edit, None, self.palette.reveal_focus),
        ]))
        return body
    def callback(self):
        return self.edit.get_edit_text()


class NoticeDialog(DialogBase):

    def __init__(self, *args, **kwargs):
        kwargs['buttons'] = 'ok'
        DialogBase.__init__(self, *args, **kwargs)

    def make_body(self, data):
        return urwid.Filler(urwid.Text(data))

    def callback(self, *args, **kwargs):
        pass

