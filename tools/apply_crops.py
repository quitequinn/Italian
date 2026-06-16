#!/usr/bin/env python3
# Apply curation results: crop kept signage photos tight to their lettering and
# write them to reference/mexican-signage/cropped/. Non-destructive (reads the
# full-res Drive originals, never modifies them).

import os, json, glob
from PIL import Image

REPO = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SRC = ("/Users/quinn-keaveney/Library/CloudStorage/GoogleDrive-quinn@quitetype.com/"
       "My Drive/QT Clients/Quite Type/2012 Mexican handpainted signage")
OUT = os.path.join(REPO, "reference", "mexican-signage", "cropped")
os.makedirs(OUT, exist_ok=True)

# Merge every agent result file.
records = []
for rf in sorted(glob.glob("/tmp/result_0*.json")):
	with open(rf) as fh:
		records.extend(json.load(fh))

def original_for(thumb_name):
	"""Recover the full-res original path from a flattened thumbnail filename."""
	stem = thumb_name[:-4] if thumb_name.lower().endswith(".jpg") else thumb_name
	rel = stem.replace("__", "/")
	for ext in (".JPG", ".jpg", ".jpeg", ".JPEG", ".png", ".PNG"):
		cand = os.path.join(SRC, rel + ext)
		if os.path.exists(cand):
			return cand
	# Fallback: glob any extension.
	hits = glob.glob(os.path.join(SRC, glob.escape(rel) + ".*"))
	return hits[0] if hits else None

kept, dropped, errors = 0, 0, []
report = []
for rec in records:
	thumb = rec.get("file")
	keep = rec.get("keep")
	reason = rec.get("reason", "")
	if not keep:
		dropped += 1
		report.append({"file": thumb, "status": "dropped", "reason": reason})
		continue
	src = original_for(thumb)
	if not src:
		errors.append(thumb)
		report.append({"file": thumb, "status": "error-missing-original", "reason": reason})
		continue
	try:
		im = Image.open(src).convert("RGB")
		W, H = im.size
		crop = rec.get("crop")
		if crop and len(crop) == 4:
			x0, y0, x1, y1 = crop
			# Clamp and sanity-check the box; fall back to full frame if degenerate.
			x0, x1 = sorted((max(0.0, min(1.0, x0)), max(0.0, min(1.0, x1))))
			y0, y1 = sorted((max(0.0, min(1.0, y0)), max(0.0, min(1.0, y1))))
			if (x1 - x0) < 0.05 or (y1 - y0) < 0.02:
				box = (0, 0, W, H)
				note = "crop-too-small-used-full"
			else:
				box = (int(x0*W), int(y0*H), int(x1*W), int(y1*H))
				note = "cropped"
		else:
			box = (0, 0, W, H)
			note = "no-crop-box-used-full"
		out_name = os.path.splitext(thumb)[0] + ".jpg"
		im.crop(box).save(os.path.join(OUT, out_name), quality=90)
		kept += 1
		report.append({"file": thumb, "status": note, "reason": reason})
	except Exception as e:
		errors.append(thumb)
		report.append({"file": thumb, "status": "error:" + str(e), "reason": reason})

with open(os.path.join(OUT, "_curation-report.json"), "w") as fh:
	json.dump(report, fh, indent=2)

print("kept/cropped:", kept, "| dropped:", dropped, "| errors:", len(errors))
if errors:
	print("error files:", errors[:10])
