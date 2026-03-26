(function () {
  var COOKIE_NAME = "site_lang";
  var ONE_YEAR_SECONDS = 60 * 60 * 24 * 365;

  function setCookie(lang) {
    document.cookie =
      COOKIE_NAME +
      "=" +
      encodeURIComponent(lang) +
      "; path=/; max-age=" +
      ONE_YEAR_SECONDS +
      "; SameSite=Lax";
  }

  function setLegacyLessonLanguage(lang) {
    var googtransValue = "/en/" + lang;
    var host = window.location.hostname || "";

    try {
      window.localStorage.setItem("lessons_language", lang);
    } catch (error) {}

    document.cookie =
      "googtrans=" +
      encodeURIComponent(googtransValue) +
      "; path=/; max-age=" +
      ONE_YEAR_SECONDS +
      "; SameSite=Lax";

    if (host && host.indexOf(".") !== -1 && host !== "localhost") {
      document.cookie =
        "googtrans=" +
        encodeURIComponent(googtransValue) +
        "; path=/; domain=." +
        host +
        "; max-age=" +
        ONE_YEAR_SECONDS +
        "; SameSite=Lax";
    }
  }

  function updateButtons(activeLang) {
    document.querySelectorAll(".lang-btn[data-lang]").forEach(function (button) {
      var isActive = button.getAttribute("data-lang") === activeLang;
      button.classList.toggle("is-active", isActive);
      button.setAttribute("aria-pressed", isActive ? "true" : "false");
    });
  }

  document.addEventListener("DOMContentLoaded", function () {
    var activeLang = document.documentElement.getAttribute("lang") || "en";
    updateButtons(activeLang);
    setLegacyLessonLanguage(activeLang);

    document.querySelectorAll(".lang-btn[data-lang]").forEach(function (button) {
      button.addEventListener("click", function () {
        var nextLang = button.getAttribute("data-lang");
        if (!nextLang || nextLang === activeLang) {
          return;
        }
        setCookie(nextLang);
        setLegacyLessonLanguage(nextLang);
        window.location.reload();
      });
    });
  });
})();
