"use strict";

// Anchors and all stages remain readable when JavaScript is unavailable.
const demoTabs = document.querySelector(".demo-tabs");
const tabs = [...demoTabs.querySelectorAll("a")];
const panels = tabs.map((tab) => document.querySelector(tab.hash));
demoTabs.setAttribute("role", "tablist");
demoTabs.parentElement.classList.add("demo-enhanced");
tabs.forEach((tab, index) => {
  tab.setAttribute("role", "tab");
  tab.setAttribute("aria-controls", panels[index].id);
  panels[index].setAttribute("role", "tabpanel");
  panels[index].setAttribute("aria-labelledby", tab.id);
  panels[index].tabIndex = 0;
});

function selectStage(index, focus = false) {
  tabs.forEach((tab, position) => {
    const selected = position === index;
    tab.setAttribute("aria-selected", String(selected));
    tab.tabIndex = selected ? 0 : -1;
    panels[position].hidden = !selected;
  });
  if (focus) tabs[index].focus();
}

tabs.forEach((tab, index) => {
  tab.addEventListener("click", (event) => {
    event.preventDefault();
    selectStage(index);
  });
  tab.addEventListener("keydown", (event) => {
    const next = {
      ArrowRight: (index + 1) % tabs.length,
      ArrowLeft: (index + tabs.length - 1) % tabs.length,
      Home: 0,
      End: tabs.length - 1,
    }[event.key];
    if (next !== undefined) {
      event.preventDefault();
      selectStage(next, true);
    }
  });
});
document.querySelectorAll(".demo-next").forEach((link) => {
  link.addEventListener("click", (event) => {
    event.preventDefault();
    selectStage(
      panels.findIndex((panel) => `#${panel.id}` === link.hash),
      true,
    );
  });
});
function selectLinkedStage() {
  const index = panels.findIndex((panel) => `#${panel.id}` === location.hash);
  if (index !== -1) selectStage(index);
}
selectStage(0);
selectLinkedStage();
window.addEventListener("hashchange", selectLinkedStage);
