# sources/

Active development UFO masters live here.

## `Italian-Regular.ufo`

Starter master for the typeface. Built by `tools/make_source_ufo.py` with:

- UPM 1000, ascender 750, cap height 750, x-height 500, descender −250
  (matching the 2015 sketches).
- 87 encoded glyphs: `A–Z`, `a–z`, `0–9`, and common punctuation — all empty,
  ready to draw into.

Open with RoboFont, Glyphs (import UFO), or [fontra](https://fontra.xyz/), and
draw the letterforms — derived from the curated signage crops in
[`../reference/mexican-signage/cropped/`](../reference/mexican-signage/cropped).

The original 2015 exploratory sketches are in
[`../archive/2015-sketches/`](../archive/2015-sketches) for reference.

When you want to test, `fontmake -u sources/Italian-Regular.ufo -o otf` will
compile it once it has outlines.
