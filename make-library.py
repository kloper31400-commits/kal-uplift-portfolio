#!/usr/bin/env python3
"""Generate work/library.html: a complete index of every published deliverable.

The curated list on the portfolio home shows about thirty pieces. This indexes
all of them, with the real <title> read out of each HTML file, so nothing that
was made ends up unreachable just because it did not make the shortlist.

Run:  python3 make-library.py
"""
import re, html, pathlib, json

ROOT = pathlib.Path(__file__).parent
WORK = ROOT / "work"

# Ordered: first matching rule wins.
RULES = [
    ("Peer session formats",   r"^(hot-seat|pitch-without)"),
    ("The resource library",   r"^resource"),
    ("How the programme works", r"(matching-logic|three-meetings|goal-loop|how-we-decided|program-requirements|improvements-onepager|speaker-system-post)"),
    ("Guides & onboarding",    r"(portal-guide|onboarding|launch-guide|welcome-packet|quiz|runbook)"),
    ("Writing & essays",       r"(diner|retrospective|blog|overheard|ten-list|expert-sessions-post|carousel-job)"),
    ("Email systems",          r"(email|icymi|nudge|apology|reply)"),
    ("Demo Night",             r"^demo-night"),
    ("Summit & events",        r"(summit|run-of-show|event-holds|pitch-challenge|thank-you|signin|name-tags|mic-flag|camera-wrap|ticket|coasters)"),
    ("Print & brand",          r"(poster|brand|certificate|confetti|square|wrap)"),
    ("Surveys & instruments",  r"(survey|exit)"),
    ("Grant reporting",        r"^njeda"),
    ("Data & rosters",         r"(companies|dates-to-know|lookbook|linkedin|tag-list|candidates)"),
]

TITLE = re.compile(r"<title>(.*?)</title>", re.S | re.I)
H1 = re.compile(r"<h1[^>]*>(.*?)</h1>", re.S | re.I)


def strip(s):
    s = re.sub(r"<[^>]+>", " ", s)
    return html.unescape(re.sub(r"\s+", " ", s)).strip()


def label(p: pathlib.Path):
    if p.suffix.lower() == ".html":
        try:
            body = p.read_text(errors="ignore")[:8000]
        except Exception:
            body = ""
        m = TITLE.search(body) or H1.search(body)
        if m:
            t = strip(m.group(1))
            t = re.sub(r"\s*[·|]\s*(Uplift|TechUnited).*$", "", t).strip()
            if t:
                return t
    if p.suffix.lower() == ".md":
        try:
            for line in p.read_text(errors="ignore").splitlines():
                if line.startswith("# "):
                    return line[2:].strip()
        except Exception:
            pass
    # Fall back to a readable version of the filename.
    return p.stem.replace("-", " ").replace("_", " ").strip().capitalize()


def bucket(name):
    for title, pat in RULES:
        if re.search(pat, name, re.I):
            return title
    return "Other"


SKIP_EXT = {".png", ".jpg", ".jpeg", ".svg", ".json"}
files = [p for p in sorted(WORK.iterdir())
         if p.is_file() and p.suffix.lower() not in SKIP_EXT
         and p.name not in {"library.html"}]

groups = {}
for p in files:
    groups.setdefault(bucket(p.name), []).append(p)

# Keep the declared order, then Other last.
order = [t for t, _ in RULES if t in groups] + (["Other"] if "Other" in groups else [])

# An HTML file and its PDF twin collapse into one row with two links.
def rows(items):
    seen, out = set(), []
    by_stem = {}
    for p in items:
        by_stem.setdefault(p.stem, []).append(p)
    for p in items:
        if p.stem in seen:
            continue
        seen.add(p.stem)
        sibs = by_stem[p.stem]
        primary = next((s for s in sibs if s.suffix == ".html"), sibs[0])
        out.append((label(primary), sorted(sibs, key=lambda s: s.suffix)))
    return sorted(out, key=lambda r: r[0].lower())


