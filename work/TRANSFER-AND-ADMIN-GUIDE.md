# Uplift App: Transfer & Admin Guide

Companion to [DEPLOY.md](DEPLOY.md), which covers a from-scratch deploy. This one is for handing off an *already-running* instance to a new machine or a new person, plus a reference for the admin/portal system as it actually works today. Written from reading the current code only. Nothing about how the app runs was changed to produce this.

---

## 1. What this system is

- Next.js 14 app, deployed on Vercel, served at `uplift.techunited.co`
- No traditional database. Google Sheets is the database, reached through a Google service account
- GitHub repo: `github.com/18kloper/uplift-app` (private)
- The repo folder on disk is ~1.3GB, but only 637 files are tracked in git. Everything else (see Section 5) is local-only data and generated output that never got committed.

---

## 2. Moving to a new machine or a new owner

1. **GitHub**: add the new person as a collaborator on `18kloper/uplift-app`, or transfer ownership for a full handoff.
2. **Vercel**: add them to the Vercel team/project so they can see env vars, domain settings, and deploy logs. This is the important one, since Vercel's dashboard is the real source of truth for secrets (more in Section 3).
3. **Clone**: `git clone https://github.com/18kloper/uplift-app.git`
4. **Install**: Node 24.x was used to build this (`node -v` on this machine says v24.18.0; Next 14.2 also runs fine on Node 18+). Then `npm install`.
5. **Env vars**: copy `.env.example` to `.env.local` and fill in real values pulled from the Vercel dashboard (Settings → Environment Variables). Don't regenerate keys unless you're intentionally rotating one.
6. **Service account file**: copy `service-account.json` directly, machine to machine. It is gitignored on purpose and will not come through `git clone`. Send it over a secure channel (password manager shared vault, encrypted zip, AirDrop), never plain email or Slack.
7. **Smoke test**: `npm run dev`, confirm it boots at `localhost:3000` and a portal URL loads.
8. **Domain**: `uplift.techunited.co` DNS lives wherever TechUnited:NJ manages DNS, not in this repo. Confirm separately who has access there.

---

## 3. Where every key and secret lives

| Variable | What it's for | Where to find/rotate it |
|---|---|---|
| `GOOGLE_SHEET_ID`, `GOOGLE_SERVICE_ACCOUNT_EMAIL`, `GOOGLE_PRIVATE_KEY` | The database. Google Cloud project `uplift-program-tracker-master`. | Google Cloud Console → IAM & Admin → Service Accounts → Keys |
| `TYPEFORM_TOKEN` | Pulls application/survey responses | Typeform → account settings → Personal tokens |
| `LUMA_API_KEY` | Event RSVP/attendance sync | Luma account settings |
| `RESEND_API_KEY` | Sends transactional email (acceptance emails, nudges) | resend.com dashboard |
| `SLACK_BOT_TOKEN` | Posts cron recaps to Slack channel `C0B3Q7WJF8C` | Slack app config for the bot |
| `CIO_API_KEY`, `CIO_SITE_ID` | Syncs mentee/mentor data into Customer.io | Customer.io account settings |
| `ANTHROPIC_API_KEY` | Powers the portal chat bot and AI features (draft-intro, prompt-themes, etc.) | console.anthropic.com |
| `ADMIN_SECRET` | Gates the ~90 one-off fix scripts under `pages/api/admin/*`, and doubles as a master override password | Not tied to a vendor. It's a string you set yourself in Vercel. |
| `PORTAL_MASTER_PASSWORD` | Master password that opens any founder/mentor portal for the team. Falls back to `ADMIN_SECRET` if unset. | Same as above, made up |
| `SETUP_SECRET` | Gates two one-time setup endpoints (`setup-sheet`, `setup-admin-tab`) for initializing a fresh spreadsheet | Only matters when standing up a new sheet from scratch |
| `LOOKBOOK_ALLOW_CONTACTS`, `LOOKBOOK_ALLOW_EDITS`, `LOOKBOOK_CONTACT_CODE`, `LOOKBOOK_EDIT_CODE` | Access codes for the fall lookbook page | Made up, set in Vercel |
| `NEXT_PUBLIC_BASE_URL`, `VERCEL_BYPASS_TOKEN` | Deployment plumbing, not vendor credentials | Vercel |

