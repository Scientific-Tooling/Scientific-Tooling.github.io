"use strict";

const copyStatus = document.querySelector(".copy-status");
document.querySelectorAll(".copy-button").forEach((button) => {
  button.addEventListener("click", async () => {
    const code = button.closest(".code-block").querySelector("code");
    try {
      await navigator.clipboard.writeText(code.textContent);
      copyStatus.textContent = `${button.getAttribute("aria-label")}: copied.`;
      button.textContent = "Copied";
      setTimeout(() => { button.textContent = "Copy"; }, 2000);
    } catch {
      copyStatus.textContent = "Clipboard access is unavailable. Select the command text and copy it manually.";
    }
  });
});

document.querySelector(".print-button").addEventListener("click", () => window.print());
