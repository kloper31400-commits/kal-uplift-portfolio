#!/usr/bin/env python3
"""Publish a real deliverable with every real person swapped for an invented one.

Some of the best pieces in this repo cannot be published as they stand because
they name founders, mentors or speakers: the onboarding deck, the ICYMI mentor
update, the speaker briefs. Withholding them loses the design and the writing
along with the names, which is the wrong trade when the names are the only part
that has to go.

So each real name gets a stable invented replacement, applied consistently:
full name, first name alone, last name alone, the email local-part, and any
LinkedIn slug built from it. Companies get the same treatment. The mapping is
deterministic, so the same person is the same invented person in every file and
the documents stay internally consistent with each other.

The output is then re-audited against the full roster, and anything still
matching is reported rather than published quietly.

Run:  python3 sanitize.py
"""
import re, json, hashlib, pathlib, sys

APP = pathlib.Path("/Users/kennedy/uplift-app")
OUT = pathlib.Path(__file__).parent / "work"
OUT.mkdir(parents=True, exist_ok=True)

# Files to sanitise and publish: (source, output name)
TARGETS = [
    ("public/onboarding-deck-fall2026-test.html", "onboarding-deck-fall2026.html"),
    ("public/onboarding-deck.html",               "onboarding-deck-summer.html"),
    ("public/fall-mentor-icymi-email.html",       "mentor-icymi-email.html"),
    ("public/uplift-speaker-onepagers.html",      "speaker-onepagers.html"),
    ("public/uplift-fall-speaker-runbook.html",   "speaker-runbook.html"),
    ("public/uplift-certificate.html",            "certificate.html"),
    ("public/uplift-speak.html",                  "share-your-expertise.html"),
    # The current match email, regenerated 10 Sept. Picked because it carries
    # both the founder's five Deep Work answers and the November progress
    # section, so the published example is the richest version rather than the
    # thinnest.
    ("public/match-emails/laura-acosta.html",     "match-email-example.html"),
]

FIRST = """Amara Nora Hugo Omar Tessa Priya Delphine Soren Ingrid Rosa Emil Ada Naomi Theo
Camille Felix Sylvie Anika Devon Marcus Jonas Margit Elena Greta Reza Julian Beatriz Zara
Caleb Lina Otto Mira Petra Yusuf Clara Idris Freya Malik Ines Bruno Saoirse Kwame Liesl
Rafael Noor Anton Maja Dario Elif Tomas""".split()

LAST = """Halloran Okafor Quintero Cortland Rutherford Vasquez Voss Marchand Lindqvist Petrov
Novak Achterberg Brannigan Bhatt Sundqvist Adeyemi Fenwick Underwood Delgado Kovacs
Thibodeaux Saldivar Restrepo Wrobel Ngata Brandt Mbeki Panetta Castellanos Aldridge
Fenwick Okonkwo Sterling Kirkland Larsen Moreau Bergstrom Haddad Nakamura Oyelaran
Ferreira Dubois Ivanova Sorensen Bekele Winters Calderon Ashworth Mensah Pavlenko""".split()

COMPANY_A = """Fieldnote Juniper Alder Cobalt Redshift Palisade Tidewater Longview Bramble
Verdigris Northvale Lantern Kestrel Meridian Coldstart Parcelwise Ledgerbloom Grainline
Trellis Standhold Fernpost Kilnwork Southport Copperleaf Brightwater Stonefall""".split()
COMPANY_B = """Labs Robotics Logistics Systems Health Works Analytics Foods Studio Partners
Technologies Collective Industries Group Ventures""".split()


def pick(pool, key, salt=""):
    h = int(hashlib.sha256((salt + key.lower()).encode()).hexdigest(), 16)
    return pool[h % len(pool)]


def synth_name(real):
    f = pick(FIRST, real, "f")
    l = pick(LAST, real, "l")
    return f, l, f"{f} {l}"


def synth_company(real):
    return f"{pick(COMPANY_A, real, 'ca')} {pick(COMPANY_B, real, 'cb')}"


# ── Roster of real names and companies ────────────────────────────────────
def read(p):
    q = APP / p
    return q.read_text(errors="ignore") if q.exists() else ""


