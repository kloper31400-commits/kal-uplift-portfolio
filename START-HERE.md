# Do these in order

Nothing assumed. Copy each command, paste, press Enter, wait for it to finish
before the next one.

**To open Terminal:** press `Cmd + Space`, type `Terminal`, press Enter.

---

# Part 1 · Already done

The screenshots are generated. **96 frames, 17 MB, sitting in `shots/`.** You do
not need to run anything.

If you ever re-capture frames in `uplift-app` and want them picked up:

```
python3 /Users/kennedy/uplift-portfolio/make-shots.py
```

---

# Part 2 · Look at it yourself (5 minutes)

```
open /Users/kennedy/uplift-portfolio/index.html
```

Your browser opens the portfolio. Click every link. You are checking for:

- Any screenshot that did not load
- Any name you recognise as a **real** founder, mentor or speaker
- Anything that reads wrong to you

**Two pages to read properly:**

- **The screenshot book** — all 96 screens, linked just under the three cards.
  The Founder Lookbook is the first section.
- **The speaker loop** — the fourth card under "Walk through the real thing".

If something is wrong, tell Claude now, before Part 3. Once it is on the
internet it has been on the internet.

---

# Part 3 · Put it online (5 minutes)

You already created the repo `kloper31400-commits/uplift-portfolio`.

### 3a. Send the files up

Copy this whole block as one piece:

```
cd /Users/kennedy/uplift-portfolio && git add -A && git commit -m "Portfolio" && git branch -M main && git remote add origin https://github.com/kloper31400-commits/uplift-portfolio.git && git push -u origin main
```

GitHub will ask you to sign in. A browser window opens. Approve it there.

**If it says `remote origin already exists`,** use this instead:

```
cd /Users/kennedy/uplift-portfolio && git add -A && git commit -m "Portfolio" && git push -u origin main
```

**If it says `nothing to commit`,** that is fine, it means everything is already
saved. Use this:

```
cd /Users/kennedy/uplift-portfolio && git push -u origin main
```

### 3b. Turn the website on

1. Open https://github.com/kloper31400-commits/uplift-portfolio
2. Click **Settings** (the tab across the top of the repo, not your profile menu)
3. Click **Pages** in the left sidebar
4. Under **Source**, pick **Deploy from a branch**
5. Under **Branch**, pick **main** and **/ (root)**
6. Click **Save**
7. Wait two minutes, then reload the page

Your site is live at:

### https://kloper31400-commits.github.io/uplift-portfolio/

That is the link you send people.

---

# Part 4 · Protect the things that are not backed up (15 minutes)

This is the part that actually matters for the job transfer, and it has a
deadline: the day your laptop goes back.

### 4a. There are two folders, and only one is safe

| Folder | What it is | Where it lives |
|---|---|---|
| `~/uplift-portfolio` | The public site | GitHub, after Part 3 |
| `~/uplift-archive` | Everything, 1.6 GB | **This Mac only** |

`~/uplift-archive` is the complete application: all 963 commits, every
screenshot, the one-on-one logs, the certificates, and your `.env` files with
the live credentials. **It exists in exactly one place.**

### 4b. Copy the archive somewhere personal

Plug in a personal external drive, or use a personal cloud account. Not a work
account, not a work drive. Then drag `uplift-archive` onto it, or run:

```
open /Users/kennedy
```

and copy the `uplift-archive` folder across by hand.

### 4c. Never push the archive anywhere

I removed its git remote on purpose, so there is no accidental upload. It
contains live API keys and 46 founders' private mentorship logs. Read
`ARCHIVE-README.md` inside it if you want the detail.

---

# Two decisions only you can make

### Your username is in the public URL

`kloper31400-commits` reads like a throwaway account, and it is the address you
are putting on applications. To change it:

https://github.com/settings/admin → Change username

**Do it before you share the link, or not at all.** Links you have already sent
will break.

### Tell TechUnited about the password

`pages/admin-fall.js` line 647 checks the admin console password by comparing
against the text `SporkMarcel27`, written directly in the code. That code runs
in the browser, so anyone who opens the page can read it. The same password is
in two of the capture scripts.

This is not a portfolio problem. It is a handover problem. Mention it to
whoever takes the system over so they can change it.

---

# Changing something later

Edit the file, then:

```
cd /Users/kennedy/uplift-portfolio && git add -A && git commit -m "Update" && git push
```

The live site updates about a minute later.

If you ever re-run the collector after changing the source repo:

```
cd /Users/kennedy/uplift-portfolio && python3 collect-everything.py
```

It re-reads all 235 real participant names and re-sorts every file into
`work/` (published) or `private/` (never published).
