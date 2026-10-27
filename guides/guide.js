"use strict";

const copyStatus = document.querySelector(".copy-status");
document.querySelectorAll(".copy-button").forEach((button) => {
  button.addEventListener("click", async () => {
    const code = button.closest(".code-block").querySelector("code");
    try {
      await navigator.clipboard.writeText(code.textContent);
      copyStatus.textContent = `${button.getAttribute("aria-label")}: copied.`;
      button.textContent = "Copied";
      setTimeout(() => {
        button.textContent = "Copy";
      }, 2000);
    } catch {
      copyStatus.textContent =
        "Clipboard access is unavailable. Select the command text and copy it manually.";
    }
  });
});

document
  .querySelector(".print-button")
  .addEventListener("click", () => window.print());

// Indicate the current section without moving focus or changing the URL.
const headings = [...document.querySelectorAll(".guide-content h2[id]")];
const contentsLinks = [
  ...document.querySelectorAll(".guide-sidebar .toc a, .mobile-toc .toc a"),
];
let scheduled = false;
function updateCurrentSection() {
  const current =
    headings
      .filter((heading) => heading.getBoundingClientRect().top <= 160)
      .pop() || headings[0];
  for (const link of contentsLinks) {
    if (current && link.hash === `#${current.id}`) {
      link.setAttribute("aria-current", "location");
    } else {
      link.removeAttribute("aria-current");
    }
  }
  scheduled = false;
}
function scheduleSectionUpdate() {
  if (!scheduled) {
    scheduled = true;
    requestAnimationFrame(updateCurrentSection);
  }
}
window.addEventListener("scroll", scheduleSectionUpdate, { passive: true });
window.addEventListener("resize", scheduleSectionUpdate);
updateCurrentSection();
