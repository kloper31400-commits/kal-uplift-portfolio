#!/usr/bin/env python3
"""Render the two peer session formats as standalone documents.

Hot Seat and Pitch Without a Deck were never one-pagers. They live as data in
lib/house-sessions.js and reach founders through the portal and the Luma event
page, which means the format itself, the rules of engagement and the framing
had no artefact of their own. This gives each one a document, in the same house
style as the rest of the resource library.

Content is the real copy, verbatim from the source file.

Run:  python3 make-sessions.py
"""
import html, pathlib

OUT = pathlib.Path(__file__).parent / "work"
OUT.mkdir(parents=True, exist_ok=True)

SESSIONS = [
    {
        "slug": "hot-seat",
        "n": 17,
        "icon": "🔥",
        "title": "Hot Seat",
        "tagline": "Some breakthroughs only happen when you say it out loud.",
        "format": "Working session · small-group breakouts",
        "length": "30 minutes",
        "about": "One person brings a real, pressing challenge. The group gets curious rather than "
                 "advisory, and the goal is to find the problem underneath the problem. Five minutes "
                 "on the format, then you break into small groups: decide who takes the hot seat, "
                 "they set the scene without cleaning it up, and the rest of the group digs in with "
                 "questions before anyone reaches for a fix.",
        "takeaways": [
            "A problem you have been circling, finally said out loud to people who have been there",
            "Questions that get under the problem, rather than advice you did not ask for",
            "One concrete next step, and somebody checking in on whether you took it",
        ],
        "rules": [
            "Ask good questions. Do not jump to solutions.",
            "Talk from the trenches. Lived experience beats a newsletter.",
            "Be alternative. The weird thing that worked is often the useful answer.",
            "Follow through. If you commit to something in the room, do it.",
        ],
        "whofor": "Any founder in the cohort. <b>Bring something specific enough that the group can "
                  "actually help:</b> “I cannot close customers outside my direct network” "
                  "gets you somewhere, “I need more leads” does not.",
        "note": None,
    },
    {
        "slug": "pitch-without-a-deck",
        "n": 1,
        "icon": "🎤",
        "title": "Pitch Without a Deck",
        "tagline": "The best founders can explain what they do in 60 seconds, no slides, no props, "
                   "just words. Can you?",
        "format": "Peer workshop · groups of three",
        "length": "30 minutes",
        "about": "Whether you are still shaping your idea or refining the pitch you have given a "
                 "hundred times, this session is built to sharpen the one thing that matters most: "
                 "clarity. Clarity on the problem you are solving, on who you are building for, and "
                 "on why it matters. Working in small groups of three, you pitch for 3 minutes to "
                 "fellow founders who know nothing about your company, the closest thing to a cold "
                 "audience you will find. Then you get direct, structured feedback from people who "
                 "were actually listening.",
        "takeaways": [
            "Three minutes in front of a genuinely cold audience, and what they did and did not understand",
            "Structured feedback from founders who were listening rather than waiting to talk",
            "A clearer answer to the problem, the who, and the why it matters",
        ],
        "rules": [
            "No slides. No deck. No camera. Just your voice and your story.",
            "Three minutes each, in groups of three.",
            "Feedback is structured, and it comes from people who were actually listening.",
        ],
        "whofor": "Any founder in the cohort, whether you are still shaping the idea or refining a "
                  "pitch you have given a hundred times.",
        "note": "This session was originally scheduled as an Ask Me Anything. We are swapping one of "
                "our later peer discussions for an AMA with a special guest, covering your business, "
                "the programme, and navigating New Jersey's innovation ecosystem.",
    },
]