**Where they physically live:**
- Locally: `.env.local` and `service-account.json`, both gitignored, both required for `npm run dev` to fully work
- In production: Vercel dashboard → project → Settings → Environment Variables. This is what the live site actually reads.
- If `.env.local` and Vercel's values ever disagree, Vercel wins for the live site. `.env.local` only affects your own machine.

Some of these accounts (Typeform, Luma, Resend, Slack app, Customer.io) may be shared TechUnited org logins rather than Kennedy's personal ones. Ask MJ (mj@techunited.co) if a new owner needs access.

---

## 4. Admin and portals: how login works, how fixes get made

- **Founder/mentor portals** (`/[mentee-slug]`, `/mentor/[mentor-slug]`): login is the person's own Uplift ID (assigned on acceptance), or `PORTAL_MASTER_PASSWORD`/`ADMIN_SECRET` as a team override that opens any portal. Full slug list is in `lib/mentees.js` and `lib/fall-roster.js`/`lib/fall-slugs.js`.
- **`/admin`** (the summer dashboard): gated by a password typed into the page. That password is literally the word `admin`, hardcoded client-side in `pages/admin.js`. It's not real security, just a soft gate so the page isn't wide open. Don't treat it as protecting anything sensitive.
- **`/admin-fall`** (the fall dashboard): a real gate. It prompts for `ADMIN_SECRET` and sends it as a token on every API call, cached in the browser's `sessionStorage` under `uplift_admin_secret`.
- **`pages/api/admin/*.js`** (about 90 files): this is where "fixing things" actually happens. Each file is a one-off script written for a specific past problem, e.g. `confirm-jim-emilia.js`, `fix-pavan-rajesh.js`, `demote-churned-three.js`. Each checks `?token=<ADMIN_SECRET>` (or a similar header, it varies file to file, check the top of each one) before touching the sheet. They're meant to run once, via a browser URL or `curl`, and then stay in the repo as a record of what was fixed.
  - Example: `curl "https://uplift.techunited.co/api/admin/some-fix?token=YOUR_ADMIN_SECRET"`
  - This is the existing pattern: when a founder's row is stuck or a match is wrong, the fix is usually a new small file in this folder, not a button in the UI.
  - I didn't run or verify any of these while writing this guide, since the ask was to not touch logic. Treat each one as write-once. Read a script before re-running it; some may not be safe to run twice.

---

## 5. What's not in git, and has to move as files

Git tracks 637 files. The folder on disk is 1.3GB. The gap is all local-only content that was never committed:

- `service-account.json`, the real Google credential
- `typeform-responses.csv` / `.json`, raw application exports
- `session-verification-kevin-abhaya.xlsx`, `uplift-2026-completers.csv`, `uplift-2026-mentors.csv`, roster and completion data
- `one-on-one-logs/` (109 files) and `public/certificates/` (47 files), generated PDFs/HTML with founder names, likely PII
- `build/`, generated output (acceptance emails, certificates) from the `scripts/` folder
- Dozens of one-off files at the repo root (`demo-night-*`, `njeda-*`, `uplift-*.md`/`.pptx`), working documents rather than app code

None of this is recoverable from git history, it was never committed in the first place. For a full handoff, these need to move as actual files (zip and secure transfer, a shared drive, an external disk), not `git clone`.

---

## 6. One thing to check: cron jobs

`pages/api/cron/daily-recap.js`, `friday-themes.js`, and `sync-to-cio.js` each say "see vercel.json" for their schedule, but the current `vercel.json` only contains `{"framework": "nextjs"}`, no crons block. Either the schedule is set directly in the Vercel dashboard (Project → Settings → Cron Jobs) instead of the file, or it's drifted. Worth checking the dashboard directly on whatever Vercel account ends up owning this, rather than trusting the repo for it. Left as-is here since it's existing behavior, not something to change.

---

## 7. Full handoff checklist

- [ ] Add new owner to the GitHub repo
- [ ] Add new owner to the Vercel team/project
- [ ] Confirm who has DNS access for `uplift.techunited.co`
- [ ] Transfer `service-account.json` and `.env.local` values over a secure channel, not git, not plaintext chat
- [ ] Transfer the non-git data/assets from Section 5 as files
- [ ] Confirm logins for Typeform, Luma, Resend, the Slack app, Customer.io, and Anthropic; ask MJ which are shared org accounts
- [ ] Check the Vercel dashboard for the real cron schedule (Section 6)
- [ ] Know the two admin doors: `/admin` (password is `admin`, cosmetic only) and `/admin-fall` (real `ADMIN_SECRET`)
