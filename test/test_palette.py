# -*- coding: utf-8 -*-

from urwid_utils import Palette, PaletteEntry
from random import choice
import unittest

class TestPalette(unittest.TestCase):

    def setUp(self):
        pass

    def test_all(self):

        how_many_entries = 200

        attr_names = PaletteEntry.attrs
        colors = ['dark red', 'light blue', 'white', 'yellow', 'dark gray']
        attr_values = ['some_palette_entry'] + colors

        kwargs = dict(list(zip(attr_names, attr_values)))

        some_palette_entry = PaletteEntry(**kwargs)

        for name, value in zip(attr_names, attr_values):
            self.assertEqual(getattr(some_palette_entry, name), value)

        for index, name in enumerate(attr_names):
            if index == 0 and name == 'name':
                continue
            setattr(some_palette_entry, name, choice(attr_values[1:]))
            self.assertEqual(getattr(some_palette_entry, name), some_palette_entry[index])
            some_palette_entry[index] = choice(attr_values[1:])
            self.assertEqual(getattr(some_palette_entry, name), some_palette_entry[index])

        entries = []
        attr_values = [None] + colors
        for number in range(1, how_many_entries):
            name = 'p' + str(number)
            palette_entry = PaletteEntry(**kwargs)
            if number % 2:
                palette_entry.name = name
            else:
                palette_entry[0] = name
            entries.append((name, palette_entry))
        entries = dict(entries)

        palette = Palette(name='palette', **entries)
        self.assertEqual(len(palette), how_many_entries - 1)

        for number in range(1, how_many_entries):
            palette_entry = getattr(palette, 'p' + str(number))
            self.assertIn(palette_entry, palette)
