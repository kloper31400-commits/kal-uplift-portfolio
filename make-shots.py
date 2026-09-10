#!/usr/bin/env python3
"""Downscale the captured demo frames into web-sized JPEGs for the portfolio.

Source frames are the full-page retina captures in the uplift-app repo
(build/demo/shots), taken against the admin demo-state injector, so the
console is populated with a synthetic mid-programme cohort.

Two frames are deliberately excluded:
  a13-comms   its caption text contains six real participant names
  a20-comms-person  same tab, no caption text to verify against

Run:  python3 make-shots.py
"""
import subprocess, pathlib, sys

SRC = pathlib.Path("/Users/kennedy/uplift-app/build/demo/shots")
DST = pathlib.Path(__file__).parent / "shots"
DST.mkdir(parents=True, exist_ok=True)

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

if not SRC.exists():
    sys.exit(f"source frames not found at {SRC}")

ok, missing = 0, []
for f in FRAMES:
    src = SRC / f"{f}.png"
    if not src.exists():
        missing.append(f)
        continue
    out = DST / f"{f}.jpg"
    subprocess.run(
        ["sips", "-Z", "1400", str(src), "--out", str(out),
         "-s", "format", "jpeg", "-s", "formatOptions", "78"],
        stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, check=False)
    if out.exists():
        ok += 1

total = sum(p.stat().st_size for p in DST.glob("*.jpg"))
print(f"converted {ok} of {len(FRAMES)} frames")
if missing:
    print("missing from source:", ", ".join(missing))
print(f"total: {total/1048576:.1f} MB in {DST}")
