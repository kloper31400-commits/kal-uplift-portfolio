# Uplift · portfolio

Design and engineering work for **Uplift**, TechUnited NJ's founder mentorship
programme. Two cohorts, 70 New Jersey founders, 8,000+ verified minutes of
one-to-one mentorship delivered against a state grant.

**Live site:** https://kloper31400-commits.github.io/uplift-portfolio/

Built by Kennedy Loper, 2026.

---

## What is in here

```
index.html          the portfolio itself
demo/               three working demos, synthetic data only
  founder.html        the founder portal
  mentor.html         the mentor guide
  admin.html          the admin dashboard
work/               ~50 real deliverables: one-pagers, guides, decks, print
assets/             shared stylesheet and brand assets
private/            NOT PUSHED. Participant records, kept locally.
```

## The demos

The production system runs on a private database of real founders, so it cannot
be published. `demo/` contains faithful static rebuilds of the three surfaces:
the same design system, information architecture and interactions, running on
invented people and companies.

Every founder, mentor and company in the demos is fictional. No real participant
appears anywhere in this repository.

## private/ is deliberate

This repo is public, because GitHub Pages on a free account only serves public
repositories. Anything naming a real founder, mentor or grant participant lives
in `private/` and is gitignored:

- NJEDA grant exhibits and verification forms
- Individual founder profile pages and cards
- One-on-one mentorship logs
- Match and acceptance emails with real recipients

Those files stay on the local disk. Back them up somewhere that is not this repo.

## Publishing

Push to `main`, then in the repo: **Settings → Pages → Source: Deploy from a
branch → `main` / `(root)`**. First build takes a couple of minutes.

`.nojekyll` is present so GitHub serves the files as-is rather than running them
through Jekyll.

## The original system

The production application is a Next.js app at `TechUnited-NJ/uplift-app`:
roughly 200 API routes, 38 library modules, 34 build and automation scripts,
963 commits over 15 weeks. It stays with TechUnited NJ.
