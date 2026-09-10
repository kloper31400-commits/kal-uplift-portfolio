#!/usr/bin/env python3
"""Downscale every captured frame into web-sized JPEGs for the screenshot book.

Source frames are the full-page retina captures in the uplift-app repo, taken
against the admin demo-state injector, so the console is populated with a
deterministic synthetic cohort.

EXCLUDED, and why. Each of these was found by grepping the captured caption
text against the 239 real participant names in the source data files:

  a13-comms        six real founders by name
  a17-speakers     real speakers against their internal chase state
  a26-portal       a real speaker's name
  a20-comms-person the comms tab again, with no caption text to verify

Run:  python3 make-shots.py          convert everything
      python3 make-shots.py sheets   also build contact sheets for auditing
"""
import pathlib, sys
from PIL import Image, ImageDraw

APP = pathlib.Path("/Users/kennedy/uplift-app")
SHOTS = APP / "build/demo/shots"
DST = pathlib.Path(__file__).parent / "shots"
SHEETS = pathlib.Path(__file__).parent / ".audit"
DST.mkdir(parents=True, exist_ok=True)

# Scale by WIDTH only. An earlier version also capped height at 5200px by
# rescaling the whole image, which meant a very tall capture had its width
# crushed to keep the height down: the resumes page came out 374px wide, 13% of
# the original, and unreadable the moment anyone zoomed. A full-page capture is
# legitimately tall, so let it be tall.
MAX_W, QUALITY = 1600, 80
MAX_H = 30000  # safety only; nothing real approaches this

EXCLUDE = {
    "a13-comms",        # six real founders by name
    "a17-speakers",     # real speakers against their internal chase state
    "a26-portal",       # a real speaker's name
    "a20-comms-person", # comms tab again, no caption text to verify against
    "a23-sop",          # the capture came out blank (mean 255.0, sd 0.0)
}

# The published Luma event is genuinely public.
EXTRA = {"speaker-luma": APP / "build/speaker-system/kenneth-jones/04-luma.png"}

if not SHOTS.exists():
    sys.exit(f"source frames not found at {SHOTS}")


def load(src):
    im = Image.open(src)
    if im.mode in ("RGBA", "LA", "P"):
        bg = Image.new("RGB", im.size, "white")
        im = im.convert("RGBA")
        bg.paste(im, mask=im.split()[-1])
        return bg
    return im.convert("RGB")


def convert(src, out):
    try:
        im = load(src)
    except Exception as e:
        print(f"  ! {src.name}: {e}")
        return False
    w, h = im.size
    scale = min(MAX_W / w, 1.0)
    if h * scale > MAX_H:
        scale = MAX_H / h
    if scale < 1.0:
        im = im.resize((max(1, int(w * scale)), max(1, int(h * scale))), Image.LANCZOS)
    im.save(out, "JPEG", quality=QUALITY, optimize=True, progressive=True)
    return True


frames = sorted(p.stem for p in SHOTS.glob("*.png") if p.stem not in EXCLUDE)

ok = 0
for f in frames:
    if convert(SHOTS / f"{f}.png", DST / f"{f}.jpg"):
        ok += 1
for name, src in EXTRA.items():
    if src.exists() and convert(src, DST / f"{name}.jpg"):
        ok += 1

# Remove any excluded frame left over from an earlier run.
for name in EXCLUDE:
    stale = DST / f"{name}.jpg"
    if stale.exists():
        stale.unlink()
        print(f"  removed previously published frame: {name}")

total = sum(p.stat().st_size for p in DST.glob("*.jpg"))
print(f"converted {ok} frames ({len(EXCLUDE)} withheld)")
print(f"total: {total / 1048576:.1f} MB in {DST}")


# ── Contact sheets, for reviewing many frames at once ─────────────────────
if "sheets" in sys.argv:
    SHEETS.mkdir(exist_ok=True)
    for p in SHEETS.glob("*.jpg"):
        p.unlink()
    # Only the top slice of each frame: names live in headers and cards, and a
    # full-page thumbnail is far too small to read anything on.
    CROP_H, TILE_W, COLS = 900, 640, 2
    names = sorted(p.stem for p in DST.glob("*.jpg"))
    per = 6
    for i in range(0, len(names), per):
        batch = names[i:i + per]
        tiles = []
        for n in batch:
            im = load(DST / f"{n}.jpg")
            im = im.crop((0, 0, im.width, min(CROP_H, im.height)))
            r = TILE_W / im.width
            im = im.resize((TILE_W, int(im.height * r)), Image.LANCZOS)
            tiles.append((n, im))
        rows = (len(tiles) + COLS - 1) // COLS
        rh = max(t.height for _, t in tiles) + 26
        sheet = Image.new("RGB", (TILE_W * COLS + 12, rh * rows + 12), "#dddddd")
        d = ImageDraw.Draw(sheet)
        for j, (n, t) in enumerate(tiles):
            x = (j % COLS) * TILE_W + 6
            y = (j // COLS) * rh + 6
            d.text((x + 3, y + 3), n, fill="#000000")
            sheet.paste(t, (x, y + 20))
        out = SHEETS / f"sheet-{i // per + 1:02d}.jpg"
        sheet.save(out, "JPEG", quality=72, optimize=True)
        print(f"  {out.name}: {', '.join(batch)}")
