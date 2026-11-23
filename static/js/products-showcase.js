/*
 * Home page product showcase (main/_products_showcase.html).
 * Accessible tabs: click or arrow keys switch products; Home/End jump to the ends.
 * Without this script every product is listed one under another.
 */
(function () {
  "use strict";

  function activate(shell, tab, focus) {
    var tabs = shell.querySelectorAll('[role="tab"]');
    tabs.forEach(function (t) {
      var selected = t === tab;
      t.setAttribute("aria-selected", selected ? "true" : "false");
      t.tabIndex = selected ? 0 : -1;
      var panel = document.getElementById(t.getAttribute("aria-controls"));
      if (panel) {
        panel.classList.toggle("is-active", selected);
      }
    });
    if (focus) {
      tab.focus();
    }
  }

  function init(shell) {
    var tabs = Array.prototype.slice.call(shell.querySelectorAll('[role="tab"]'));
    if (!tabs.length) {
      return;
    }
    shell.classList.add("ps-ready");

    tabs.forEach(function (tab, index) {
      tab.addEventListener("click", function () {
        activate(shell, tab, false);
      });
      tab.addEventListener("keydown", function (event) {
        var next = null;
        if (event.key === "ArrowDown" || event.key === "ArrowRight") {
          next = tabs[(index + 1) % tabs.length];
        } else if (event.key === "ArrowUp" || event.key === "ArrowLeft") {
          next = tabs[(index - 1 + tabs.length) % tabs.length];
        } else if (event.key === "Home") {
          next = tabs[0];
        } else if (event.key === "End") {
          next = tabs[tabs.length - 1];
        }
        if (next) {
          event.preventDefault();
          activate(shell, next, true);
          next.scrollIntoView({ block: "nearest", inline: "nearest" });
        }
      });
    });
  }

  function start() {
    document.querySelectorAll("[data-product-showcase]").forEach(init);
  }

  if (document.readyState === "loading") {
    document.addEventListener("DOMContentLoaded", start);
  } else {
    start();
  }
})();
