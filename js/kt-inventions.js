(function () {
  "use strict";

  var widget = document.getElementById("inventionsArticlesWidget");

  if (window.KT_SIDEBAR_TOC_GROUPS) {
    window.KT_SIDEBAR_TOC_GROUPS.enhance();
    if (widget) {
      window.KT_SIDEBAR_TOC_GROUPS.bindPanelControls(widget);
    }
  }

  var searchInput = document.getElementById("inventionsSearch");
  var filterCategory = document.getElementById("filterCategory");
  var filterPeriod = document.getElementById("filterPeriod");
  var clearFilters = document.getElementById("clearFilters");
  var catalogToolbar = document.querySelector(".toolbar.catalog-toolbar");
  var entries = Array.prototype.slice.call(document.querySelectorAll(".inventions-entry"));
  var categories = Array.prototype.slice.call(document.querySelectorAll(".inventions-category"));
  var widgetBody = widget ? widget.querySelector(".widget-body") : null;
  var tocEntries = Array.prototype.slice.call(
    document.querySelectorAll(".inventions-toc-entry")
  );
  var tocCats = Array.prototype.slice.call(
    document.querySelectorAll(".toc-group[data-toc-cat]")
  );
  var mobileMq = window.matchMedia("(max-width: 1060px)");

  var navLinks = widget
    ? Array.prototype.slice.call(
        widget.querySelectorAll('.timeline-list a[href^="#"]')
      )
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

  var programmaticLock = false;
  var lockTimer = null;
  var scrollTick = false;
  var lastActiveId = "";

  function normalize(text) {
    return (text || "").toLowerCase().replace(/\s+/g, " ").trim();
  }

  function inferPeriodSlug(text, slug) {
    var hp = window.KT_HISTORICAL_PERIODS;
    if (hp) return hp.inferPeriodSlug(text, null, slug);
    return "modern";
  }

  function categoryNumberFromTitle(title) {
    var m = String(title || "").match(/^(\d+)/);
    return m ? m[1] : "";
  }

  function enrichEntryMetadata() {
    categories.forEach(function (cat) {
      var num = categoryNumberFromTitle(cat.getAttribute("data-category"));
      if (num) cat.setAttribute("data-category", num);
    });

    entries.forEach(function (entry) {
      var cat = entry.closest(".inventions-category");
      if (cat && !entry.getAttribute("data-category")) {
        entry.setAttribute("data-category", cat.getAttribute("data-category") || "");
      }
      var meta = entry.querySelector(".inventions-entry-meta");
        var blob = [
          entry.getAttribute("data-search") || "",
          meta ? meta.textContent : "",
        ].join(" ");
        entry.setAttribute("data-period", inferPeriodSlug(blob, entry.id || ""));
    });

    tocEntries.forEach(function (item) {
      var slug = item.getAttribute("data-toc-entry");
      var entry = slug ? document.getElementById(slug) : null;
      if (!entry) return;
      if (!item.getAttribute("data-category")) {
        item.setAttribute("data-category", entry.getAttribute("data-category") || "");
      }
      if (!item.getAttribute("data-period")) {
        item.setAttribute("data-period", entry.getAttribute("data-period") || "");
      }
    });
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

  function lockSpy(ms) {
    programmaticLock = true;
    clearTimeout(lockTimer);
    lockTimer = setTimeout(function () {
      programmaticLock = false;
      updateActiveFromScroll(true);
    }, ms || 900);
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

  function filterIsActive(id) {
    var mf = window.KT_CATALOG_MULTI_FILTER;
    if (mf) return mf.isActive(id);
    var el = document.getElementById(id);
    return !!(el && el.value);
  }

  function itemMatches(el, q) {
    var mf = window.KT_CATALOG_MULTI_FILTER;
    if (mf) {
      if (!mf.passesFilter("filterCategory", el.getAttribute("data-category") || ""))
        return false;
      if (!mf.passesFilter("filterPeriod", el.getAttribute("data-period") || ""))
        return false;
    } else {
      if (
        filterCategory &&
        filterCategory.value &&
        el.getAttribute("data-category") !== filterCategory.value
      ) {
        return false;
      }
      if (
        filterPeriod &&
        filterPeriod.value &&
        el.getAttribute("data-period") !== filterPeriod.value
      ) {
        return false;
      }
    }
    var hay = normalize(el.getAttribute("data-search") || el.textContent);
    if (q && hay.indexOf(q) === -1) return false;
    return true;
  }

  function applyFilters() {
    if (!searchInput) return;
    var q = normalize(searchInput.value);
    var filtering = !!(
      q ||
      filterIsActive("filterCategory") ||
      filterIsActive("filterPeriod")
    );

    entries.forEach(function (entry) {
      var match = itemMatches(entry, q);
      entry.classList.toggle("is-hidden", filtering && !match);
    });

    categories.forEach(function (cat) {
      var visible = cat.querySelectorAll(".inventions-entry:not(.is-hidden)").length;
      cat.classList.toggle("is-hidden", filtering && visible === 0);
    });

    tocEntries.forEach(function (item) {
      var slug = item.getAttribute("data-toc-entry");
      var entry = slug ? document.getElementById(slug) : null;
      var hidden = entry ? entry.classList.contains("is-hidden") : false;
      item.classList.toggle("is-hidden", hidden);
    });

    tocCats.forEach(function (item) {
      var slug = item.getAttribute("data-toc-cat");
      var related = tocEntries.filter(function (e) {
        return e.getAttribute("data-toc-cat") === slug;
      });
      var anyVisible = related.some(function (e) {
        return !e.classList.contains("is-hidden");
      });
      item.classList.toggle("is-hidden", !anyVisible);
    });

    updateFilterStyles();
    syncToolbarFilterBadge();
    updateActiveFromScroll(true);
    if (window.KT_SIDEBAR_TOC_GROUPS && widget) {
      window.KT_SIDEBAR_TOC_GROUPS.refreshArticlesSidebarButtons(widget);
    }
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

  function clearActiveStates() {
    navLinks.forEach(function (l) {
      l.classList.remove("tl-active");
      l.removeAttribute("aria-current");
    });
    tocCats.forEach(function (row) {
      row.classList.remove("toc-active");
    });
  }

  function closeEventsMenu() {
    if (!widget) return;
    var toggle = widget.querySelector(".events-menu-toggle");
    widget.classList.remove("events-open");
    if (toggle) toggle.setAttribute("aria-expanded", "false");
  }

  function toggleEventsMenu() {
    if (!widget) return;
    var toggle = widget.querySelector(".events-menu-toggle");
    var open = widget.classList.toggle("events-open");
    if (toggle) toggle.setAttribute("aria-expanded", open ? "true" : "false");
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
    var force = !!options.force;
    if (!id || (id === lastActiveId && !force)) {
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

    var li = link.closest("li");
    if (li && window.KT_SIDEBAR_TOC_GROUPS) {
      window.KT_SIDEBAR_TOC_GROUPS.expandGroupContaining(li);
    }

    if (li && li.classList.contains("inventions-toc-entry")) {
      var catSlug = li.getAttribute("data-toc-cat");
      if (catSlug) {
        var catGroup = widget.querySelector('.toc-group[data-toc-cat="' + catSlug + '"]');
        if (catGroup) catGroup.classList.add("toc-active");
      }
    }

    if (!options.skipSidebarScroll) {
      scrollSidebarLinkIntoView(link);
    }
  }

  function isSectionVisible(section) {
    if (!section || section.offsetParent === null) return false;
    if (section.classList.contains("is-hidden")) return false;
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

  function resolveScrollTarget(id) {
    var el = document.getElementById(id);
    if (!el) return null;
    if (el.classList.contains("inventions-entry")) {
      return el.querySelector(".inventions-entry-title") || el;
    }
    if (el.classList.contains("inventions-category")) {
      return el.querySelector(".inventions-category-head") || el;
    }
    return el.querySelector("h2, h1") || el;
  }

  function jumpToTarget(id) {
    var target = resolveScrollTarget(id);
    if (!target) return false;

    var Pos = window.KT_LANG_POSITION;
    if (Pos && Pos.scrollToAnchor) {
      return Pos.scrollToAnchor(id, false);
    }

    var root = document.documentElement;
    var prevBehavior = root.style.scrollBehavior;
    var top =
      target.getBoundingClientRect().top +
      (window.pageYOffset || root.scrollTop || 0) -
      stickyScrollOffset();

    root.style.scrollBehavior = "auto";
    window.scrollTo({ top: Math.max(0, Math.round(top)), left: 0, behavior: "auto" });
    window.requestAnimationFrame(function () {
      root.style.scrollBehavior = prevBehavior;
    });
    return true;
  }

  function scrollToSection(id) {
    if (!id || !document.getElementById(id)) return;

    lockSpy(480);
    setActive(id, { force: true, forceSidebarScroll: true });
    jumpToTarget(id);

    if (window.history && window.history.replaceState) {
      window.history.replaceState(null, "", "#" + id);
    }

    if (mobileMq.matches) {
      closeEventsMenu();
    }

    window.requestAnimationFrame(function () {
      window.requestAnimationFrame(function () {
        setActive(id, { force: true, forceSidebarScroll: true });
      });
    });
  }

  enrichEntryMetadata();

  if (searchInput) {
    searchInput.addEventListener("input", applyFilters);
  }

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
        toggleEventsMenu();
      });
    }

    document.addEventListener("click", function (e) {
      if (!mobileMq.matches || !widget.classList.contains("events-open")) return;
      if (widget.contains(e.target)) return;
      closeEventsMenu();
    });

    document.addEventListener("keydown", function (e) {
      if (e.key === "Escape") closeEventsMenu();
    });

    navLinks.forEach(function (a) {
      var hrefId = a.getAttribute("href").slice(1);
      var row = a.closest("[data-toc-entry]");
      if (row && row.getAttribute("data-toc-entry") !== hrefId) {
        console.warn("TOC entry mismatch:", row.getAttribute("data-toc-entry"), hrefId);
      }
      if (hrefId && !document.getElementById(hrefId)) {
        console.warn("TOC link missing section:", hrefId);
      }

      a.addEventListener("click", function (e) {
        e.preventDefault();
        scrollToSection(hrefId);
      });
    });

    window.addEventListener(
      "scroll",
      function () {
        if (scrollTick) return;
        scrollTick = true;
        requestAnimationFrame(function () {
          scrollTick = false;
          updateActiveFromScroll(false);
        });
      },
      { passive: true }
    );

    window.addEventListener("resize", function () {
      updateActiveFromScroll(true);
    });

    mobileMq.addEventListener("change", function () {
      updateActiveFromScroll(true);
    });

    if (window.location.hash) {
      var hashId = window.location.hash.slice(1);
      if (linkById[hashId]) {
        setTimeout(function () {
          scrollToSection(hashId);
        }, 100);
      }
    } else {
      updateActiveFromScroll(true);
    }
  }
})();
