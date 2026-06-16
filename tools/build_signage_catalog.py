#!/usr/bin/env python3
# Build an HTML contact sheet of all Mexican-signage reference thumbnails so the
# source material can be reviewed and letterforms curated for the typeface.

import os

REPO_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
THUMB_DIR = os.path.join(REPO_ROOT, "reference", "mexican-signage", "thumbs")
OUT_HTML = os.path.join(REPO_ROOT, "reference", "mexican-signage", "contact-sheet.html")


def main():
	thumbs = sorted(f for f in os.listdir(THUMB_DIR) if f.lower().endswith(".jpg"))
	html = [
		"<!doctype html><html><head><meta charset='utf-8'>",
		"<title>Mexican handpainted signage — reference</title>",
		"<style>",
		"body{font:13px/1.4 -apple-system,sans-serif;margin:1.5rem;background:#111;color:#eee}",
		"h1{font-weight:600}",
		".grid{display:grid;grid-template-columns:repeat(auto-fill,minmax(220px,1fr));gap:.75rem}",
		".cell{background:#1c1c1c;border-radius:6px;overflow:hidden}",
		".cell img{width:100%;display:block}",
		".cell .id{padding:.35rem .5rem;font-size:11px;color:#9a9a9a;font-family:ui-monospace,monospace}",
		"</style></head><body>",
		"<h1>Mexican handpainted signage &mdash; {} reference photos</h1>".format(len(thumbs)),
		"<p>Source for the Italian (reverse-contrast slab) typeface. "
		"Click filenames against the full-res originals in Google Drive to trace from.</p>",
		"<div class='grid'>",
	]
	for t in thumbs:
		# Display name restores the original folder/file from the flattened thumb name.
		shown = t[:-4].replace("__", " / ")
		html.append(
			"<div class='cell'><img loading='lazy' src='thumbs/{f}'>"
			"<div class='id'>{n}</div></div>".format(f=t, n=shown)
		)
	html.append("</div></body></html>")
	with open(OUT_HTML, "w") as fh:
		fh.write("\n".join(html))
	print("Catalog: {} ({} images)".format(OUT_HTML, len(thumbs)))


if __name__ == "__main__":
	main()
