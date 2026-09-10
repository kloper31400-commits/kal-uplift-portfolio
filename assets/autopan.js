/* Slow auto-scroll on screenshot frames and embedded documents.
 *
 * A grid of full-page captures is mostly headers: every plate shows the top few
 * hundred pixels and they all look alike. Panning each one slowly through its
 * own content shows what is actually in it, and the movement is what makes the
 * grid read as a set of living screens rather than a contact sheet.
 *
 * Two kinds of pane:
 *   a scroll container   the screenshot plates, panned by scrollTop
 *   an embedded document the resource plates, panned inside the iframe itself
 *
 * Direction is chosen from whichever axis actually overflows, so the onboarding
 * deck (29 slides laid out sideways) pans across while a one-pager pans down.
 *
 * Real scrolling rather than a transform, so a wheel gesture takes over from
 * the animation instead of fighting it. Pauses on hover, only runs while the
 * plate is on screen, and does nothing for anyone who asked for reduced motion.
 */
(function () {
  if (window.matchMedia("(prefers-reduced-motion: reduce)").matches) return;

  const SPEED = 16;        // pixels per second
  const HOLD_TOP = 2000;   // ms paused at the start
  const HOLD_END = 1500;   // ms paused at the far end
  const RESUME = 4000;     // ms after a hand-scroll before resuming

  const panes = [];

  // A pane exposes a uniform interface whether it is a div or a document.
  function makePane(el) {
    const frame = el.querySelector("iframe");
    if (frame) {
      let doc = null;
      try { doc = frame.contentDocument; } catch (e) { return null; }
      if (!doc || !doc.scrollingElement) return null;
      const se = doc.scrollingElement;
      const maxY = se.scrollHeight - se.clientHeight;
      const maxX = se.scrollWidth - se.clientWidth;
      if (Math.max(maxX, maxY) < 40) return null;
      const axis = maxX > maxY ? "x" : "y";
      return {
        host: el, axis,
        max: () => axis === "x" ? se.scrollWidth - se.clientWidth
                                : se.scrollHeight - se.clientHeight,
        get: () => axis === "x" ? se.scrollLeft : se.scrollTop,
        set: v => { if (axis === "x") se.scrollLeft = v; else se.scrollTop = v; },
        target: doc,
      };
    }
    if (el.scrollHeight - el.clientHeight < 40) return null;
    return {
      host: el, axis: "y",
      max: () => el.scrollHeight - el.clientHeight,
      get: () => el.scrollTop,
      set: v => { el.scrollTop = v; },
      target: el,
    };
  }

  function register(el) {
    if (el.dataset.pan) return;
    const p = makePane(el);
    if (!p) return;
    el.dataset.pan = "1";
    p.dir = 1; p.wait = HOLD_TOP; p.visible = false; p.held = false; p.parkedAt = 0;
    const hold = () => { p.held = true; p.parkedAt = 0; };
    const release = () => { p.held = false; };
    el.addEventListener("pointerenter", hold);
    el.addEventListener("pointerleave", release);
    const park = () => { p.held = true; p.parkedAt = performance.now(); };
    el.addEventListener("wheel", park, { passive: true });
    try { p.target.addEventListener("wheel", park, { passive: true }); } catch (e) {}
    panes.push(p);
    io.observe(el);
  }

  const io = new IntersectionObserver(entries => {
    for (const e of entries) {
      const p = panes.find(x => x.host === e.target);
      if (p) p.visible = e.isIntersecting;
    }
  }, { rootMargin: "100px" });

  let last = performance.now();
  function frame(now) {
    const dt = Math.min(now - last, 60);
    last = now;
    for (const p of panes) {
      if (!p.visible) continue;
      if (p.held) {
        if (p.parkedAt && now - p.parkedAt > RESUME) { p.held = false; p.parkedAt = 0; }
        else continue;
      }
      const max = p.max();
      if (max < 40) continue;
      if (p.wait > 0) { p.wait -= dt; continue; }
      const next = p.get() + (SPEED * dt / 1000) * p.dir;
      if (next >= max) { p.set(max); p.dir = -1; p.wait = HOLD_END; }
      else if (next <= 0 && p.dir === -1) { p.set(0); p.dir = 1; p.wait = HOLD_TOP; }
      else p.set(next);
    }
    requestAnimationFrame(frame);
  }

  function scan() {
    document.querySelectorAll(".fr, .shot.tall").forEach(el => {
      register(el);
      // A heavy embedded document can finish well after the last timed scan,
      // and one of these decks is a megabyte. Rather than guessing at a delay,
      // each iframe is asked to say when it is ready.
      const f = el.querySelector("iframe");
      if (f && !el.dataset.pan && !f.dataset.waiting) {
        f.dataset.waiting = "1";
        f.addEventListener("load", () => { delete f.dataset.waiting; register(el); });
      }
    });
  }

  // Plates are built after the manifest loads and images settle later still,
  // so this re-scans rather than assuming everything exists at load.
  window.addEventListener("load", () => {
    scan();
    setTimeout(scan, 1200);
    setTimeout(scan, 3000);
    setTimeout(scan, 6000);
    // A slow connection can still be filling the grid after that.
    const late = setInterval(scan, 4000);
    setTimeout(() => clearInterval(late), 40000);
    requestAnimationFrame(frame);
  });
})();
