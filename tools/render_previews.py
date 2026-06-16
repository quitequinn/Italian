#!/usr/bin/env python3
# Render every glyph in every UFO sketch to an SVG outline and build an HTML
# contact sheet, so the whole body of source material can be compared at a glance.

import os
from defcon import Font
from fontTools.pens.svgPathPen import SVGPathPen

# Directories, relative to repo root.
REPO_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SOURCE_DIR = os.path.join(REPO_ROOT, "archive", "2015-sketches")
OUT_DIR = os.path.join(REPO_ROOT, "previews")
SVG_DIR = os.path.join(OUT_DIR, "svg")

# Display height (px) for each glyph cell in the contact sheet.
CELL_HEIGHT = 140


def glyph_to_svg(glyph, ascender, descender):
	"""Return a standalone SVG string for a single glyph, flipped to screen space."""
	pen = SVGPathPen(glyph.getParent())
	glyph.draw(pen)
	path_data = pen.getCommands()
	width = glyph.width or 1000
	height = ascender - descender  # total em box height in font units
	# Translate to the ascender then flip Y so font space (y-up) maps to SVG (y-down).
	body = (
		'<path d="{d}" fill="#111"/>'.format(d=path_data) if path_data else ""
	)
	return (
		'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {w} {h}" '
		'height="{ch}">'
		'<g transform="translate(0,{asc}) scale(1,-1)">{body}</g>'
		"</svg>"
	).format(w=width, h=height, ch=CELL_HEIGHT, asc=ascender, body=body)


def main():
	os.makedirs(SVG_DIR, exist_ok=True)
	sketches = sorted(
		d for d in os.listdir(SOURCE_DIR) if d.endswith(".ufo")
	)

	html = [
		"<!doctype html><html><head><meta charset='utf-8'>",
		"<title>Italian — source material outlines</title>",
		"<style>",
		"body{font:14px/1.4 -apple-system,sans-serif;margin:2rem;background:#fafafa;color:#111}",
		"h1{font-weight:600}h2{margin-top:2.5rem;font-size:1rem;color:#444}",
		".row{display:flex;flex-wrap:wrap;gap:1rem;align-items:flex-end;",
		"border:1px solid #e3e3e3;border-radius:8px;padding:1rem;background:#fff}",
		".cell{display:flex;flex-direction:column;align-items:center;gap:.25rem}",
		".cell svg{border:1px solid #eee;background:",
		"linear-gradient(#fff,#fff) }",
		".cell .lbl{font-size:11px;color:#888}",
		"</style></head><body>",
		"<h1>Italian — 2015 source outlines</h1>",
		"<p>Every glyph from each sketch, rendered straight from the UFO outlines.</p>",
	]

	for sketch in sketches:
		path = os.path.join(SOURCE_DIR, sketch)
		font = Font(path)
		info = font.info
		ascender = info.ascender if info.ascender is not None else 750
		descender = info.descender if info.descender is not None else -250
		name = sketch[:-4]  # strip .ufo

		# Per-sketch output folder of individual SVG files.
		sketch_svg_dir = os.path.join(SVG_DIR, name)
		os.makedirs(sketch_svg_dir, exist_ok=True)

		glyph_names = sorted(font.keys())
		html.append("<h2>{} &middot; {} glyphs</h2>".format(name, len(glyph_names)))
		html.append("<div class='row'>")
		for gname in glyph_names:
			glyph = font[gname]
			svg = glyph_to_svg(glyph, ascender, descender)
			# Write the standalone SVG file.
			with open(os.path.join(sketch_svg_dir, gname + ".svg"), "w") as fh:
				fh.write(svg)
			html.append(
				"<div class='cell'>{svg}<span class='lbl'>{n}</span></div>".format(
					svg=svg, n=gname
				)
			)
		html.append("</div>")
		print("Rendered {} ({} glyphs)".format(name, len(glyph_names)))

	html.append("</body></html>")
	index_path = os.path.join(OUT_DIR, "index.html")
	with open(index_path, "w") as fh:
		fh.write("\n".join(html))
	print("\nContact sheet: {}".format(index_path))


if __name__ == "__main__":
	main()
