# -*- coding: utf-8 -*-
"""*MANUAL* testing of urwid_utils.dialog
"""

import curses
import urwid
from urwid_utils import dialog

class TestDialog(dialog.EditDialog):
    pass

class ManualTest(object):

    def __init__(self):

        message = [
            'Press "q" to test YesNoDialog (and optionally quit).',
            'Press "e" to test EditDialog. A NoticeDialog will display',
            'the text you enter.',
        ]

        message = '\n'.join(message)

        self.topmost = urwid.Filler(urwid.Text(message))

    def main(self, *args, **kwargs):
        self.loop = urwid.MainLoop(self.topmost, palette=(), unhandled_input=self.unhandled_input, pop_ups=True, handle_mouse=False)
        self.loop.run()

    def quit(self, *args, **kwargs):
        raise urwid.ExitMainLoop()

    def edit_dialog_callback(self, *args, **kwargs):
        text, = args
        d = dialog.NoticeDialog(40, 10, data='You entered:\n"{0}"'.format(text),
                        header_text='F. Y. I.', loop=self.loop)
        urwid.connect_signal(d, 'commit', lambda *a, **k: None)
        d.show()

    def unhandled_input(self, k):
        if not isinstance(k, str):
            return k
        if k.lower() == 'q':
            d = dialog.YesNoDialog(30, 10, data='Are you sure you want to quit?',
                            header_text='Quitting Application', loop=self.loop)
            urwid.connect_signal(d, 'commit', self.quit)
            d.show()
        if k.lower() == 'e':
            d = TestDialog(50, 10, data=('<<existing text>>', 'please enter some text: '),
                           header_text='The Header Text',
                           loop=self.loop)
            urwid.connect_signal(d, 'commit', self.edit_dialog_callback)
            d.show()

def main():
    curses.wrapper(ManualTest().main)

if __name__ == '__main__':
    main()
