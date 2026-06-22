/**
 * Global site search — nav trigger, overlay modal, and search-index.json lookup.
 */
(function (window, document) {
  "use strict";

  if (window.__KT_SEARCH_INSTALLED__) return;
  window.__KT_SEARCH_INSTALLED__ = true;

  var indexEntries = null;
  var indexLoadPromise = null;
  var indexLoadDone = false;
  var indexLoadError = null;
  var focusedIndex = -1;
  var currentResults = [];
  var debounceTimer = 0;

  var FALLBACK_UI = {
    az: {
      navLabel: "Axtarış",
      navAria: "Sayt üzrə axtarış",
      overlayAria: "Qlobal axtarış",
      overlayTitle: "Bilik xəzinəsində axtarış",
      placeholder: "Profil, ixtira və ya səhifə axtarın…",
      prompt: "Axtarış üçün yazmağa başlayın",
      empty: "Nəticə tapılmadı",
      loading: "Axtarılır…",
      indexError: "Axtarış indeksi yüklənmədi. START-SITE.bat ilə saytı işə salın.",
      clear: "Təmizlə",
      clearAria: "Axtarış mətnini təmizlə",
      panelClose: "Bağla",
      panelCloseAria: "Axtarış pəncərəsini bağla",
      close: "Bağla",
      hintNav: "Keçid",
      hintOpen: "aç",
      hintClear: "təmizlə",
      hintClose: "bağla",
      types: {
        page: "Səhifə",
        profile: "Profil",
        invention: "İxtira",
      },
    },
    en: {
      navLabel: "Search",
      navAria: "Search the site",
      overlayAria: "Global search",
      overlayTitle: "Search Knowledge Treasury",
      placeholder: "Search profiles, inventions, or pages…",
      prompt: "Start typing to search",
      empty: "No results found",
      loading: "Searching…",
      indexError: "Search index could not be loaded. Run START-SITE.bat to preview locally.",
      clear: "Clear",
      clearAria: "Clear search text",
      panelClose: "Close",
      panelCloseAria: "Close search panel",
      close: "Close",
      hintNav: "Navigate",
      hintOpen: "open",
      hintClear: "clear",
      hintClose: "close",
      types: {
        page: "Page",
        profile: "Profile",
        invention: "Invention",
      },
    },
  };

  function lang() {
    var I18N = window.KT_I18N;
    return I18N ? I18N.detectLang() : document.documentElement.lang === "en" ? "en" : "az";
  }

  function uiStrings() {
    var L = lang();
    var ui = window.__KT_UI_CACHE__;
    if (ui && ui.search && ui.search[L]) return ui.search[L];
    return FALLBACK_UI[L] || FALLBACK_UI.en;
  }

  function assetRoot() {
    return document.documentElement.getAttribute("data-kt-asset-root") || "../";
  }

  function norm(text) {
    return String(text || "")
      .toLowerCase()
      .normalize("NFD")
      .replace(/[\u0300-\u036f]/g, "")
      .replace(/ə/g, "e")
      .replace(/ı/g, "i")
      .replace(/ö/g, "o")
      .replace(/ü/g, "u")
      .replace(/ş/g, "s")
      .replace(/ç/g, "c")
      .replace(/ğ/g, "g")
      .replace(/[^a-z0-9\s]/g, " ")
      .replace(/\s+/g, " ")
      .trim();
  }

  function resolveHref(storedHref, targetLang) {
    var I18N = window.KT_I18N;
    if (!storedHref) return "#";
    var az = storedHref;
    var en = storedHref;
    if (storedHref.indexOf("az/") === 0) {
      az = storedHref;
      en = "en/" + storedHref.slice(3);
    } else if (storedHref.indexOf("en/") === 0) {
      en = storedHref;
      az = "az/" + storedHref.slice(3);
    }
    if (I18N && typeof I18N.pageHref === "function") {
      return I18N.pageHref({ az: az, en: en }, targetLang);
    }
    return storedHref;
  }

  function entryForLang(entry) {
    var L = lang();
    return entry[L] || entry.en || entry.az || {};
  }

  function typeLabel(type) {
    var labels = uiStrings().types || {};
    return labels[type] || type;
  }

  function scoreEntry(entry, query) {
    var localized = entryForLang(entry);
    var title = norm(localized.title);
    var desc = norm(localized.desc);
    var tags = norm(localized.tags);
    var entryId = norm(entry.id);
    if (!query) return 0;
    if (title === query) return 120;
    if (title.indexOf(query) === 0) return 100;
    if (title.indexOf(query) >= 0) return 80;
    if (entryId.indexOf(query) >= 0) return 70;
    if (tags.indexOf(query) >= 0) return 55;
    if (desc.indexOf(query) >= 0) return 40;
    var parts = query.split(" ").filter(Boolean);
    if (!parts.length) return 0;
    var matched = 0;
    parts.forEach(function (part) {
      if (title.indexOf(part) >= 0 || tags.indexOf(part) >= 0 || desc.indexOf(part) >= 0) {
        matched += 1;
      }
    });
    return matched ? matched * 18 : 0;
  }

  function searchEntries(query) {
    if (!indexEntries || !query) return [];
    var q = norm(query);
    if (!q) return [];
    return indexEntries
      .map(function (entry) {
        return { entry: entry, score: scoreEntry(entry, q) };
      })
      .filter(function (row) {
        return row.score > 0;
      })
      .sort(function (a, b) {
        return b.score - a.score || (entryForLang(a.entry).title || "").localeCompare(entryForLang(b.entry).title || "");
      })
      .slice(0, 12)
      .map(function (row) {
        return row.entry;
      });
  }

  function ensureNavButton() {
    var existing = document.getElementById("nav-search-btn");
    if (existing) return existing;

    var inner = document.querySelector(".nav-inner");
    if (!inner) return null;

    var actions =
      (window.KT_SHELL && window.KT_SHELL.ensureNavActions && window.KT_SHELL.ensureNavActions(inner)) ||
      inner.querySelector(".nav-actions");

    var btn = document.createElement("button");
    btn.type = "button";
    btn.id = "nav-search-btn";
    btn.className = "nav-search-btn";
    var strings = uiStrings();
    btn.setAttribute("aria-label", strings.navAria);
    btn.setAttribute("title", strings.navAria);
    btn.innerHTML =
      '<span class="nav-search-btn__icon" aria-hidden="true">' +
      '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.2" stroke-linecap="round" stroke-linejoin="round">' +
      '<circle cx="11" cy="11" r="7"></circle><line x1="21" y1="21" x2="16.65" y2="16.65"></line></svg></span>' +
      '<span class="nav-search-btn__label">' +
      strings.navLabel +
      "</span>" +
      '<kbd class="nav-search-btn__kbd" aria-hidden="true">Ctrl K</kbd>';

    btn.addEventListener("click", function () {
      openSearch();
    });

    if (actions) {
      actions.insertBefore(btn, actions.firstChild);
    } else {
      inner.appendChild(btn);
    }

    document.dispatchEvent(new CustomEvent("kt-nav-tools-mounted"));
    return btn;
  }

  function escapeAttr(text) {
    return String(text)
      .replace(/&/g, "&amp;")
      .replace(/"/g, "&quot;")
      .replace(/</g, "&lt;");
  }

  function searchIconSvg() {
    return (
      '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true">' +
      '<circle cx="11" cy="11" r="7"></circle><line x1="21" y1="21" x2="16.65" y2="16.65"></line></svg>'
    );
  }

  function clearIconSvg() {
    return (
      '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.2" stroke-linecap="round" aria-hidden="true">' +
      '<line x1="18" y1="6" x2="6" y2="18"></line><line x1="6" y1="6" x2="18" y2="18"></line></svg>'
    );
  }

  function panelCloseIconSvg() {
    return (
      '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.2" stroke-linecap="round" aria-hidden="true">' +
      '<path d="M18 6L6 18M6 6l12 12"></path></svg>'
    );
  }

  function updateClearButtonVisibility() {
    var input = document.getElementById("search-input");
    var clearBtn = document.getElementById("search-clear-btn");
    if (!clearBtn) return;
    var hasText = !!(input && String(input.value || "").length);
    clearBtn.hidden = !hasText;
    clearBtn.disabled = !hasText;
  }

  function clearSearchField() {
    var input = document.getElementById("search-input");
    if (!input) return;
    input.value = "";
    focusedIndex = -1;
    currentResults = [];
    renderResultsNow("");
    updateClearButtonVisibility();
    input.focus();
  }

  function applySearchControlLabels() {
    var strings = uiStrings();
    var input = document.getElementById("search-input");
    var clearBtn = document.getElementById("search-clear-btn");
    var panelCloseBtn = document.getElementById("search-panel-close-btn");
    var title = document.querySelector(".search-modal__title");
    if (input) input.placeholder = strings.placeholder;
    if (title) title.textContent = strings.overlayTitle || strings.overlayAria;
    if (clearBtn) {
      clearBtn.setAttribute("aria-label", strings.clearAria || strings.clear);
      clearBtn.setAttribute("title", strings.clearAria || strings.clear);
    }
    if (panelCloseBtn) {
      panelCloseBtn.setAttribute("aria-label", strings.panelCloseAria || strings.panelClose);
      panelCloseBtn.setAttribute("title", (strings.panelCloseAria || strings.panelClose) + " (Esc)");
      var panelText = panelCloseBtn.querySelector(".search-panel-close-btn__text");
      if (panelText) panelText.textContent = strings.panelClose || strings.close;
    }
    updateClearButtonVisibility();
    updateHint();
  }

  function bindOverlayEvents(overlay) {
    if (!overlay || overlay.getAttribute("data-kt-search-bound") === "1") return;
    overlay.setAttribute("data-kt-search-bound", "1");

    var input = overlay.querySelector("#search-input");
    var clearBtn = overlay.querySelector("#search-clear-btn");
    var panelCloseBtn = overlay.querySelector("#search-panel-close-btn");
    if (input) {
      input.addEventListener("input", onSearchInput);
      input.addEventListener("keyup", onSearchInput);
      input.addEventListener("search", onSearchInput);
      input.addEventListener("keydown", onInputKeydown);
    }
    if (clearBtn) {
      clearBtn.addEventListener("click", function (event) {
        event.preventDefault();
        clearSearchField();
      });
    }
    if (panelCloseBtn) {
      panelCloseBtn.addEventListener("click", function (event) {
        event.preventDefault();
        closeSearch();
      });
    }
    overlay.addEventListener("click", function (event) {
      if (event.target === overlay) closeSearch();
    });

    applySearchControlLabels();
    document.dispatchEvent(new CustomEvent("kt-search-overlay-ready", { detail: { overlay: overlay } }));
  }

  function onSearchInput(event) {
    var input = event && event.target ? event.target : document.getElementById("search-input");
    if (!input) return;
    updateClearButtonVisibility();
    window.clearTimeout(debounceTimer);
    debounceTimer = window.setTimeout(function () {
      renderResults(input.value);
    }, 80);
  }

  function ensureOverlay() {
    var overlay = document.getElementById("search-overlay");
    if (overlay && !overlay.querySelector("#search-clear-btn")) {
      overlay.remove();
      overlay = null;
    }
    if (overlay) {
      bindOverlayEvents(overlay);
      return overlay;
    }

    var strings = uiStrings();
    overlay = document.createElement("div");
    overlay.id = "search-overlay";
    overlay.className = "kt-search-overlay";
    overlay.setAttribute("role", "dialog");
    overlay.setAttribute("aria-modal", "true");
    overlay.setAttribute("aria-label", strings.overlayAria);
    overlay.setAttribute("aria-hidden", "true");
    overlay.innerHTML =
      '<div class="search-modal" role="document">' +
      '<div class="search-modal__header">' +
      '<div class="search-modal__top">' +
      '<p class="search-modal__title">' +
      escapeHtml(strings.overlayTitle || strings.overlayAria) +
      "</p>" +
      '<button type="button" class="search-panel-close-btn" id="search-panel-close-btn" aria-label="' +
      escapeAttr(strings.panelCloseAria || strings.panelClose || strings.close) +
      '" title="' +
      escapeAttr((strings.panelCloseAria || strings.panelClose || strings.close) + " (Esc)") +
      '">' +
      '<span class="search-panel-close-btn__text">' +
      escapeHtml(strings.panelClose || strings.close) +
      "</span>" +
      '<kbd class="search-panel-close-btn__kbd" aria-hidden="true">Esc</kbd>' +
      '<span class="search-panel-close-btn__icon" aria-hidden="true">' +
      panelCloseIconSvg() +
      "</span>" +
      "</button>" +
      "</div>" +
      '<div class="search-input-row">' +
      '<span class="search-icon-large">' +
      searchIconSvg() +
      "</span>" +
      '<input id="search-input" type="text" inputmode="search" autocomplete="off" spellcheck="false" aria-controls="search-results" />' +
      '<button type="button" class="search-clear-btn" id="search-clear-btn" aria-label="' +
      escapeAttr(strings.clearAria || strings.clear) +
      '" title="' +
      escapeAttr(strings.clearAria || strings.clear) +
      '" hidden>' +
      clearIconSvg() +
      "</button>" +
      "</div>" +
      "</div>" +
      '<div class="search-results" id="search-results"></div>' +
      '<div class="search-hint" id="search-hint"></div>' +
      "</div>";
    document.body.appendChild(overlay);
    bindOverlayEvents(overlay);
    return overlay;
  }

  function updateHint() {
    var hint = document.getElementById("search-hint");
    if (!hint) return;
    var strings = uiStrings();
    hint.innerHTML =
      "<span><kbd>↑</kbd><kbd>↓</kbd> " +
      strings.hintNav +
      "</span>" +
      "<span><kbd>Enter</kbd> " +
      strings.hintOpen +
      "</span>" +
      "<span class=\"search-hint__clear\">" +
      strings.clear +
      " · <kbd aria-hidden=\"true\">×</kbd></span>" +
      "<span><kbd>Esc</kbd> " +
      strings.hintClose +
      "</span>";
  }

  function showResultsStatus(message, className) {
    var resultsEl = document.getElementById("search-results");
    if (!resultsEl) return;
    resultsEl.innerHTML = "";
    var el = document.createElement("div");
    el.className = className || "search-status";
    el.textContent = message;
    resultsEl.appendChild(el);
  }

  function renderResults(query) {
    var q = norm(query);
    if (q && !indexLoadDone) {
      showResultsStatus(uiStrings().loading, "search-status search-status--loading");
    }
    ensureIndexLoaded()
      .then(function () {
        renderResultsNow(query);
      })
      .catch(function () {
        renderResultsNow(query);
      });
  }

  function renderResultsNow(query) {
    var resultsEl = document.getElementById("search-results");
    if (!resultsEl) return;

    currentResults = searchEntries(query);
    focusedIndex = currentResults.length ? 0 : -1;
    resultsEl.innerHTML = "";

    if (!norm(query)) {
      var prompt = document.createElement("div");
      prompt.className = "search-prompt";
      prompt.textContent = uiStrings().prompt;
      resultsEl.appendChild(prompt);
      return;
    }

    if (indexLoadError && (!indexEntries || !indexEntries.length)) {
      var error = document.createElement("div");
      error.className = "search-empty search-empty--error";
      error.textContent = uiStrings().indexError;
      resultsEl.appendChild(error);
      return;
    }

    if (!currentResults.length) {
      var empty = document.createElement("div");
      empty.className = "search-empty";
      empty.textContent = uiStrings().empty;
      resultsEl.appendChild(empty);
      return;
    }

    currentResults.forEach(function (entry, index) {
      var localized = entryForLang(entry);
      var href = resolveHref(localized.href, lang());
      var link = document.createElement("a");
      link.className = "search-result-item" + (index === focusedIndex ? " focused" : "");
      link.href = href;
      link.setAttribute("data-search-index", String(index));
      link.innerHTML =
        '<span class="sri-icon" aria-hidden="true">' +
        (entry.icon || "📄") +
        "</span>" +
        '<span class="sri-body">' +
        '<span class="sri-title">' +
        escapeHtml(localized.title || "") +
        "</span>" +
        (localized.desc
          ? '<span class="sri-desc">' + escapeHtml(localized.desc) + "</span>"
          : "") +
        "</span>" +
        '<span class="sri-tag">' +
        escapeHtml(typeLabel(entry.type)) +
        "</span>";
      link.addEventListener("mouseenter", function () {
        setFocusedIndex(index);
      });
      resultsEl.appendChild(link);
    });
  }

  function escapeHtml(text) {
    return String(text)
      .replace(/&/g, "&amp;")
      .replace(/</g, "&lt;")
      .replace(/>/g, "&gt;")
      .replace(/"/g, "&quot;");
  }

  function setFocusedIndex(index) {
    focusedIndex = index;
    var items = document.querySelectorAll(".search-result-item");
    Array.prototype.forEach.call(items, function (item, i) {
      item.classList.toggle("focused", i === focusedIndex);
    });
    var focused = items[focusedIndex];
    if (focused && focused.scrollIntoView) {
      focused.scrollIntoView({ block: "nearest" });
    }
  }

  function openSearch() {
    if (document.body && document.body.classList.contains("kt-gateway")) return;
    var overlay = ensureOverlay();
    var input = document.getElementById("search-input");
    if (!overlay || !input) return;

    overlay.classList.add("open");
    overlay.setAttribute("aria-hidden", "false");
    applySearchControlLabels();
    ensureIndexLoaded().then(function () {
      renderResultsNow("");
    });
    window.setTimeout(function () {
      input.focus();
      input.select();
      updateClearButtonVisibility();
    }, 0);

    if (window.KT_SCROLL_LOCK && window.KT_SCROLL_LOCK.update) {
      window.KT_SCROLL_LOCK.update();
    }
    if (window.KT_NAV && window.KT_NAV.closeMobileMenu) {
      window.KT_NAV.closeMobileMenu();
    }
  }

  function closeSearch() {
    var overlay = document.getElementById("search-overlay");
    if (!overlay) return;
    var input = document.getElementById("search-input");
    if (input) input.value = "";
    overlay.classList.remove("open");
    overlay.setAttribute("aria-hidden", "true");
    focusedIndex = -1;
    currentResults = [];
    updateClearButtonVisibility();
    if (window.KT_SCROLL_LOCK && window.KT_SCROLL_LOCK.update) {
      window.KT_SCROLL_LOCK.update();
    }
    var btn = document.getElementById("nav-search-btn");
    if (btn) btn.focus();
  }

  function openFocusedResult() {
    if (focusedIndex < 0 || !currentResults[focusedIndex]) return;
    var localized = entryForLang(currentResults[focusedIndex]);
    var href = resolveHref(localized.href, lang());
    if (href && href !== "#") {
      location.assign(href);
    }
  }

  function onInputKeydown(event) {
    if (event.key === "ArrowDown") {
      event.preventDefault();
      if (!currentResults.length) return;
      setFocusedIndex(Math.min(focusedIndex + 1, currentResults.length - 1));
      return;
    }
    if (event.key === "ArrowUp") {
      event.preventDefault();
      if (!currentResults.length) return;
      setFocusedIndex(Math.max(focusedIndex - 1, 0));
      return;
    }
    if (event.key === "Enter") {
      if (focusedIndex >= 0) {
        event.preventDefault();
        openFocusedResult();
      }
      return;
    }
    if (event.key === "Escape") {
      event.preventDefault();
      closeSearch();
    }
  }

  function onDocumentKeydown(event) {
    var overlay = document.getElementById("search-overlay");
    var isOpen = overlay && overlay.classList.contains("open");
    if ((event.ctrlKey || event.metaKey) && String(event.key).toLowerCase() === "k") {
      event.preventDefault();
      if (isOpen) closeSearch();
      else openSearch();
      return;
    }
    if (isOpen && event.key === "Escape") {
      event.preventDefault();
      closeSearch();
    }
  }

  function indexUrl() {
    var I18N = window.KT_I18N;
    if (I18N && typeof I18N.i18nUrl === "function") {
      return I18N.i18nUrl("search-index.json") + "?v=1";
    }
    var root = assetRoot();
    return root + "i18n/search-index.json?v=1";
  }

  function indexScriptUrl() {
    var root = assetRoot();
    return root + "i18n/search-index.js?v=1";
  }

  function loadIndexFromScript() {
    if (window.__KT_SEARCH_INDEX__ && window.__KT_SEARCH_INDEX__.entries) {
      indexEntries = window.__KT_SEARCH_INDEX__.entries;
      return Promise.resolve(indexEntries);
    }
    if (document.querySelector('script[data-kt-search-index="1"]')) {
      return Promise.resolve(indexEntries || []);
    }
    return new Promise(function (resolve, reject) {
      var script = document.createElement("script");
      script.src = indexScriptUrl();
      script.setAttribute("data-kt-search-index", "1");
      script.onload = function () {
        indexEntries = (window.__KT_SEARCH_INDEX__ && window.__KT_SEARCH_INDEX__.entries) || [];
        resolve(indexEntries);
      };
      script.onerror = function () {
        reject(new Error("Failed to load search index script"));
      };
      document.head.appendChild(script);
    });
  }

  function fetchWithTimeout(url, ms) {
    return Promise.race([
      fetch(url),
      new Promise(function (_, reject) {
        window.setTimeout(function () {
          reject(new Error("Search index request timed out"));
        }, ms);
      }),
    ]);
  }

  function finishIndexLoad(entries, err) {
    indexEntries = Array.isArray(entries) ? entries : [];
    indexLoadDone = true;
    indexLoadError = err || null;
    return indexEntries;
  }

  function fetchIndexDirect() {
    return fetchWithTimeout(indexUrl(), 10000)
      .then(function (res) {
        if (!res.ok) throw new Error("Failed to load " + indexUrl());
        return res.json();
      })
      .then(function (data) {
        return finishIndexLoad((data && data.entries) || [], null);
      });
  }

  function loadIndex(attempt) {
    attempt = attempt || 0;

    if (window.__KT_SEARCH_INDEX__ && window.__KT_SEARCH_INDEX__.entries) {
      return Promise.resolve(finishIndexLoad(window.__KT_SEARCH_INDEX__.entries, null));
    }

    if (location.protocol === "file:") {
      return loadIndexFromScript()
        .then(function (entries) {
          return finishIndexLoad(entries, null);
        })
        .catch(function (err) {
          return finishIndexLoad([], err && err.message ? err.message : "file-protocol");
        });
    }

    var I18N = window.KT_I18N;
    var loader;
    if (I18N && typeof I18N.loadSearchIndex === "function") {
      loader = I18N.loadSearchIndex()
        .then(function (data) {
          return finishIndexLoad((data && data.entries) || [], null);
        })
        .catch(function (err) {
          console.warn("[kt-search] KT_I18N index load failed, retrying direct fetch:", err);
          return fetchIndexDirect();
        })
        .catch(function (err) {
          console.warn("[kt-search] Direct fetch failed, loading search-index.js:", err);
          return loadIndexFromScript().then(function (entries) {
            return finishIndexLoad(entries, null);
          });
        });
    } else if (attempt < 40) {
      loader = new Promise(function (resolve) {
        window.setTimeout(function () {
          resolve(loadIndex(attempt + 1));
        }, 25);
      });
    } else {
      loader = fetchIndexDirect()
        .catch(function (err) {
          console.warn("[kt-search] Direct fetch failed, loading search-index.js:", err);
          return loadIndexFromScript().then(function (entries) {
            return finishIndexLoad(entries, null);
          });
        });
    }

    return loader.catch(function (err) {
      console.warn("[kt-search] Index load failed:", err);
      return finishIndexLoad([], err && err.message ? err.message : "load-failed");
    });
  }

  function ensureIndexLoaded() {
    if (indexLoadDone) {
      return Promise.resolve(indexEntries || []);
    }
    if (!indexLoadPromise) {
      indexLoadPromise = loadIndex();
    }
    return indexLoadPromise.then(function (entries) {
      return entries || [];
    });
  }

  function cacheUi(ui) {
    if (ui) window.__KT_UI_CACHE__ = ui;
  }

  function init() {
    if (document.body && document.body.classList.contains("kt-gateway")) return;

    ensureNavButton();
    updateHint();

    var I18N = window.KT_I18N;
    var loaders = [ensureIndexLoaded()];
    if (I18N && typeof I18N.loadUi === "function") {
      loaders.push(
        I18N.loadUi().then(function (ui) {
          cacheUi(ui);
          var btn = document.getElementById("nav-search-btn");
          var strings = uiStrings();
          if (btn) {
            btn.setAttribute("aria-label", strings.navAria);
            btn.setAttribute("title", strings.navAria);
            var label = btn.querySelector(".nav-search-btn__label");
            if (label) label.textContent = strings.navLabel;
          }
          applySearchControlLabels();
        })
      );
    }

    Promise.all(loaders).catch(function () {
      /* ignore */
    });
  }

  function boot() {
    init();
    document.addEventListener("keydown", onDocumentKeydown);
    document.addEventListener("kt-primary-nav-ready", function () {
      ensureNavButton();
    });
    document.addEventListener("kt-nav-tools-mounted", function () {
      ensureNavButton();
    });
  }

  if (document.readyState === "loading") {
    document.addEventListener("DOMContentLoaded", boot);
  } else {
    boot();
  }

  window.KT_SEARCH = {
    open: openSearch,
    close: closeSearch,
    reloadIndex: function () {
      indexEntries = null;
      indexLoadPromise = null;
      indexLoadDone = false;
      indexLoadError = null;
      return loadIndex();
    },
  };
})(window, document);
