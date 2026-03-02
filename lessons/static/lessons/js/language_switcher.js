(function () {
  "use strict";

  var STORAGE_KEY = "lessons_language";
  var SUPPORTED = { en: true, fr: true };
  var currentLang = "en";

  function isSupported(lang) {
    return !!SUPPORTED[lang];
  }

  function readCookie(name) {
    if (!document.cookie) return "";
    var match = document.cookie
      .split(";")
      .map(function (item) {
        return item.trim();
      })
      .find(function (item) {
        return item.indexOf(name + "=") === 0;
      });
    return match ? decodeURIComponent(match.split("=").slice(1).join("=")) : "";
  }

  function getCookieLang() {
    var value = readCookie("googtrans");
    var parts = value.split("/");
    var maybeLang = parts.length >= 3 ? parts[2] : "";
    return isSupported(maybeLang) ? maybeLang : "";
  }

  function getStoredLang() {
    try {
      var value = localStorage.getItem(STORAGE_KEY);
      return isSupported(value) ? value : "";
    } catch (error) {
      return "";
    }
  }

  function saveLang(lang) {
    try {
      localStorage.setItem(STORAGE_KEY, lang);
    } catch (error) {}
  }

  function setGoogTransCookie(lang) {
    var safeLang = isSupported(lang) ? lang : "en";
    var value = "/en/" + safeLang;
    var maxAge = 60 * 60 * 24 * 365;
    document.cookie = "googtrans=" + value + ";path=/;max-age=" + maxAge;

    var host = window.location.hostname || "";
    if (host && host.indexOf(".") !== -1 && host !== "localhost") {
      document.cookie =
        "googtrans=" +
        value +
        ";path=/;domain=." +
        host +
        ";max-age=" +
        maxAge;
    }
  }

  function ensureWidgetRoot() {
    if (document.getElementById("google_translate_element")) return;
    var root = document.createElement("div");
    root.id = "google_translate_element";
    root.style.display = "none";
    document.body.appendChild(root);
  }

  function ensureStyle() {
    if (document.getElementById("global-language-switch-style")) return;
    var style = document.createElement("style");
    style.id = "global-language-switch-style";
    style.textContent =
      ":root{--ui-top-controls-y:0.5rem;--ui-top-controls-x:max(1rem,calc((100vw - 900px) / 2 + 1rem));--ui-top-controls-z:80}" +
      ".lang-switch--floating{position:fixed;top:var(--ui-top-controls-y);right:var(--ui-top-controls-x);display:inline-flex;align-items:center;gap:.25rem;background:#fff;border:1px solid #cbd5e1;border-radius:999px;padding:.2rem;box-shadow:0 4px 12px rgba(15,23,42,.12);z-index:var(--ui-top-controls-z)}" +
      ".lang-btn{border:none;border-radius:999px;background:transparent;color:#334155;padding:.35rem .7rem;font-size:.76rem;font-weight:700;cursor:pointer;line-height:1}" +
      ".lang-btn:hover{background:#e2e8f0}" +
      ".lang-btn.is-active{background:#1d4ed8;color:#fff}" +
      ".top-bar{position:fixed!important;top:var(--ui-top-controls-y)!important;left:var(--ui-top-controls-x)!important;right:var(--ui-top-controls-x)!important;z-index:var(--ui-top-controls-z)!important}" +
      ".top-bar form{margin:0!important}" +
      ".top-bar .lang-switch{position:static!important;margin-left:auto!important}" +
      ".back-button,.back-link,.global-top-left-control{position:fixed!important;top:var(--ui-top-controls-y)!important;left:var(--ui-top-controls-x)!important;z-index:var(--ui-top-controls-z)!important;margin:0!important}" +
      ".breadcrumb{margin:0!important}" +
      "html.translated-ltr,html.translated-rtl,html,body{top:0!important;margin-top:0!important;padding-top:0!important}" +
      "body{position:static!important}" +
      ".goog-te-banner-frame.skiptranslate{display:none!important}" +
      ".goog-te-banner-frame{display:none!important}" +
      ".VIpgJd-ZVi9od-ORHb-OEVmcd{display:none!important}" +
      ".VIpgJd-ZVi9od-aZ2wEe-wOHMyf{display:none!important;height:0!important;min-height:0!important}" +
      ".skiptranslate>iframe{height:0!important;border:none!important;box-shadow:none!important}" +
      "#goog-gt-tt,.goog-te-balloon-frame,.goog-te-spinner-pos{display:none!important}" +
      "body{top:0!important}";
    document.head.appendChild(style);
  }

  function alignPageControls() {
    var breadcrumb = document.querySelector(".breadcrumb");
    if (breadcrumb) {
      var firstLink = breadcrumb.querySelector("a");
      if (firstLink) {
        firstLink.classList.add("global-top-left-control");
      }
    }
  }

  function createFloatingSwitch() {
    var wrapper = document.createElement("div");
    wrapper.className = "lang-switch lang-switch--floating";
    wrapper.setAttribute("role", "group");
    wrapper.setAttribute("aria-label", "Language switch");
    wrapper.innerHTML =
      '<button class="lang-btn" type="button" data-lang="en" aria-pressed="false">EN</button>' +
      '<button class="lang-btn" type="button" data-lang="fr" aria-pressed="false">FR</button>';
    document.body.appendChild(wrapper);
    return wrapper;
  }

  function setActive(buttons, lang) {
    buttons.forEach(function (button) {
      var isActive = button.getAttribute("data-lang") === lang;
      button.classList.toggle("is-active", isActive);
      button.setAttribute("aria-pressed", isActive ? "true" : "false");
    });
  }

  function setComboLang(lang) {
    var combo = document.querySelector(".goog-te-combo");
    if (!combo) return false;
    if (combo.value !== lang) {
      combo.value = lang;
      combo.dispatchEvent(new Event("change"));
    }
    return true;
  }

  function hideGoogleBars() {
    var selectors = [
      "iframe.goog-te-banner-frame",
      "iframe.skiptranslate",
      ".goog-te-banner-frame",
      ".goog-te-banner-frame.skiptranslate",
      ".VIpgJd-ZVi9od-ORHb-OEVmcd",
      "#goog-gt-tt",
      ".goog-te-balloon-frame",
      ".goog-te-spinner-pos",
      ".VIpgJd-ZVi9od-aZ2wEe-wOHMyf",
    ];
    selectors.forEach(function (selector) {
      var nodes = document.querySelectorAll(selector);
      nodes.forEach(function (node) {
        node.style.setProperty("display", "none", "important");
        node.style.setProperty("visibility", "hidden", "important");
        node.style.setProperty("height", "0", "important");
        node.style.setProperty("min-height", "0", "important");
        node.style.setProperty("margin", "0", "important");
        node.style.setProperty("padding", "0", "important");
        node.style.setProperty("border", "0", "important");
      });
    });

    if (document.body) {
      document.body.style.setProperty("top", "0", "important");
      document.body.style.setProperty("margin-top", "0", "important");
      document.body.style.setProperty("padding-top", "0", "important");
      document.body.style.setProperty("position", "static", "important");
    }
    if (document.documentElement) {
      document.documentElement.style.setProperty("top", "0", "important");
      document.documentElement.style.setProperty("margin-top", "0", "important");
      document.documentElement.style.setProperty("padding-top", "0", "important");
    }
  }

  function installHideObserver() {
    hideGoogleBars();
    var observer = new MutationObserver(function () {
      hideGoogleBars();
    });
    observer.observe(document.documentElement || document.body, {
      childList: true,
      subtree: true,
      attributes: true,
      attributeFilter: ["style", "class"],
    });

    var attempts = 0;
    var timer = window.setInterval(function () {
      attempts += 1;
      hideGoogleBars();
      if (attempts > 300) {
        window.clearInterval(timer);
      }
    }, 250);
  }

  function applyGoogleTranslation(lang) {
    if (lang === "en") return;
    var attempts = 0;
    var timer = window.setInterval(function () {
      attempts += 1;
      if (setComboLang(lang) || attempts > 40) {
        window.clearInterval(timer);
      }
    }, 150);
  }

  function loadGoogleTranslate(lang) {
    ensureWidgetRoot();

    window.googleTranslateElementInit = function () {
      if (!window.google || !window.google.translate || !window.google.translate.TranslateElement) {
        return;
      }
      new window.google.translate.TranslateElement(
        {
          pageLanguage: "en",
          includedLanguages: "en,fr",
          autoDisplay: false,
        },
        "google_translate_element"
      );
      applyGoogleTranslation(lang);
    };

    if (window.google && window.google.translate && window.google.translate.TranslateElement) {
      window.googleTranslateElementInit();
      return;
    }

    if (document.getElementById("google-translate-script")) return;
    var script = document.createElement("script");
    script.id = "google-translate-script";
    script.src = "https://translate.google.com/translate_a/element.js?cb=googleTranslateElementInit";
    script.async = true;
    document.head.appendChild(script);
  }

  function applyLang(lang, options) {
    var safeLang = isSupported(lang) ? lang : "en";
    currentLang = safeLang;
    saveLang(safeLang);
    setGoogTransCookie(safeLang);
    document.documentElement.lang = safeLang;

    var buttons = Array.prototype.slice.call(document.querySelectorAll(".lang-btn[data-lang]"));
    if (buttons.length) {
      setActive(buttons, safeLang);
    }

    if (safeLang !== "en") {
      loadGoogleTranslate(safeLang);
    }

    if (options && options.reload) {
      window.location.reload();
    }
  }

  function initSwitch() {
    ensureStyle();
    var wrapper = document.querySelector(".lang-switch");
    if (!wrapper) {
      wrapper = createFloatingSwitch();
    }

    var buttons = Array.prototype.slice.call(wrapper.querySelectorAll(".lang-btn[data-lang]"));
    buttons.forEach(function (button) {
      button.addEventListener("click", function () {
        var lang = button.getAttribute("data-lang");
        if (!isSupported(lang) || lang === currentLang) return;
        applyLang(lang, { reload: true });
      });
    });
  }

  function init() {
    initSwitch();
    alignPageControls();
    installHideObserver();

    var initial =
      getStoredLang() ||
      getCookieLang() ||
      (isSupported((navigator.language || "en").slice(0, 2).toLowerCase())
        ? (navigator.language || "en").slice(0, 2).toLowerCase()
        : "en");

    applyLang(initial, { reload: false });
  }

  if (document.readyState === "loading") {
    document.addEventListener("DOMContentLoaded", init);
  } else {
    init();
  }
})();
