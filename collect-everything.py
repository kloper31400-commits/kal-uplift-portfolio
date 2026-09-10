#!/usr/bin/env python3
"""Sweep every authored deliverable out of uplift-app into the portfolio.

Classification is automatic, not by hand. Every real name in the programme
(founders, mentors, speakers) is pulled out of the source data files, and each
deliverable is grepped against that list:

    names a real participant  ->  private/   (gitignored, never published)
    names nobody              ->  work/      (published)

Binary files (PDF, images) cannot be grepped reliably, so they are matched on
filename against the same name list and otherwise routed by folder convention.

Run:  python3 collect-everything.py
"""
import re, shutil, pathlib, sys, subprocess

APP = pathlib.Path("/Users/kennedy/uplift-app")
OUT = pathlib.Path(__file__).parent
WORK, PRIV = OUT / "work", OUT / "private"
for d in (WORK, PRIV):
    d.mkdir(parents=True, exist_ok=True)

if not APP.exists():
    sys.exit(f"source repo not found at {APP}")


# ── Build the roster of real names ────────────────────────────────────────
def names_from(path, pairs=True):
    p = APP / path
    if not p.exists():
        return set()
    src = p.read_text(errors="ignore")
    out = set()
    if pairs:
        for m in re.finditer(r'first:\s*"([^"]+)"\s*,\s*last:\s*"([^"]+)"', src):
            out.add(f"{m.group(1)} {m.group(2)}")
    for m in re.finditer(r'name:\s*"([A-Z][a-zA-Z\'À-ɏ.-]+ [A-Z][a-zA-Z\'À-ɏ.-]+[^"]*)"', src):
        out.add(m.group(1).strip())
    return out


REAL = set()
for f in ["lib/mentees.js", "lib/fall-cohort.js", "lib/fall-mentors.js",
          "lib/summer-mentors.js", "lib/expert-speakers.js", "lib/uplift-alumni.js"]:
    REAL |= names_from(f)

# Kennedy and the team are not participants; their names may appear freely.
TEAM = {"Kennedy Loper", "MJ Durkin", "Jackie Anzaroot", "Aaron Price"}
REAL = {n for n in REAL if n and n not in TEAM and len(n.split()) >= 2}
print(f"roster: {len(REAL)} real participant names")


# ── What to sweep ─────────────────────────────────────────────────────────
SOURCES = []
SOURCES += sorted((APP / "public").glob("*.html"))
SOURCES += sorted((APP / "public").glob("*.pdf"))
SOURCES += sorted(APP.glob("*.md"))
SOURCES += sorted(APP.glob("*.html"))
SOURCES += sorted(APP.glob("*.pdf"))

# Folders that are participant records by definition, whatever is in them.
ALWAYS_PRIVATE_DIRS = ["one-on-one-logs", "public/certificates"]

SKIP = {"README.md", "DEPLOY.md", "CLAUDE.md"}

TEXT_EXT = {".html", ".md", ".txt", ".svg"}


def classify(p: pathlib.Path):
    """Return 'private' or 'work'."""
    if p.suffix.lower() in TEXT_EXT:
        try:
            body = p.read_text(errors="ignore")
        except Exception:
            return "private"
        for n in REAL:
            if n in body:
                return "private"
        return "work"
    # Binary: match the filename against the roster, slugified.
    stem = p.stem.lower().replace("_", "-")
    for n in REAL:
        slug = n.lower().replace(" ", "-").replace("'", "").replace(".", "")
        if slug and slug in stem:
            return "private"
    # A PDF built from an HTML sibling inherits that sibling's verdict.
    sib = p.with_suffix(".html")
    if sib.exists():
        return classify(sib)
    return "work"


counts = {"work": 0, "private": 0, "skipped": 0}
routed = {"work": [], "private": []}

for src in SOURCES:
    if src.name in SKIP:
        counts["skipped"] += 1
        continue
    verdict = classify(src)
    dst = (WORK if verdict == "work" else PRIV) / src.name
    shutil.copy2(src, dst)
    # A file staged into work/ by an earlier pass must be removed from it when
    # this pass decides it is private. Copying to private/ does not do that,
    # and a stale copy in work/ is exactly the leak this script exists to stop.
    if verdict == "private":
        stale = WORK / src.name
        if stale.exists():
            stale.unlink()
    counts[verdict] += 1
    routed[verdict].append(src.name)

# Whole folders that are always private.
for d in ALWAYS_PRIVATE_DIRS:
    s = APP / d
    if not s.exists():
        continue
    t = PRIV / pathlib.Path(d).name
    if t.exists():
        shutil.rmtree(t)
    shutil.copytree(s, t)
    n = len(list(t.rglob("*")))
    print(f"  {d} -> private/{pathlib.Path(d).name}  ({n} files)")

print(f"\nwork/    {counts['work']} files published")
print(f"private/ {counts['private']} files withheld")
print(f"skipped  {counts['skipped']}")

# Show what got withheld, so the call is reviewable rather than silent.
print("\nWithheld because they name a real participant:")
for n in sorted(routed["private"])[:40]:
    print(f"   {n}")
if len(routed["private"]) > 40:
    print(f"   ... and {len(routed['private']) - 40} more")

# Fix asset paths in the newly copied HTML so it renders standalone.
for img in ["uplift-logo.png", "uplift-logo-white.png", "techunited-logo.png",
            "uplift-mountain-mark.png", "aidn-logo.svg", "overdrive-logo.png",
            "uplift-confetti-band.png", "uplift-email-header.png"]:
    s = APP / "public" / img
    if s.exists():
        shutil.copy2(s, WORK / img)

for html in WORK.glob("*.html"):
    try:
        t = html.read_text(errors="ignore")
    except Exception:
        continue
    o = t
    for img in ["uplift-logo.png", "uplift-logo-white.png", "techunited-logo.png",
                "uplift-mountain-mark.png", "aidn-logo.svg", "overdrive-logo.png"]:
        t = t.replace(f'="/{img}"', f'="{img}"')
    if t != o:
        html.write_text(t)

# ── Final safety sweep ────────────────────────────────────────────────────
# Belt and braces. Whatever put a file in work/ (this script, an earlier pass,
# a hand copy), nothing naming a real participant is allowed to stay there.
moved = []
for p in sorted(list(WORK.glob("*.html")) + list(WORK.glob("*.md")) + list(WORK.glob("*.txt"))):
    try:
        body = p.read_text(errors="ignore")
    except Exception:
        continue
    hits = sorted(n for n in REAL if n in body)
    if hits:
        shutil.move(str(p), str(PRIV / p.name))
        pdf = p.with_suffix(".pdf")
        if pdf.exists():
            shutil.move(str(pdf), str(PRIV / pdf.name))
        moved.append((p.name, hits[:3]))

if moved:
    print(f"\nSafety sweep pulled {len(moved)} more file(s) out of work/:")
    for name, hits in moved:
        print(f"   {name}  ({', '.join(hits)})")
else:
    print("\nSafety sweep: work/ is clean.")

print(f"\nTotal in work/:    {len(list(WORK.iterdir()))}")
print(f"Total in private/: {len(list(PRIV.iterdir()))}")
