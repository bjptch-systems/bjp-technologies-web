/*
 * Cookie consent (PDPC compliance).
 *
 * Nothing from Google that sets cookies loads until the visitor clicks "Accept":
 *   - Google Analytics: gtag.js is only fetched after consent. The inline stub in
 *     base.html queues config/events in window.dataLayer, which gtag.js replays.
 *   - Google Maps: iframes carry data-consent-src instead of src.
 * The choice lives in localStorage; "Cookie settings" links reopen the banner.
 */
(function () {
  "use strict";

  var STORAGE_KEY = "bjp_cookie_consent";
  var ACCEPTED = "accepted";
  var REJECTED = "rejected";

  function getChoice() {
    try {
      return window.localStorage.getItem(STORAGE_KEY);
    } catch (e) {
      return null;
    }
  }

  function saveChoice(choice) {
    try {
      window.localStorage.setItem(STORAGE_KEY, choice);
    } catch (e) {
      /* Storage blocked: the choice applies to this page view only. */
    }
  }

  function loadAnalytics() {
    var id = window.BJP_GA_ID;
    if (!id || document.getElementById("bjp-gtag")) {
      return;
    }
    var script = document.createElement("script");
    script.id = "bjp-gtag";
    script.async = true;
    script.src = "https://www.googletagmanager.com/gtag/js?id=" + encodeURIComponent(id);
    document.head.appendChild(script);
  }

  function clearAnalyticsCookies() {
    var host = window.location.hostname;
    var domains = ["", host, "." + host, "." + host.replace(/^www\./, "")];
    document.cookie.split(";").forEach(function (cookie) {
      var name = cookie.split("=")[0].trim();
      if (name.indexOf("_ga") === 0) {
        domains.forEach(function (domain) {
          document.cookie =
            name + "=; expires=Thu, 01 Jan 1970 00:00:00 GMT; path=/" +
            (domain ? "; domain=" + domain : "");
        });
      }
    });
  }

  function loadMaps() {
    document.querySelectorAll("iframe[data-consent-src]").forEach(function (frame) {
      if (!frame.getAttribute("src")) {
        frame.setAttribute("src", frame.getAttribute("data-consent-src"));
      }
      frame.hidden = false;
    });
    document.querySelectorAll("[data-map-placeholder]").forEach(function (el) {
      el.hidden = true;
    });
  }

  function apply(choice) {
    if (choice === ACCEPTED) {
      loadAnalytics();
      loadMaps();
    }
  }

  function init() {
    var banner = document.getElementById("cookie-banner");
    var current = getChoice();

    if (current === ACCEPTED || current === REJECTED) {
      apply(current);
    } else if (banner) {
      banner.hidden = false;
    }

    document.querySelectorAll("[data-cookie-choice]").forEach(function (button) {
      button.addEventListener("click", function () {
        var choice = button.getAttribute("data-cookie-choice");
        var previous = getChoice();
        saveChoice(choice);
        if (banner) {
          banner.hidden = true;
        }
        if (choice === REJECTED && previous === ACCEPTED) {
          // Analytics already ran on this page: drop its cookies and reload clean.
          clearAnalyticsCookies();
          window.location.reload();
          return;
        }
        apply(choice);
      });
    });

    document.querySelectorAll("[data-cookie-settings]").forEach(function (link) {
      link.addEventListener("click", function (event) {
        event.preventDefault();
        if (banner) {
          banner.hidden = false;
          var first = banner.querySelector("button");
          if (first) {
            first.focus();
          }
        }
      });
    });

    // "Show map" counts as accepting cookies (the placeholder says so).
    document.querySelectorAll("[data-map-consent]").forEach(function (button) {
      button.addEventListener("click", function () {
        saveChoice(ACCEPTED);
        if (banner) {
          banner.hidden = true;
        }
        apply(ACCEPTED);
      });
    });
  }

  if (document.readyState === "loading") {
    document.addEventListener("DOMContentLoaded", init);
  } else {
    init();
  }
})();