SRC = "".join(read(p) for p in [
    "lib/mentees.js", "lib/fall-cohort.js", "lib/fall-mentors.js",
    "lib/summer-mentors.js", "lib/expert-speakers.js", "lib/uplift-alumni.js",
    "lib/past-sessions.js",
])

TEAM = {"Kennedy Loper", "MJ Durkin", "Jackie Anzaroot", "Aaron Price", "Elana Abramovitz"}

names = set()
for m in re.finditer(r'first:\s*"([^"]+)"\s*,\s*last:\s*"([^"]+)"', SRC):
    names.add(f"{m.group(1)} {m.group(2)}")
for m in re.finditer(r'name:\s*"([A-Z][\w\'À-ɏ.-]+ [A-Z][\w\'À-ɏ.-]+[^"]*)"', SRC):
    names.add(m.group(1).strip())
names = {n for n in names if n and n not in TEAM and len(n.split()) >= 2}

companies = set()
for key in ("company", "firm"):
    for m in re.finditer(key + r':\s*"([^"]{3,60})"', SRC):
        v = m.group(1).strip()
        if v and v.lower() not in {"self", "n/a", "none", "other"}:
            companies.add(v)

print(f"roster: {len(names)} names, {len(companies)} companies")

# Longest first, so "Anna-Maria Del Rio" is replaced before "Anna".
name_pairs = sorted(names, key=len, reverse=True)
company_pairs = sorted(companies, key=len, reverse=True)

MAP = {}
for real in name_pairs:
    f, l, full = synth_name(real)
    MAP[real] = full


def sanitize(text):
    hits = 0
    # Full names first.
    for real in name_pairs:
        if real in text:
            text = text.replace(real, MAP[real]); hits += 1
    # Companies.
    for real in company_pairs:
        if len(real) >= 4 and real in text:
            text = text.replace(real, synth_company(real)); hits += 1
    # Bare first and last names of roster people, on word boundaries.
    for real in name_pairs:
        rf, rl = real.split()[0], real.split()[-1]
        sf, sl = MAP[real].split()[0], MAP[real].split()[-1]
        for a, b in ((rf, sf), (rl, sl)):
            if len(a) < 3:
                continue
            new, n = re.subn(rf"\b{re.escape(a)}\b", b, text)
            if n:
                text = new; hits += n
    # Contact details and profile links.
    text = re.sub(r'\b[\w.+-]+@(?!techunited\.co)[\w.-]+\.\w{2,}', 'founder@example.com', text)
    text = re.sub(r'(linkedin\.com/in/)[\w%-]+', r'\1invented-profile', text, flags=re.I)
    text = re.sub(r'\b(\+?1[-.\s]?)?\(?\d{3}\)?[-.\s]\d{3}[-.\s]\d{4}\b', '(555) 010-0100', text)
    return text, hits


built, failed = [], []
for src_rel, out_name in TARGETS:
    src = APP / src_rel
    if not src.exists():
        failed.append((out_name, "source missing")); continue
    clean, hits = sanitize(src.read_text(errors="ignore"))

    leaks = sorted(n for n in names if n in clean)
    if leaks:
        failed.append((out_name, f"still names {', '.join(leaks[:3])}")); continue

    banner = (
        '<div style="background:#1a1733;color:#fff;font:500 12.5px/1.5 Inter,system-ui,sans-serif;'
        'padding:9px 20px;text-align:center">'
        '<strong style="color:#c7bcff">SANITISED</strong> &middot; The real deliverable, with every '
        'participant replaced by an invented one. Design, structure and writing are untouched. '
        '<a href="../index.html" style="color:#c7bcff">back to the portfolio</a></div>')
    clean = re.sub(r'(<body[^>]*>)', r'\1' + banner, clean, count=1) if "<body" in clean else banner + clean

    (OUT / out_name).write_text(clean)
    built.append((out_name, hits))

for n, h in built:
    print(f"  {n:34s} {h:5d} substitutions")
for n, why in failed:
    print(f"  SKIPPED {n:26s} {why}")
print(f"\npublished {len(built)}, skipped {len(failed)}")