body = []
total = 0
for g in order:
    rs = rows(groups[g])
    total += len(rs)
    cards = []
    for name, sibs in rs:
        links = " ".join(
            f'<a class="ext" href="{s.name}">{s.suffix.lstrip(".").upper()}</a>' for s in sibs)
        cards.append(
            f'<div class="row"><span class="nm">{html.escape(name)}</span>'
            f'<span class="lk">{links}</span></div>')
    body.append(
        f'<section class="grp"><h2>{html.escape(g)} '
        f'<span class="ct">{len(rs)}</span></h2><div class="rows">' + "".join(cards) + "</div></section>")

page = f"""<!doctype html>
<html lang="en"><head><meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>Everything I Made · Uplift</title>
<link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800&display=swap" rel="stylesheet">
<style>
  :root{{--indigo:#5c4eb5;--deep:#3d2f8a;--night:#1a0e4f;--light:#9b8fcf;--line:#e8e4f5;
        --surface:#f5f3ff;--ink:#1a1733;--muted:#6b6480;}}
  *{{box-sizing:border-box;margin:0;padding:0}}
  body{{background:#fff;font-family:'Inter',system-ui,sans-serif;color:var(--ink);-webkit-font-smoothing:antialiased}}
  .bar{{background:#1a1733;color:#fff;font-size:12.5px;padding:9px 20px;text-align:center}}
  .bar a{{color:#c7bcff}}
  .hero{{background:linear-gradient(150deg,var(--night),var(--deep) 55%,var(--indigo));color:#fff;padding:54px 24px 58px}}
  .hero-in{{max-width:920px;margin:0 auto}}
  .eyebrow{{font-size:11px;font-weight:800;letter-spacing:.15em;text-transform:uppercase;color:#b6a9ff;margin-bottom:14px}}
  h1{{font-size:clamp(28px,5vw,42px);font-weight:900;letter-spacing:-1.2px;line-height:1.08;margin-bottom:14px}}
  .hero p{{font-size:16px;line-height:1.62;opacity:.9;max-width:64ch}}
  main{{max-width:920px;margin:0 auto;padding:8px 24px 90px}}
  .grp{{padding-top:40px}}
  .grp h2{{font-size:13px;font-weight:800;letter-spacing:.09em;text-transform:uppercase;color:var(--muted);
          padding-bottom:9px;border-bottom:1px solid var(--line);margin-bottom:2px;display:flex;gap:9px;align-items:center}}
  .ct{{background:var(--surface);color:var(--indigo);border-radius:20px;padding:2px 9px;font-size:11px;letter-spacing:0}}
  .rows{{}}
  .row{{display:flex;gap:14px;align-items:center;padding:11px 4px;border-bottom:1px solid var(--line)}}
  .row:last-child{{border-bottom:0}}
  .nm{{flex:1;font-size:14px;font-weight:600;line-height:1.45}}
  .lk{{display:flex;gap:6px;flex-shrink:0}}
  .ext{{font-size:10.5px;font-weight:800;letter-spacing:.05em;text-decoration:none;
       border:1px solid var(--line);border-radius:6px;padding:4px 9px;color:var(--indigo);background:#fff}}
  .ext:hover{{background:var(--surface);border-color:var(--light)}}
  .note{{background:var(--surface);border:1px solid var(--line);border-left:3px solid var(--light);
        border-radius:9px;padding:13px 16px;font-size:13.5px;color:var(--muted);line-height:1.6;margin-top:30px}}
  .note strong{{color:var(--ink)}}
</style></head><body>
<div class="bar">Every published deliverable, indexed automatically ·
  <a href="../index.html">back to the portfolio</a></div>
<div class="hero"><div class="hero-in">
  <div class="eyebrow">The complete set</div>
  <h1>Everything I made</h1>
  <p>{total} deliverables from two cohorts of Uplift: one-pagers, guides, session formats, essays,
  email systems, event collateral and print. Built as code and rendered, which is why the whole set
  could be regenerated when the fall dates moved.</p>
</div></div>
<main>
{"".join(body)}
<div class="note"><strong>What is not here.</strong> Anything naming a real founder, mentor or grant
participant is withheld: the per-participant NJEDA verification forms, the completion reports, the
one-on-one logs, the named certificates and the individual founder pages. Those exist, they are just
not mine to publish.</div>
</main>
</body></html>"""

(WORK / "library.html").write_text(page)
print(f"library.html: {total} deliverables across {len(order)} groups")
for g in order:
    print(f"  {len(rows(groups[g])):3d}  {g}")
