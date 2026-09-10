#!/usr/bin/env python3
"""Downscale the captured demo frames into web-sized JPEGs for the portfolio.

Source frames are the full-page retina captures in the uplift-app repo, taken
against the admin demo-state injector, so the console is populated with a
synthetic mid-programme cohort.

Frames deliberately excluded:
  a13-comms, a20-comms-person   the comms tab captures contain six real
                                participant names
  speaker application / slot board   real applicants' private submissions and
                                internal chase states; rebuilt in HTML instead

Run:  python3 make-shots.py
"""
import pathlib, sys
from PIL import Image

APP = pathlib.Path("/Users/kennedy/uplift-app")
SHOTS = APP / "build/demo/shots"
DST = pathlib.Path(__file__).parent / "shots"
DST.mkdir(parents=True, exist_ok=True)

MAX_W = 1400          # plenty for a full-width figure on a 1120px page
MAX_H = 5200          # a few captures are 7700px tall; cap them
QUALITY = 78

FRAMES = """
a02-today a03-deadlines a04-overview a05-roster a05c-roster-profile
a06-mentorapps a06f-founder-apps a06g-founder-review
a08-matching a08d-picks a08e-override a08h-plan-pruned
a09-matched a09b-match-breakdown a10-cohorts a11-signals a12-pulse
a14-reporting a16-sessions a17-speakers a18-review-meetings a21-wins
a22-credibility-expanded a30-intros
m01-gate m02-week1 m03b-quiz-taking m04-deepwork m05-mentor m05d-mentor-card
m06-goals m07-milestones m08-meetings m09-edu m11-directory m12-roadmap
m13-certificate m14-ulrike-widget
e01-acceptance e02-match
""".split()

# The published Luma event is genuinely public, so it comes from the
# speaker-system capture set rather than the demo-state set.
EXTRA = {
    "speaker-luma": APP / "build/speaker-system/kenneth-jones/04-luma.png",
}

if not SHOTS.exists():
    sys.exit(f"source frames not found at {SHOTS}")


def convert(src: pathlib.Path, out: pathlib.Path) -> bool:
    try:
        im = Image.open(src)
    except Exception as e:
        print(f"  ! {src.name}: {e}")
        return False
    if im.mode in ("RGBA", "LA", "P"):
        bg = Image.new("RGB", im.size, "white")
        im = im.convert("RGBA")
        bg.paste(im, mask=im.split()[-1])
        im = bg
    else:
        im = im.convert("RGB")

    w, h = im.size
    scale = min(MAX_W / w, 1.0)
    if h * scale > MAX_H:
        scale = MAX_H / h
    if scale < 1.0:
        im = im.resize((max(1, int(w * scale)), max(1, int(h * scale))), Image.LANCZOS)

    im.save(out, "JPEG", quality=QUALITY, optimize=True, progressive=True)
    return True


ok, missing = 0, []
for f in FRAMES:
    src = SHOTS / f"{f}.png"
    if not src.exists():
        missing.append(f)
        continue
    if convert(src, DST / f"{f}.jpg"):
        ok += 1

for name, src in EXTRA.items():
    if not src.exists():
        missing.append(name)
        continue
    if convert(src, DST / f"{name}.jpg"):
        ok += 1

total = sum(p.stat().st_size for p in DST.glob("*.jpg"))
print(f"converted {ok} of {len(FRAMES) + len(EXTRA)} frames")
if missing:
    print("missing from source:", ", ".join(missing))
print(f"total: {total / 1048576:.1f} MB in {DST}")
