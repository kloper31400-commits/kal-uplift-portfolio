#!/usr/bin/env python3
"""Write shots/manifest.json: the pixel dimensions of every frame.

The book builds its plates in JavaScript, and a lazily-loaded image with no
declared size gives its container zero height until it decodes. Scrolling the
page quickly therefore showed collapsed, empty sections, which reads as
missing content rather than as unloaded content.

With a manifest the plate can reserve the right box up front via aspect-ratio,
so the layout is stable before anything downloads.

Run:  python3 make-manifest.py
"""
import json, pathlib
from PIL import Image

DST = pathlib.Path(__file__).parent / "shots"
out = {}
for p in sorted(DST.glob("*.jpg")):
    with Image.open(p) as im:
        out[p.stem] = [im.width, im.height]

(DST / "manifest.json").write_text(json.dumps(out, indent=0, sort_keys=True))
print(f"manifest: {len(out)} frames")
tall = sorted(out.items(), key=lambda kv: -kv[1][1])[:5]
for k, (w, h) in tall:
    print(f"  tallest  {k:28s} {w}x{h}")
