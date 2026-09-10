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
python3 /Users/kennedy/kal-uplift-portfolio/make-shots.py
```

---

# Part 2 · Look at it yourself (5 minutes)

```
open /Users/kennedy/kal-uplift-portfolio/index.html
```

Your browser opens the portfolio. Click every link. You are checking for:

- Any screenshot that did not load
- Any name you recognise as a **real** founder, mentor or speaker
- Anything that reads wrong to you

**What to look at properly:**

- **The inventory itself** — it is the front page now. 120 frames, twelve
  sections, starting with the console. Click any frame to open it full size.
- **The three deep dives** at the bottom, under "Want to walk through more?"

The 145 images on this site are the one thing no script can check for you.
Grep proved there is not a single real participant name in any of the text.
It cannot read a face or a screenshot. Four images were pulled today for
exactly that reason, so scroll the frames with that in mind.

If something is wrong, tell Claude now, before Part 3. Once it is on the
internet it has been on the internet.

---

# Part 3 · Put it online (5 minutes)

### 3a. Rename the empty repo first (30 seconds)

The repo you made is called `uplift-portfolio`. Nothing has been pushed to it
yet, so renaming it now costs nothing and no link breaks.

1. Open https://github.com/kloper31400-commits/uplift-portfolio
2. **Settings** &rarr; the **Repository name** box at the top
3. Change it to `kal-uplift-portfolio` and click **Rename**

Everything below assumes the new name.

### 3b. Send the files up

Copy this whole block as one piece:

```
cd /Users/kennedy/kal-uplift-portfolio && git add -A && git commit -m "Portfolio" && git branch -M main && git remote add origin https://github.com/kloper31400-commits/kal-uplift-portfolio.git && git push -u origin main
```

GitHub will ask you to sign in. A browser window opens. Approve it there.

**If it says `remote origin already exists`,** use this instead:

```
cd /Users/kennedy/kal-uplift-portfolio && git add -A && git commit -m "Portfolio" && git push -u origin main
```

**If it says `nothing to commit`,** that is fine, it means everything is already
saved. Use this:

```
cd /Users/kennedy/kal-uplift-portfolio && git push -u origin main
```

### 3c. Turn the website on

1. Open https://github.com/kloper31400-commits/kal-uplift-portfolio
2. Click **Settings** (the tab across the top of the repo, not your profile menu)
3. Click **Pages** in the left sidebar
4. Under **Source**, pick **Deploy from a branch**
5. Under **Branch**, pick **main** and **/ (root)**
6. Click **Save**
7. Wait two minutes, then reload the page

Your site is live at:

### https://kloper31400-commits.github.io/kal-uplift-portfolio/

That is the link you send people.

---

# Part 4 · Protect the things that are not backed up (15 minutes)

This is your own Mac, so nothing here is on a clock. The archive is worth
copying anyway for the ordinary reason: it is 1.6 GB that exists in exactly
one place, and a dead drive would be the end of it.

### 4a. There are two folders, and only one is safe

| Folder | What it is | Where it lives |
|---|---|---|
| `~/kal-uplift-portfolio` | The public site | GitHub, after Part 3 |
| `~/kal-uplift-archive` | Everything, 1.6 GB | **This Mac only** |

`~/kal-uplift-archive` is the complete application: all 963 commits, every
screenshot, the one-on-one logs, the certificates, and your `.env` files with
the live credentials. **It exists in exactly one place.**

### 4b. Copy the archive somewhere personal

Plug in a personal external drive, or use a personal cloud account. Not a work
account, not a work drive. Then drag `kal-uplift-archive` onto it, or run:

```
open /Users/kennedy
```

and copy the `kal-uplift-archive` folder across by hand.

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

---

# Changing something later

Edit the file, then:

```
cd /Users/kennedy/kal-uplift-portfolio && git add -A && git commit -m "Update" && git push
```

The live site updates about a minute later.

If you ever re-run the collector after changing the source repo:

```
cd /Users/kennedy/kal-uplift-portfolio && python3 collect-everything.py
```

It re-reads all 235 real participant names and re-sorts every file into
`work/` (published) or `private/` (never published).
