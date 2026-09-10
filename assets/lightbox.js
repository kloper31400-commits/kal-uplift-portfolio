/* Shared lightbox for every screenshot on the site.
 *
 * Inline frames deliberately CLIP rather than scroll. They used to be
 * overflow-y:auto, which turned each one into a scroll trap: a full-page
 * capture can be twenty thousand pixels tall, so a wheel gesture over a plate
 * scrolled inside it more or less forever and the page underneath never moved.
 * Now a frame shows its top, fades out, and opening it is what lets you read it.
 */
(function () {
  const SEL = ".fr img, .shot img";

  const lb = document.createElement("div");
  lb.className = "lbx";
  lb.innerHTML =
    '<div class="lbx-bar">' +
      '<span class="lbx-cap"></span>' +
      '<span class="lbx-act">' +
        '<a class="lbx-open" target="_blank" rel="noopener">Open original</a>' +
        '<button class="lbx-x" type="button">Close &#10005;</button>' +
      '</span>' +
    '</div><div class="lbx-scroll"><img alt=""></div>';
  document.body.appendChild(lb);

  const img = lb.querySelector("img");
  const cap = lb.querySelector(".lbx-cap");
  const open = lb.querySelector(".lbx-open");
  const scroller = lb.querySelector(".lbx-scroll");

  function show(src, alt) {
    img.src = src;
    img.alt = alt || "";
    cap.textContent = alt || "";
    open.href = src;
    lb.classList.add("on");
    scroller.scrollTop = 0;
    document.documentElement.classList.add("lbx-locked");
  }
  function hide() {
    lb.classList.remove("on");
    document.documentElement.classList.remove("lbx-locked");
    img.removeAttribute("src");
  }

  document.addEventListener("click", (e) => {
    const t = e.target.closest(SEL);
    if (t) { e.preventDefault(); show(t.getAttribute("src"), t.getAttribute("alt")); return; }
    if (e.target.closest(".lbx-x")) { hide(); return; }
    // Clicking the backdrop closes; clicking the image itself does not.
    if (e.target === lb || e.target === scroller) hide();
  });

  document.addEventListener("keydown", (e) => {
    if (!lb.classList.contains("on")) return;
    if (e.key === "Escape") { hide(); return; }
    // Keyboard scrolling has to reach the scroller, not the locked page.
    const step = e.shiftKey ? scroller.clientHeight : 90;
    if (e.key === "ArrowDown") { scroller.scrollTop += step; e.preventDefault(); }
    if (e.key === "ArrowUp")   { scroller.scrollTop -= step; e.preventDefault(); }
    if (e.key === "PageDown")  { scroller.scrollTop += scroller.clientHeight * 0.9; e.preventDefault(); }
    if (e.key === "PageUp")    { scroller.scrollTop -= scroller.clientHeight * 0.9; e.preventDefault(); }
    if (e.key === "Home")      { scroller.scrollTop = 0; e.preventDefault(); }
    if (e.key === "End")       { scroller.scrollTop = scroller.scrollHeight; e.preventDefault(); }
  });
})();
