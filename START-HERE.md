# Do these four things, in order

Nothing here assumes you know git. Copy each command exactly, one at a time.

To open a Terminal: press `Cmd + Space`, type `Terminal`, press Enter.

---

## Step 1 — Make the screenshots

The portfolio shows real screenshots of your console and portal. They have to be
shrunk down for the web first. This does that.

Copy this line, paste it into Terminal, press Enter:

```
python3 /Users/kennedy/uplift-portfolio/make-shots.py
```

It takes about a minute. When it finishes it prints something like
`converted 40 of 40 frames`.

---

## Step 2 — Look at it before anyone else does

Copy, paste, Enter:

```
open /Users/kennedy/uplift-portfolio/index.html
```

That opens the portfolio in your browser. Click through it. If anything is
wrong, tell Claude before you do Step 3.

---

## Step 3 — Put it on GitHub

You already made the repo at `kloper31400-commits/uplift-portfolio`.

Copy this whole block, paste it into Terminal, press Enter:

```
cd /Users/kennedy/uplift-portfolio && git add -A && git commit -m "Portfolio" && git branch -M main && git remote add origin https://github.com/kloper31400-commits/uplift-portfolio.git && git push -u origin main
```

GitHub will ask you to sign in. A browser window opens; approve it there.

If it says `remote origin already exists`, run this instead:

```
cd /Users/kennedy/uplift-portfolio && git add -A && git commit -m "Portfolio" && git push -u origin main
```

---

## Step 4 — Turn the website on

1. Go to https://github.com/kloper31400-commits/uplift-portfolio
2. Click **Settings** (top right of the repo, not your account settings)
3. Click **Pages** in the left sidebar
4. Under **Source**, choose **Deploy from a branch**
5. Under **Branch**, choose **main** and **/ (root)**, then click **Save**
6. Wait about two minutes, then refresh the page

Your site is now live at:

**https://kloper31400-commits.github.io/uplift-portfolio/**

That is the link you send people.

---

## Two things to know

**Your username looks auto-generated.** `kloper31400-commits` is in the public
URL. If you want it to read `kennedyloper.github.io/uplift-portfolio`, change it
at https://github.com/settings/admin **before** you send the link anywhere. The
site URL updates automatically. Do it now or not at all, because links you have
already sent will break.

**The `private/` folder never gets uploaded.** It holds the one-on-one logs, the
NJEDA forms, and anything naming a real founder. Git is told to skip it. It stays
on your Mac only. Back that folder up somewhere separate, because it is not in
the repo and it is not on your work laptop forever.

---

## To change something later

Edit the file, then run:

```
cd /Users/kennedy/uplift-portfolio && git add -A && git commit -m "Update" && git push
```

The live site updates about a minute later.
