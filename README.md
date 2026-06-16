# Italian

An Italian-style serif typeface, in early development. This repo collects the
original 2015 exploratory sketches and provides a clean structure for continuing
the design.

## Structure

```
Italian/
├── sources/              # active development UFO masters (start here)
├── archive/
│   ├── 2015-sketches/    # original exploratory UFOs (preserved for reference)
│   └── example-1.woff    # early compiled web-font test
├── .gitignore
└── README.md
```

## The 2015 sketches

Ten distinct early UFOs are preserved in `archive/2015-sketches/`. Each contains
a handful of glyphs (lowercase `a e h l t y`, the core set for testing a serif's
proportions and rhythm). They fall into three explorations:

| Sketch | Glyphs | Notes |
| --- | --- | --- |
| `attempt at a better serif.ufo` (+ `?`, `??` variants) | a e h l t y | Three iterations refining the serif construction |
| `better?.ufo` / `better? better?.ufo` / `better? better????.ufo` / `better? better???? wit mid.ufo` | a e h l t y | "better?" series; the "wit mid" variant explores a mid contrast |
| `weird serifw.ufo` | a e h l t y | An off-beat serif direction |
| `Sketch Mach 1.ufo` / `Sketch Mach 8.ufo` | a e h | Earliest rough sketches |

Editor autosave duplicates (`-AutoSaved`, `-AutoSaved-AutoSaved`, ` copy`) that
RoboFont generated have been removed; only the saved masters remain.

Font metrics (shared across sketches): UPM 1000, ascender 750, cap height 750,
x-height 500, descender −250.

## Continuing development

1. Pick a sketch direction from `archive/2015-sketches/`.
2. Copy it into `sources/` and give it a proper `familyName` / `styleName` in
   `fontinfo.plist`.
3. Build out the character set from there.

Sources are [UFO](https://unifiedfontobject.org/) — open with RoboFont, Glyphs
(import), or [fontra](https://fontra.xyz/). A build pipeline
(e.g. `fontmake`) can be added once a working master exists.
