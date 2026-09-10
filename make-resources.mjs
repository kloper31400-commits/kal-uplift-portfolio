// Render the six /resources pages to standalone HTML for the portfolio.
//
// They are React pages, but they are data-driven: each one passes a literal
// props object to <ResourceLayout>. So rather than standing up Next to render
// them, the props are extracted from the source and rendered here with the same
// markup the component produces.
//
// Run:  node make-resources.mjs

import { readFileSync, writeFileSync, mkdirSync } from "node:fs";
import path from "node:path";

const APP = "/Users/kennedy/uplift-app";
const OUT = path.join(import.meta.dirname, "work");
mkdirSync(OUT, { recursive: true });

const PAGES = [
  "mentor-handbook", "first-meeting", "feedback-guide",
  "mentor-credibility", "nj-ecosystem", "program-schedule",
];

// Pull a balanced {...} or [...] literal starting at the given index.
function balanced(src, start, open, close) {
  let depth = 0, i = start, inStr = null, esc = false;
  for (; i < src.length; i++) {
    const c = src[i];
    if (esc) { esc = false; continue; }
    if (c === "\\") { esc = true; continue; }
    if (inStr) { if (c === inStr) inStr = null; continue; }
    if (c === '"' || c === "'" || c === "`") { inStr = c; continue; }
    if (c === open) depth++;
    else if (c === close) { depth--; if (depth === 0) return src.slice(start, i + 1); }
  }
  throw new Error("unbalanced literal");
}

function attr(src, name) {
  const m = new RegExp(`${name}=\\{?["'\`]([\\s\\S]*?)["'\`]\\}?[\\s\\n]`).exec(src);
  return m ? m[1] : "";
}

function arrayProp(src, name) {
  const at = src.indexOf(`${name}={[`);
  if (at === -1) return [];
  const lit = balanced(src, src.indexOf("[", at), "[", "]");
  // The literal is plain data: objects, strings, template strings. Safe to eval
  // here because the input is this repo's own source, not user input.
  return eval(`(${lit})`);
}

const esc = (s) => String(s ?? "")
  .replace(/&/g, "&amp;").replace(/</g, "&lt;").replace(/>/g, "&gt;");

