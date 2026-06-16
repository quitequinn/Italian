#!/usr/bin/env python3
# Create a starter UFO master for the Italian typeface with correct metrics and
# an empty-but-encoded glyph set, ready to draw letterforms into.

import os
from defcon import Font

REPO = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
OUT = os.path.join(REPO, "sources", "Italian-Regular.ufo")

font = Font()
info = font.info
info.familyName = "Italian"
info.styleName = "Regular"
info.unitsPerEm = 1000
info.ascender = 750
info.capHeight = 750
info.xHeight = 500
info.descender = -250
info.italicAngle = 0
info.versionMajor = 0
info.versionMinor = 1
info.openTypeNameDesigner = "Quinn Keaveney"
info.note = "Italian (reverse-contrast slab) display face, drawn from 2012 Yucatan hand-painted signage."

# Default advance widths (font units) for the starter set.
W_LETTER = 600
W_NARROW = 320
W_SPACE = 280

# Build the encoded glyph set: name -> unicode.
glyph_order = [".notdef", "space"]
specs = {}  # name -> (unicode, width)
specs["space"] = (0x0020, W_SPACE)

for code in range(ord("A"), ord("Z") + 1):
	name = chr(code)
	specs[name] = (code, W_LETTER)
	glyph_order.append(name)
for code in range(ord("a"), ord("z") + 1):
	name = chr(code)
	specs[name] = (code, W_LETTER)
	glyph_order.append(name)
for code in range(ord("0"), ord("9") + 1):
	name = {"0":"zero","1":"one","2":"two","3":"three","4":"four","5":"five",
	        "6":"six","7":"seven","8":"eight","9":"nine"}[chr(code)]
	specs[name] = (code, W_LETTER)
	glyph_order.append(name)

# Common punctuation (Italian signage uses quotes, periods, etc.).
punct = {
	"period": 0x002E, "comma": 0x002C, "colon": 0x003A, "semicolon": 0x003B,
	"exclam": 0x0021, "question": 0x003F, "quotedbl": 0x0022, "quotesingle": 0x0027,
	"hyphen": 0x002D, "slash": 0x002F, "ampersand": 0x0026, "parenleft": 0x0028,
	"parenright": 0x0029, "quoteleft": 0x2018, "quoteright": 0x2019,
	"quotedblleft": 0x201C, "quotedblright": 0x201D, "dollar": 0x0024,
	"percent": 0x0025, "asterisk": 0x002A, "numbersign": 0x0023,
	"exclamdown": 0x00A1, "questiondown": 0x00BF,
}
for name, code in punct.items():
	w = W_NARROW if name in ("period","comma","colon","semicolon","exclam",
	                         "hyphen","quotesingle","quoteleft","quoteright") else W_LETTER
	specs[name] = (code, w)
	glyph_order.append(name)

# .notdef first, no unicode.
notdef = font.newGlyph(".notdef")
notdef.width = W_LETTER

for name in glyph_order:
	if name == ".notdef":
		continue
	code, width = specs[name]
	g = font.newGlyph(name)
	g.width = width
	if code is not None:
		g.unicode = code

font.glyphOrder = glyph_order
font.lib["public.glyphOrder"] = glyph_order

font.save(OUT)
print("Created", OUT)
print("Glyphs:", len(font), "| UPM", info.unitsPerEm, "| cap", info.capHeight, "x-ht", info.xHeight)
