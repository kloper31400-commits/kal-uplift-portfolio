/* A small persistent index that follows you down the page.
 *
 * The home page was carrying three paragraphs of prose whose only job was to
 * tell you what you could click into. That is navigation wearing a sentence as
 * a disguise: it reads once, scrolls away, and then you are three pages deep
 * with no idea what else exists. This puts the same list somewhere it stays.
 *
 * Collapsed by default to a small tab so it never sits on top of the work.
 * Remembers whether you opened it, marks the page you are on, and gets out of
 * the way entirely on a narrow screen until you ask for it.
 */
(function () {
  const HERE = location.pathname.replace(/\/index\.html$/, "/").replace(/\/+$/, "/");
  const AT_ROOT = !/\/demo\//.test(location.pathname);
  const P = AT_ROOT ? "" : "../";

  // Sections of the home page. Reachable from anywhere: from a demo page these
  // simply carry you home and land you on the right one.
  const SECTIONS = [
    ["Walk through the real thing",  "#demos"],
    ["Six systems",                  "#systems"],
    ["Write it once",                "#writeonce"],
    ["Programme collateral",         "#collateral"],
    ["Stack and constraints",        "#how"],
    ["What is real here",            "#note"],
    ["Get in touch",                 "#contact"],
  ];

  // Same ranking as the inventory: the pieces that would work somewhere else
  // first, the programme they were built for after.
  const LINKS = [
    ["Portfolio home",        P + "index.html",              "home"],
    ["Interface inventory",   P + "demo/book.html",          "123 screens, all of it"],
    ["The programme console", P + "demo/book.html#g-console", "22 tabs, in the grid"],
    ["Why these two",         P + "demo/why-these-two.html", "the matching engine explains itself"],
    ["The speaker loop",      P + "demo/speaker-loop.html",  "one date, five systems"],
    ["The Founder Lookbook",  P + "demo/lookbook.html",      "86 pages from one form"],
    ["The comms board",       P + "demo/comms.html",         "receipt vs reconstruction"],
    ["The peer rooms",        P + "demo/cohorts.html",       "four-factor grouping"],
    ["The founder portal",    P + "demo/book.html#g-portal",  "gate to certificate"],
    ["The mentor guide",      P + "demo/mentor.html",        "one ungated page"],
    ["Everything I made",     P + "work/library.html",       "95 deliverables"],
  ];

  const css = `
    .jn { position: fixed; left: 16px; top: 92px; z-index: 300;
          font: 500 13px 'Inter', system-ui, sans-serif; }
    .jn-tab {
      display: flex; align-items: center; gap: 8px; cursor: pointer;
      background: #1a0e4f; color: #fff; border: 0; border-radius: 10px;
      padding: 9px 13px; font: 800 11.5px 'Inter', system-ui, sans-serif;
      letter-spacing: .1em; text-transform: uppercase;
      box-shadow: 0 4px 16px rgba(26,14,79,.28);
    }
    .jn-tab:hover { background: #3d2f8a; }
    .jn-tab .chev { font-size: 9px; opacity: .7; }
    .jn-panel {
      display: none; margin-top: 8px; width: 234px;
      background: #fff; border: 1px solid #e8e4f5; border-radius: 12px;
      box-shadow: 0 6px 28px rgba(26,23,51,.16); overflow: hidden;
    }
    .jn.open .jn-panel { display: block; }
    .jn-panel { max-height: min(74vh, 640px); overflow-y: auto; }
    .jn-panel .jn-h {
      font: 800 10px 'Inter', system-ui, sans-serif; letter-spacing: .12em;
      text-transform: uppercase; color: #9b8fcf;
      padding: 11px 14px 7px; position: sticky; top: 0; background: #fff;
    }
    .jn-panel .jn-h2 { border-top: 1px solid #e8e4f5; margin-top: 4px; }
    .jn-panel a.jn-sec b { font-weight: 600; font-size: 12.5px; color: #4a4060; }
    .jn-panel a.jn-sec { padding: 7px 14px; }
    .jn-panel a {
      display: block; padding: 8px 14px; text-decoration: none; color: #1a1733;
      border-top: 1px solid #f1eefa; line-height: 1.3;
    }
    .jn-panel a:hover { background: #f5f3ff; }
    .jn-panel a.on { background: #f0ecff; box-shadow: inset 3px 0 0 #5c4eb5; }
    .jn-panel a b { display: block; font-weight: 650; font-size: 13px; }
    .jn-panel a i { display: block; font-style: normal; font-size: 11px; color: #6b6480; margin-top: 1px; }
    @media (max-width: 1180px) { .jn { top: auto; bottom: 16px; } .jn-panel { position: absolute; bottom: 42px; } }
    @media print { .jn { display: none; } }
  `;
  const style = document.createElement("style");
  style.textContent = css;
  document.head.appendChild(style);

  const wrap = document.createElement("nav");
  wrap.className = "jn";
  wrap.setAttribute("aria-label", "Jump to another part of the portfolio");

  const btn = document.createElement("button");
  btn.className = "jn-tab";
  btn.type = "button";
  btn.innerHTML = 'Jump to <span class="chev">▼</span>';
  btn.setAttribute("aria-expanded", "false");

  const panel = document.createElement("div");
  panel.className = "jn-panel";
  const sectionRows = SECTIONS.map(([label, hash]) =>
    `<a class="jn-sec" href="${AT_ROOT ? "" : P + "index.html"}${hash}"><b>${label}</b></a>`).join("");

  panel.innerHTML =
    '<div class="jn-h">On the home page</div>' + sectionRows +
    '<div class="jn-h jn-h2">Everything you can open</div>' +
    LINKS.map(([label, href, note]) => {
      const target = href.replace(/^\.\.\//, "/").replace(/^index\.html$/, "/");
      const isHere =
        (label === "Portfolio home" && AT_ROOT && /(^\/$|index\.html$)/.test(location.pathname)) ||
        (!AT_ROOT && location.pathname.endsWith(href.replace("../", "").replace("demo/", "")));
      return `<a href="${href}"${isHere ? ' class="on" aria-current="page"' : ""}>` +
             `<b>${label}</b><i>${note}</i></a>`;
    }).join("");

  wrap.appendChild(btn);
  wrap.appendChild(panel);
  document.addEventListener("DOMContentLoaded", () => document.body.appendChild(wrap));
  if (document.readyState !== "loading") document.body.appendChild(wrap);

  function setOpen(open) {
    wrap.classList.toggle("open", open);
    btn.setAttribute("aria-expanded", String(open));
    btn.querySelector(".chev").textContent = open ? "▲" : "▼";
    try { localStorage.setItem("jn-open", open ? "1" : "0"); } catch (e) {}
  }
  btn.addEventListener("click", () => setOpen(!wrap.classList.contains("open")));
  document.addEventListener("keydown", e => { if (e.key === "Escape") setOpen(false); });
  document.addEventListener("click", e => {
    if (!wrap.contains(e.target) && wrap.classList.contains("open")) setOpen(false);
  });

  try { if (localStorage.getItem("jn-open") === "1") setOpen(true); } catch (e) {}
})();
