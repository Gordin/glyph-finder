#!env python

from fontTools.ttLib import TTFont
from sh import fc_list
import sys
import os


class silence:
    def __enter__(self):
        sys.stderr = open(os.devnull, "w")
        sys.stdout = open(os.devnull, "w")

    def __exit__(self, type, value, traceback):
        sys.stderr = sys.__stderr__
        sys.stdout = sys.__stdout__


class GlyphChecker(object):
    def __init__(self, glyph):
        self.glyph = glyph
        self.glyph_code = self.glyph_to_code(self.glyph)

    def get_font_list(self):
        """Gets list of ttf fonts from fc-cache"""
        all_fonts = map(lambda x: x.split(':')[0], fc_list(':', 'file'))
        ttf_fonts = set(filter(lambda x: x.endswith('ttf'), all_fonts))
        return ttf_fonts

    def glyph_to_code(self, glyph):
        """Converts a glyph to the unicode string"""
        code = 'u{}'.format(hex(ord(glyph)).split('x')[1].upper())
        print('Code: {}'.format(code))
        return code

    def check_font(self, fontname):
        """Checks if Glyph is included in given font"""

        font = TTFont(fontname)
        with silence():
            found_glyph = font.getReverseGlyphMap().get(self.glyph_code)

        # if found_glyph:
        #     __import__('pprint').pprint("Found glyph in {}".format(fontname))
        return bool(found_glyph)

    def check_all_fonts(self):
        fonts = self.get_font_list()
        fonts_with_glyph = filter(self.check_font, fonts)
        self.print_fonts(fonts_with_glyph)
        return fonts_with_glyph

    def print_fonts(self, font_list):
        for font in font_list:
            print(font)


if __name__ == "__main__":
    args = sys.argv
    if len(args) != 2:
        print('try this: ./glyph_finder.py \'🐍\'')
        sys.exit(1)
    checker = GlyphChecker(args[1])
    checker.check_all_fonts()