TPL = """<!doctype html>
<html lang="en"><head><meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{title} · Uplift Session {n}</title>
<link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800&display=swap" rel="stylesheet">
<style>
  :root{{--g:linear-gradient(90deg,#5B8DEF,#9B59B6,#E91E8C);--g135:linear-gradient(135deg,#5B8DEF,#9B59B6,#E91E8C);
        --soft:#f7f6fb;--card:#fff;--border:#ece9f4;--text:#111;--muted:#888;}}
  *{{box-sizing:border-box;margin:0;padding:0}}
  body{{background:var(--soft);font-family:'Inter',system-ui,sans-serif;color:var(--text);-webkit-font-smoothing:antialiased}}
  .nav{{background:var(--card);border-bottom:1px solid var(--border);padding:0 36px;height:52px;
       display:flex;align-items:center;justify-content:space-between;font-size:13.5px}}
  .nav a{{color:var(--text);text-decoration:none;font-weight:600}}
  .nav span{{font-size:12px;color:var(--muted)}}
  .hero{{background:var(--card);border-bottom:1px solid var(--border);padding:44px 40px 46px}}
  .in{{max-width:680px;margin:0 auto}}
  .badge{{display:inline-block;padding:3px 12px;border-radius:100px;background:var(--g);color:#fff;
         font-size:10.5px;font-weight:700;margin-bottom:16px}}
  .head{{display:flex;align-items:center;gap:16px}}
  .ico{{width:52px;height:52px;border-radius:16px;background:var(--g135);flex-shrink:0;
       display:flex;align-items:center;justify-content:center;font-size:24px}}
  h1{{font-size:30px;font-weight:800;letter-spacing:-.8px}}
  .tag{{font-size:15px;color:#555;line-height:1.55;margin-top:12px;font-style:italic;max-width:56ch}}
  .meta{{display:flex;gap:8px;flex-wrap:wrap;margin-top:16px}}
  .meta span{{font-size:11.5px;font-weight:700;background:var(--soft);border:1px solid var(--border);
             border-radius:20px;padding:4px 12px;color:#5B2D8E}}
  main{{max-width:680px;margin:0 auto;padding:28px 20px 80px}}
  .card{{background:var(--card);border:1px solid var(--border);border-radius:16px;padding:22px 26px;
        margin-bottom:10px;box-shadow:0 1px 4px rgba(0,0,0,.03)}}
  .card h2{{font-size:16px;font-weight:700;margin-bottom:12px;padding-left:12px;border-left:3px solid #9B59B6}}
  .card p{{font-size:14px;color:#444;line-height:1.8}}
  .card ul{{margin:8px 0 0;padding-left:20px}}
  .card li{{font-size:13.5px;color:#444;line-height:1.75;margin-bottom:6px}}
  .rules div{{font-size:14px;font-weight:600;padding:9px 0;border-top:1px solid var(--border)}}
  .rules div:first-child{{border-top:0}}
  .note{{background:#fffaf0;border:1px solid #e3c9a0;border-radius:12px;padding:16px 20px;
        font-size:13.5px;color:#6b5a33;line-height:1.7;margin-bottom:10px}}
  .foot{{text-align:center;padding:20px 0 0;font-size:12px;color:var(--muted)}}
  .demo{{background:#1a1733;color:#fff;font-size:12.5px;padding:9px 20px;text-align:center}}
  .demo a{{color:#c7bcff}}
  @media(max-width:640px){{.hero{{padding:30px 20px 34px}}h1{{font-size:24px}}.nav{{padding:0 16px}}}}
</style></head><body>
<div class="demo">A session Uplift runs itself: the format is the programming ·
  <a href="../index.html">back to the portfolio</a></div>
<div class="nav"><a href="library.html">← All resources</a><span>Uplift · Session {n}</span></div>
<div class="hero"><div class="in">
  <span class="badge">Peer Session Format</span>
  <div class="head"><div class="ico">{icon}</div><div><h1>{title}</h1></div></div>
  <p class="tag">&ldquo;{tagline}&rdquo;</p>
  <div class="meta"><span>{fmt}</span><span>{length}</span><span>Session {n}</span></div>
</div></div>
<main>
  {note}
  <section class="card"><h2>What happens</h2><p>{about}</p></section>
  <section class="card"><h2>What you leave with</h2><ul>{takeaways}</ul></section>
  <section class="card"><h2>Rules of engagement</h2><div class="rules">{rules}</div></section>
  <section class="card"><h2>Who it is for</h2><p>{whofor}</p></section>
  <section class="card"><h2>Why this has no speaker</h2>
    <p>Some sessions have no guest and never will, because the format <em>is</em> the programming.
    Counting those as &ldquo;still needs a speaker&rdquo; overstates the work left and makes an
    empty-looking calendar out of a planned one, so the system tracks them as house sessions:
    a title, the copy that goes on the event page, and takeaways, with no bio and no one-pager
    to chase, because there is nobody to send one to.</p></section>
  <div class="foot">TechUnited NJ · Uplift · <a href="mailto:uplift@techunited.co" style="color:var(--muted)">uplift@techunited.co</a></div>
</main>
</body></html>"""

for s in SESSIONS:
    note = f'<div class="note"><b>Said out loud rather than quietly swapped.</b> {html.escape(s["note"])}</div>' if s["note"] else ""
    page = TPL.format(
        title=html.escape(s["title"]), n=s["n"], icon=s["icon"],
        tagline=html.escape(s["tagline"]), fmt=html.escape(s["format"]),
        length=html.escape(s["length"]), about=html.escape(s["about"]),
        takeaways="".join(f"<li>{html.escape(t)}</li>" for t in s["takeaways"]),
        rules="".join(f"<div>{html.escape(r)}</div>" for r in s["rules"]),
        whofor=s["whofor"], note=note)
    (OUT / f"{s['slug']}.html").write_text(page)
    print(f"  {s['slug']}.html  session {s['n']}")
