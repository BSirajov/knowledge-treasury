(function () {
  "use strict";

  var widget = document.getElementById("researchTocWidget");

  if (window.KT_SIDEBAR_TOC_GROUPS) {
    window.KT_SIDEBAR_TOC_GROUPS.enhance();
    if (widget) {
      window.KT_SIDEBAR_TOC_GROUPS.bindPanelControls(widget);
    }
  }

  var searchInput = document.getElementById("researchSearch");
  var noResultsEl = document.getElementById("researchNoResults");
  var toggleArticlesBtn = document.getElementById("researchToggleArticles");
  var toggleCategoriesBtn = document.getElementById("researchToggleCategories");
  var progressBar = document.getElementById("researchProgressBar");
  var filterCategory = document.getElementById("filterCategory");
  var filterPeriod = document.getElementById("filterPeriod");
  var clearFilters = document.getElementById("clearFilters");
  var catalogToolbar = document.querySelector(".toolbar.catalog-toolbar");
  var tocFab = document.getElementById("researchTocFab");
  var widgetBody = widget ? widget.querySelector(".widget-body") : null;

  var entries = Array.prototype.slice.call(
    document.querySelectorAll(".research-entry:not(.research-bibliography-entry)")
  );
  var bibliographyEntry = document.querySelector(".research-bibliography-entry");
  var collapsibleEntries = Array.prototype.slice.call(
    document.querySelectorAll(".research-entry")
  );
  var categories = Array.prototype.slice.call(document.querySelectorAll(".research-category"));
  var tocEntries = Array.prototype.slice.call(document.querySelectorAll(".research-toc-entry"));
  var tocCats = Array.prototype.slice.call(
    document.querySelectorAll(".toc-group[data-toc-cat]")
  );
  var mobileMq = window.matchMedia("(max-width: 1060px)");

  var programmaticLock = false;
  var lockTimer = null;
  var scrollTick = false;
  var lastActiveId = "";

  var navLinks = widget
    ? Array.prototype.slice.call(widget.querySelectorAll('.timeline-list a[href^="#"]'))
    : [];
  var linkById = {};
  var sections = [];

  navLinks.forEach(function (a) {
    var id = a.getAttribute("href").slice(1);
    if (!id) return;
    linkById[id] = a;
    var el = document.getElementById(id);
    if (el) sections.push(el);
  });

  sections.sort(function (a, b) {
    if (a === b) return 0;
    return a.compareDocumentPosition(b) & Node.DOCUMENT_POSITION_FOLLOWING ? -1 : 1;
  });

  function normalize(text) {
    return (text || "").toLowerCase().replace(/\s+/g, " ").trim();
  }

  function stickyScrollOffset() {
    var root = document.documentElement;
    var style = window.getComputedStyle(root);
    var stack = parseFloat(style.getPropertyValue("--kt-sticky-top-stack"));
    if (!isFinite(stack) || stack <= 0) {
      stack = parseFloat(style.getPropertyValue("--kt-nav-height"));
      if (!isFinite(stack) || stack <= 0) {
        var nav = document.querySelector(".nav-strip");
        stack = nav ? nav.getBoundingClientRect().height : 86;
      }
      var crumbsH = parseFloat(style.getPropertyValue("--kt-breadcrumbs-height"));
      if (isFinite(crumbsH) && crumbsH > 0) {
        stack += crumbsH;
      } else {
        var crumbs = document.getElementById("kt-breadcrumbs");
        if (crumbs) stack += crumbs.getBoundingClientRect().height;
      }
    }
    var gap = parseFloat(style.getPropertyValue("--kt-scroll-anchor-gap"));
    if (!isFinite(gap) || gap <= 0) gap = 20;
    return Math.ceil(stack) + gap;
  }

  function activeFilterValues(id) {
    var mf = window.KT_CATALOG_MULTI_FILTER;
    if (mf) return mf.getActiveValues(id);
    var el = document.getElementById(id);
    return el && el.value ? [el.value] : [];
  }

  function updateFilterStyles() {
    ["filterCategory", "filterPeriod"].forEach(function (id) {
      var el = document.getElementById(id);
      if (!el) return;
      var wrap = el.closest(".sel-wrap");
      if (!wrap) return;
      var active = window.KT_CATALOG_MULTI_FILTER
        ? window.KT_CATALOG_MULTI_FILTER.isActive(id)
        : el.value !== "";
      wrap.classList.toggle("active", active);
    });
  }

  function syncToolbarFilterBadge() {
    if (catalogToolbar && catalogToolbar._ktSyncFilterBadge) {
      catalogToolbar._ktSyncFilterBadge();
    }
  }

  function isBibliographyEntry(entry) {
    return entry && entry.classList.contains("research-bibliography-entry");
  }

  function filterIsActive(id) {
    var mf = window.KT_CATALOG_MULTI_FILTER;
    if (mf) return mf.isActive(id);
    var el = document.getElementById(id);
    return !!(el && el.value);
  }

  function itemMatches(entry, q) {
    var mf = window.KT_CATALOG_MULTI_FILTER;
    if (isBibliographyEntry(entry)) {
      if (
        filterIsActive("filterCategory") ||
        filterIsActive("filterPeriod")
      ) {
        return true;
      }
      var bibHay = normalize(entry.getAttribute("data-search") || entry.textContent);
      if (q && bibHay.indexOf(q) === -1) return false;
      return true;
    }
    if (mf) {
      if (!mf.passesFilter("filterCategory", entry.getAttribute("data-category") || ""))
        return false;
      if (!mf.passesFilter("filterPeriod", entry.getAttribute("data-period") || ""))
        return false;
    } else {
      if (
        filterCategory &&
        filterCategory.value &&
        entry.getAttribute("data-category") !== filterCategory.value
      ) {
        return false;
      }
      if (
        filterPeriod &&
        filterPeriod.value &&
        entry.getAttribute("data-period") !== filterPeriod.value
      ) {
        return false;
      }
    }
    var hay = normalize(entry.getAttribute("data-search") || entry.textContent);
    if (q && hay.indexOf(q) === -1) return false;
    return true;
  }

  function setFilteredState(el, match) {
    el.classList.toggle("is-filtered-out", !match);
  }

  function applyFilters() {
    var q = normalize(searchInput ? searchInput.value : "");
    var filtering = !!(
      q ||
      filterIsActive("filterCategory") ||
      filterIsActive("filterPeriod")
    );
    var visible = 0;

    entries.forEach(function (entry) {
      var match = itemMatches(entry, q);
      setFilteredState(entry, match);
      if (match) visible += 1;
    });

    if (bibliographyEntry) {
      var bibMatch = itemMatches(bibliographyEntry, q);
      setFilteredState(bibliographyEntry, bibMatch);
    }

    categories.forEach(function (cat) {
      var visibleInCat = cat.querySelectorAll(".research-entry:not(.is-filtered-out)").length;
      setFilteredState(cat, visibleInCat > 0);
    });

    tocEntries.forEach(function (item) {
      var slug = item.getAttribute("data-toc-entry");
      var entry = document.getElementById(slug);
      var hidden = !entry || entry.classList.contains("is-filtered-out");
      item.classList.toggle("is-hidden", hidden);
    });

    tocCats.forEach(function (catGroup) {
      var catNum = catGroup.getAttribute("data-category");
      var related = tocEntries.filter(function (e) {
        return e.getAttribute("data-category") === catNum;
      });
      var anyVisible = related.some(function (e) {
        return !e.classList.contains("is-hidden");
      });
      catGroup.classList.toggle("is-hidden", !anyVisible);
    });

    if (noResultsEl) {
      var bibVisible =
        bibliographyEntry && !bibliographyEntry.classList.contains("is-filtered-out");
      noResultsEl.hidden = visible > 0 || bibVisible;
    }

    updateFilterStyles();
    syncToolbarFilterBadge();
    updateActiveFromScroll(true);
    updateProgress();
    refreshArticlesPanelToggles();
  }

  function clearFilterInputs() {
    if (searchInput) searchInput.value = "";
    if (window.KT_CATALOG_MULTI_FILTER) {
      window.KT_CATALOG_MULTI_FILTER.clearMany(["filterCategory", "filterPeriod"]);
      return;
    }
    if (filterCategory) filterCategory.value = "";
    if (filterPeriod) filterPeriod.value = "";
  }

  function setExpanded(entry, expanded, options) {
    options = options || {};
    var toggle = entry.querySelector(".research-entry__toggle");
    var body = entry.querySelector(".research-entry__body");
    if (!toggle || !body) return;

    entry.classList.toggle("is-expanded", expanded);
    toggle.setAttribute("aria-expanded", expanded ? "true" : "false");
    body.hidden = !expanded;

    if (options.scroll && expanded) {
      var top =
        toggle.getBoundingClientRect().top +
        (window.pageYOffset || document.documentElement.scrollTop) -
        stickyScrollOffset();
      window.scrollTo({ top: Math.max(0, Math.round(top)), behavior: "smooth" });
    }
  }

  function expandEntry(entry, options) {
    setExpanded(entry, true, options);
  }

  function collapseEntry(entry) {
    setExpanded(entry, false);
  }

  function visibleCollapsibleEntries() {
    return collapsibleEntries.filter(function (entry) {
      return !entry.classList.contains("is-filtered-out");
    });
  }

  function allVisibleEntriesExpanded() {
    var list = visibleCollapsibleEntries();
    if (!list.length) return false;
    return list.every(function (entry) {
      return entry.classList.contains("is-expanded");
    });
  }

  function visibleCategories() {
    return categories.filter(function (cat) {
      return !cat.classList.contains("is-filtered-out");
    });
  }

  function allVisibleCategoriesExpanded() {
    var list = visibleCategories();
    if (!list.length) return true;
    return list.every(function (cat) {
      return !cat.classList.contains("is-category-collapsed");
    });
  }

  function syncArticlesPanelToggle(btn, allExpanded, kind) {
    if (!btn) return;
    if (window.KT_SIDEBAR_TOC_GROUPS && window.KT_SIDEBAR_TOC_GROUPS.updateBulkActionButton) {
      window.KT_SIDEBAR_TOC_GROUPS.updateBulkActionButton(btn, allExpanded, kind);
      return;
    }
    btn.setAttribute("aria-pressed", allExpanded ? "true" : "false");
    btn.setAttribute("aria-expanded", allExpanded ? "true" : "false");
  }

  function refreshArticlesPanelToggles() {
    syncArticlesPanelToggle(toggleArticlesBtn, allVisibleEntriesExpanded(), "articles");
    syncArticlesPanelToggle(toggleCategoriesBtn, allVisibleCategoriesExpanded(), "categories");
  }

  function toggleAllArticles() {
    var expand = !allVisibleEntriesExpanded();
    visibleCollapsibleEntries().forEach(function (entry) {
      setExpanded(entry, expand);
    });
    refreshArticlesPanelToggles();
  }

  function toggleAllCategories() {
    var expand = !allVisibleCategoriesExpanded();
    visibleCategories().forEach(function (cat) {
      cat.classList.toggle("is-category-collapsed", !expand);
    });
    refreshArticlesPanelToggles();
  }

  function expandAllVisible() {
    collapsibleEntries.forEach(function (entry) {
      if (!entry.classList.contains("is-filtered-out")) {
        expandEntry(entry);
      }
    });
  }

  function collapseAll() {
    collapsibleEntries.forEach(function (entry) {
      collapseEntry(entry);
    });
  }

  function lockSpy(ms) {
    programmaticLock = true;
    clearTimeout(lockTimer);
    lockTimer = setTimeout(function () {
      programmaticLock = false;
      updateActiveFromScroll(true);
    }, ms || 900);
  }

  function clearActiveStates() {
    navLinks.forEach(function (l) {
      l.classList.remove("tl-active");
      l.removeAttribute("aria-current");
    });
  }

  function closeTocMenu() {
    if (!widget) return;
    var toggle = widget.querySelector(".events-menu-toggle");
    widget.classList.remove("events-open");
    if (toggle) toggle.setAttribute("aria-expanded", "false");
  }

  function openTocMenu() {
    if (!widget) return;
    var toggle = widget.querySelector(".events-menu-toggle");
    widget.classList.add("events-open");
    if (toggle) toggle.setAttribute("aria-expanded", "true");
  }

  function toggleTocMenu() {
    if (!widget) return;
    if (widget.classList.contains("events-open")) {
      closeTocMenu();
    } else {
      openTocMenu();
    }
  }

  function scrollSidebarLinkIntoView(link) {
    if (!widgetBody || mobileMq.matches || !link) return;
    var row = link.closest("li") || link;
    var bodyRect = widgetBody.getBoundingClientRect();
    var rowRect = row.getBoundingClientRect();
    var pad = 10;
    if (rowRect.top < bodyRect.top + pad) {
      widgetBody.scrollTop += rowRect.top - bodyRect.top - pad;
    } else if (rowRect.bottom > bodyRect.bottom - pad) {
      widgetBody.scrollTop += rowRect.bottom - bodyRect.bottom + pad;
    }
  }

  function setActive(id, options) {
    options = options || {};
    if (!id || (id === lastActiveId && !options.force)) {
      if (options.forceSidebarScroll && linkById[id]) {
        scrollSidebarLinkIntoView(linkById[id]);
      }
      return;
    }
    lastActiveId = id;
    clearActiveStates();
    var link = linkById[id];
    if (!link) return;
    link.classList.add("tl-active");
    link.setAttribute("aria-current", "true");
    if (window.KT_SIDEBAR_TOC_GROUPS) {
      window.KT_SIDEBAR_TOC_GROUPS.expandGroupContaining(link);
    }
    if (!options.skipSidebarScroll) {
      scrollSidebarLinkIntoView(link);
    }
  }

  function isSectionVisible(section) {
    if (!section || section.offsetParent === null) return false;
    if (section.classList.contains("is-filtered-out")) return false;
    return true;
  }

  function pickActiveSection() {
    if (!sections.length) return null;
    var offset = stickyScrollOffset();
    var active = null;
    var i;
    for (i = 0; i < sections.length; i += 1) {
      var section = sections[i];
      if (!isSectionVisible(section)) continue;
      var sectionTop = section.getBoundingClientRect().top;
      if (sectionTop - offset <= 2) {
        active = section;
      } else if (active) {
        break;
      }
    }
    if (active) return active;
    for (i = 0; i < sections.length; i += 1) {
      if (isSectionVisible(sections[i])) return sections[i];
    }
    return null;
  }

  function updateActiveFromScroll(force) {
    if (programmaticLock && !force) return;
    var active = pickActiveSection();
    if (active && active.id) {
      setActive(active.id, { skipSidebarScroll: false });
    }
  }

  function updateProgress() {
    if (!progressBar) return;
    var doc = document.documentElement;
    var scrollTop = window.pageYOffset || doc.scrollTop || 0;
    var height = doc.scrollHeight - doc.clientHeight;
    var ratio = height > 0 ? Math.min(1, scrollTop / height) : 0;
    progressBar.style.transform = "scaleX(" + ratio + ")";
  }

  function jumpToEntry(id) {
    var entry = document.getElementById(id);
    if (!entry) return false;
    expandEntry(entry, { scroll: false });
    var toggle = entry.querySelector(".research-entry__toggle");
    if (!toggle) return false;

    var Pos = window.KT_LANG_POSITION;
    if (Pos && Pos.scrollToAnchor) {
      return Pos.scrollToAnchor(id, false);
    }

    var top =
      toggle.getBoundingClientRect().top +
      (window.pageYOffset || document.documentElement.scrollTop) -
      stickyScrollOffset();
    window.scrollTo({ top: Math.max(0, Math.round(top)), left: 0, behavior: "auto" });
    return true;
  }

  function scrollToSection(id) {
    if (!id || !document.getElementById(id)) return;
    lockSpy(520);
    expandEntry(document.getElementById(id));
    setActive(id, { force: true, forceSidebarScroll: true });
    jumpToEntry(id);
    if (window.history && window.history.replaceState) {
      window.history.replaceState(null, "", "#" + id);
    }
    if (mobileMq.matches) closeTocMenu();
    window.requestAnimationFrame(function () {
      window.requestAnimationFrame(function () {
        setActive(id, { force: true, forceSidebarScroll: true });
      });
    });
  }

  collapsibleEntries.forEach(function (entry) {
    var toggle = entry.querySelector(".research-entry__toggle");
    if (!toggle) return;
    toggle.addEventListener("click", function () {
      var expanded = entry.classList.contains("is-expanded");
      if (expanded) {
        collapseEntry(entry);
      } else {
        expandEntry(entry, { scroll: false });
      }
      refreshArticlesPanelToggles();
    });
  });

  if (searchInput) {
    searchInput.addEventListener("input", applyFilters);
  }

  if (toggleArticlesBtn) {
    toggleArticlesBtn.addEventListener("click", toggleAllArticles);
  }

  if (toggleCategoriesBtn) {
    toggleCategoriesBtn.addEventListener("click", toggleAllCategories);
  }

  refreshArticlesPanelToggles();

  if (filterCategory) {
    filterCategory.addEventListener("change", applyFilters);
  }

  if (filterPeriod) {
    filterPeriod.addEventListener("change", applyFilters);
  }

  document.querySelectorAll(".sel-clear").forEach(function (btn) {
    btn.addEventListener("click", function () {
      if (window.KT_CATALOG_MULTI_FILTER) {
        window.KT_CATALOG_MULTI_FILTER.clear(btn.dataset.for);
      } else {
        var el = document.getElementById(btn.dataset.for);
        if (el) {
          el.value = "";
          el.dispatchEvent(new Event("change", { bubbles: true }));
        }
      }
      applyFilters();
    });
  });

  if (clearFilters) {
    clearFilters.addEventListener("click", function () {
      clearFilterInputs();
      applyFilters();
    });
  }

  if (widget) {
    var toggle = widget.querySelector(".events-menu-toggle");
    if (toggle) {
      toggle.addEventListener("click", function (e) {
        e.stopPropagation();
        toggleTocMenu();
      });
    }
    document.addEventListener("click", function (e) {
      if (!mobileMq.matches || !widget.classList.contains("events-open")) return;
      if (widget.contains(e.target)) return;
      closeTocMenu();
    });
    document.addEventListener("keydown", function (e) {
      if (e.key === "Escape") closeTocMenu();
    });
    navLinks.forEach(function (a) {
      var hrefId = a.getAttribute("href").slice(1);
      a.addEventListener("click", function (e) {
        e.preventDefault();
        scrollToSection(hrefId);
      });
    });
  }

  if (tocFab && widget) {
    tocFab.hidden = !mobileMq.matches;
    mobileMq.addEventListener("change", function () {
      tocFab.hidden = !mobileMq.matches;
      if (!mobileMq.matches) openTocMenu();
    });
    tocFab.addEventListener("click", function () {
      openTocMenu();
      if (widgetBody) widgetBody.scrollTop = 0;
    });
  }

  window.addEventListener(
    "scroll",
    function () {
      if (scrollTick) return;
      scrollTick = true;
      requestAnimationFrame(function () {
        scrollTick = false;
        updateActiveFromScroll(false);
        updateProgress();
      });
    },
    { passive: true }
  );

  window.addEventListener("resize", function () {
    updateActiveFromScroll(true);
    updateProgress();
  });

  if (window.location.hash) {
    var hashId = window.location.hash.slice(1);
    if (linkById[hashId] || document.getElementById(hashId)) {
      setTimeout(function () {
        scrollToSection(hashId);
      }, 120);
    }
  }

  applyFilters();
  updateProgress();
})();