// ResourceLayout renders **bold** and wraps 'quoted' items in an em.
const inline = (s) => esc(s)
  .replace(/\*\*(.*?)\*\*/g, "<strong>$1</strong>")
  .replace(/^&#39;(.*)&#39;$/, "<em class='q'>$1</em>")
  .replace(/^'(.*)'$/, "<em class='q'>$1</em>");

const paras = (body) => body.split("\n\n")
  .map(p => `<p>${inline(p).replace(/\n/g, "<br>")}</p>`).join("\n");

function render({ slug, icon, title, subtitle, badge, sections, timeline }) {
  const secs = sections.map(s => `
    <section class="card">
      <h2>${esc(s.heading)}</h2>
      ${s.body ? paras(s.body) : ""}
      ${s.items ? `<ul>${s.items.map(i => `<li>${inline(i)}</li>`).join("")}</ul>` : ""}
    </section>`).join("");

  const tl = timeline.length ? `
    <section class="card">
      <div class="tl">
        ${timeline.map(t => `
          <div class="ti ${t.done ? "done" : ""} ${t.active ? "active" : ""}">
            <div class="tw">${esc(t.week)} <span class="td">· ${esc(t.dates)}</span>
              ${t.active ? '<span class="now">Now</span>' : ""}</div>
            <p class="tt">${esc(t.title)}</p>
            <ul>${(t.items || []).map(i => `<li>${inline(i)}</li>`).join("")}</ul>
          </div>`).join("")}
      </div>
    </section>` : "";

  return `<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>${esc(title)} · Uplift</title>
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800&display=swap" rel="stylesheet">
<style>
  :root{--g:linear-gradient(90deg,#5B8DEF,#9B59B6,#E91E8C);--g135:linear-gradient(135deg,#5B8DEF,#9B59B6,#E91E8C);
        --soft:#f7f6fb;--card:#fff;--border:#ece9f4;--text:#111;--muted:#888;}
  *{box-sizing:border-box;margin:0;padding:0}
  body{background:var(--soft);font-family:'Inter',system-ui,sans-serif;color:var(--text);-webkit-font-smoothing:antialiased}
  .nav{background:var(--card);border-bottom:1px solid var(--border);padding:0 36px;height:52px;
       display:flex;align-items:center;justify-content:space-between;position:sticky;top:0;z-index:100;
       box-shadow:0 1px 4px rgba(0,0,0,.04);font-size:13.5px}
  .nav a{color:var(--text);text-decoration:none;font-weight:600;display:flex;gap:8px;align-items:center}
  .nav span{font-size:12px;color:var(--muted)}
  .hero{background:var(--card);border-bottom:1px solid var(--border);padding:44px 40px 48px}
  .hero-in{max-width:680px;margin:0 auto}
  .badge{display:inline-block;padding:3px 12px;border-radius:100px;background:var(--g);color:#fff;
         font-size:10.5px;font-weight:700;margin-bottom:16px}
  .head{display:flex;align-items:center;gap:16px}
  .ico{width:52px;height:52px;border-radius:16px;background:var(--g135);flex-shrink:0;
       display:flex;align-items:center;justify-content:center;font-size:24px}
  h1{font-size:30px;font-weight:800;letter-spacing:-.8px}
  .hero p{font-size:14px;color:var(--muted);line-height:1.6}
  main{max-width:680px;margin:0 auto;padding:28px 20px 80px}
  .card{background:var(--card);border:1px solid var(--border);border-radius:16px;padding:22px 26px;
        margin-bottom:10px;box-shadow:0 1px 4px rgba(0,0,0,.03)}
  .card h2{font-size:16px;font-weight:700;margin-bottom:12px;padding-left:12px;
           border-left:3px solid #9B59B6}
  .card p{font-size:14px;color:#444;line-height:1.8;margin-bottom:12px}
  .card p:last-child{margin-bottom:0}
  .card ul{margin:8px 0 0;padding-left:20px}
  .card li{font-size:13.5px;color:#444;line-height:1.75;margin-bottom:4px}
  .q{color:#5B2D8E}
  .tl{position:relative;padding-left:28px}
  .tl:before{content:"";position:absolute;left:7px;top:8px;bottom:8px;width:2px;
             background:linear-gradient(180deg,#5B8DEF,#E91E8C);border-radius:1px}
  .ti{position:relative;padding-bottom:24px}
  .ti:before{content:"";position:absolute;left:-27px;top:4px;width:16px;height:16px;border-radius:8px;
             background:var(--card);border:2px solid var(--border)}
  .ti.done:before,.ti.active:before{background:var(--g135);border:none}
  .tw{font-size:10px;font-weight:700;color:var(--muted);text-transform:uppercase;letter-spacing:.6px;margin-bottom:6px}
  .ti.active .tw{color:#9B59B6}
  .td{font-weight:400;text-transform:none;letter-spacing:0}
  .now{margin-left:8px;font-size:9.5px;font-weight:700;background:var(--g);color:#fff;border-radius:100px;padding:2px 8px}
  .tt{font-size:15px;font-weight:700;margin-bottom:8px}
  .ti.done .tt{color:var(--muted)}
  .foot{text-align:center;padding:20px 0 0;font-size:12px;color:var(--muted)}
  .foot a{color:var(--muted)}
  .demo{background:#1a1733;color:#fff;font-size:12.5px;padding:9px 20px;text-align:center}
  .demo a{color:#c7bcff}
  @media(max-width:640px){.hero{padding:30px 20px 34px}h1{font-size:24px}.nav{padding:0 16px}}
</style>
</head>
<body>
<div class="demo">Uplift programme resource, written for participants ·
  <a href="../index.html">back to the portfolio</a></div>
<div class="nav"><a href="resources-index.html"><span>←</span> All resources</a>
  <span>Uplift · TechUnited NJ</span></div>
<div class="hero"><div class="hero-in">
  <span class="badge">${esc(badge)}</span>
  <div class="head"><div class="ico">${icon}</div>
    <div><h1>${esc(title)}</h1><p>${esc(subtitle)}</p></div></div>
</div></div>
<main>${tl}${secs}
  <div class="foot">TechUnited NJ · Uplift · <a href="mailto:uplift@techunited.co">uplift@techunited.co</a></div>
</main>
</body>
</html>`;
}

const built = [];
for (const slug of PAGES) {
  const src = readFileSync(path.join(APP, "pages/resources", `${slug}.js`), "utf8");
  const meta = {
    slug,
    icon: attr(src, "icon"),
    title: attr(src, "title"),
    subtitle: attr(src, "subtitle"),
    badge: attr(src, "badge"),
    sections: arrayProp(src, "sections"),
    timeline: arrayProp(src, "timeline"),
  };
  writeFileSync(path.join(OUT, `resource-${slug}.html`), render(meta));
  built.push(meta);
  console.log(`  resource-${slug}.html  ${meta.sections.length} sections, ${meta.timeline.length} timeline steps`);
}

// Index page listing all six.
const cards = built.map(m => `
  <a class="rc" href="resource-${m.slug}.html">
    <div class="ri">${m.icon}</div>
    <div><div class="rt">${esc(m.title)}</div>
    <div class="rs">${esc(m.subtitle)}</div>
    <div class="rb">${esc(m.badge)} · ${m.sections.length || m.timeline.length} sections</div></div>
  </a>`).join("");

writeFileSync(path.join(OUT, "resources-index.html"), `<!doctype html>
<html lang="en"><head><meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>Resource Library · Uplift</title>
<link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800&display=swap" rel="stylesheet">
<style>
  *{box-sizing:border-box;margin:0;padding:0}
  body{background:#f7f6fb;font-family:'Inter',system-ui,sans-serif;color:#111;-webkit-font-smoothing:antialiased}
  .demo{background:#1a1733;color:#fff;font-size:12.5px;padding:9px 20px;text-align:center}
  .demo a{color:#c7bcff}
  .hero{background:#fff;border-bottom:1px solid #ece9f4;padding:44px 40px 46px}
  .hero-in{max-width:760px;margin:0 auto}
  .badge{display:inline-block;padding:3px 12px;border-radius:100px;
         background:linear-gradient(90deg,#5B8DEF,#9B59B6,#E91E8C);color:#fff;font-size:10.5px;font-weight:700;margin-bottom:16px}
  h1{font-size:32px;font-weight:800;letter-spacing:-.9px;margin-bottom:10px}
  .hero p{font-size:15px;color:#666;line-height:1.65;max-width:62ch}
  main{max-width:760px;margin:0 auto;padding:28px 20px 80px;display:grid;gap:10px}
  .rc{display:flex;gap:16px;align-items:flex-start;background:#fff;border:1px solid #ece9f4;border-radius:16px;
      padding:20px 24px;text-decoration:none;color:inherit;box-shadow:0 1px 4px rgba(0,0,0,.03)}
  .rc:hover{border-color:#9B59B6}
  .ri{width:46px;height:46px;border-radius:14px;flex-shrink:0;font-size:21px;
      background:linear-gradient(135deg,#5B8DEF,#9B59B6,#E91E8C);display:flex;align-items:center;justify-content:center}
  .rt{font-size:16.5px;font-weight:750;margin-bottom:3px}
  .rs{font-size:13.5px;color:#666;line-height:1.55}
  .rb{font-size:11px;font-weight:700;color:#9B59B6;text-transform:uppercase;letter-spacing:.05em;margin-top:7px}
</style></head><body>
<div class="demo">Every one of these was written for this programme rather than linked from elsewhere ·
  <a href="../index.html">back to the portfolio</a></div>
<div class="hero"><div class="hero-in">
  <span class="badge">Resource Library</span>
  <h1>Six guides, written for the programme</h1>
  <p>Mentors kept asking the same questions: what do we talk about, how do I give feedback a founder
  can actually use, what am I being checked on. Each answer became a page rather than a reply.</p>
</div></div>
<main>${cards}</main>
</body></html>`);

console.log(`  resources-index.html  ${built.length} resources`);
