(function () {
  'use strict';

  // Site search index — navigation only, no generated answers
  var SITE_SEARCH_INDEX = [
    { title: 'Home', url: 'index.html', description: 'Veteran Rights Field Manual and starting hub.', keywords: 'home start overview veteran rights' },
    { title: 'Crisis Help', url: 'help-now.html', description: '988, emergency housing, and immediate veteran assistance.', keywords: 'crisis 988 emergency suicide homeless help now' },
    { title: 'VA Claims', url: 'claims.html', description: 'VA disability claims, effective dates, evidence, and C&P exams.', keywords: 'claim disability va benefits evidence effective date compensation' },
    { title: 'Appeals', url: 'appeals.html', description: 'VA appeals: Higher-Level Review, Supplemental Claim, Board Appeal.', keywords: 'appeal denial higher level review supplemental board nod' },
    { title: 'Discharge Upgrade', url: 'discharge-upgrade.html', description: 'Discharge upgrade, DD-214 correction, and military records.', keywords: 'discharge dd214 upgrade military records drb bcgr bcnr' },
    { title: 'Housing', url: 'housing.html', description: 'Housing, eviction, homelessness, and VA homeless programs.', keywords: 'housing eviction homeless homelessness rent shelter hud vash ssaf' },
    { title: 'Employment & Money', url: 'employment-money.html', description: 'SCRA, VA debts, unemployment, and veteran income.', keywords: 'employment money scrm debt unemployment income finance' },
    { title: 'Employment Rights / USERRA', url: 'employment-rights.html', description: 'USERRA employment and reemployment rights.', keywords: 'userra employment job discrimination retaliation reemployment dol vets esgr' },
    { title: 'VA Debt', url: 'va-debt.html', description: 'VA debt, overpayments, disputes, waivers, and repayment.', keywords: 'va debt overpayment waiver debt collection dispute treasury' },
    { title: 'Family & Immigration', url: 'family-immigration.html', description: 'Military naturalization, family petitions, and deportation defense.', keywords: 'immigration citizenship family i130 i485 naturalization vawa deportation' },
    { title: 'Substance Use & Recovery', url: 'substance-use.html', description: 'VA substance use treatment and recovery options.', keywords: 'substance use recovery addiction drugs alcohol treatment va' },
    { title: 'Widows & Surviving Spouses', url: 'widows.html', description: 'DIC, SBP, CHAMPVA, education, and survivor benefits.', keywords: 'widow survivor dic sbp champva education benefits spouse' },
    { title: 'State & Local Resources', url: 'state-resources.html', description: 'State veterans affairs offices and local legal aid.', keywords: 'state resources local directory veterans affairs legal aid' },
    { title: 'Faith & Encouragement', url: 'faith-encouragement.html', description: 'Selected Psalms for veterans and families.', keywords: 'faith encouragement psalm prayer bible kjv scripture' },
    { title: 'Legal Library', url: 'legal-library.html', description: 'Legal reference language and citations for veteran advocacy.', keywords: 'legal library reference law citation language words' },
    { title: 'Toolkit', url: 'toolkit.html', description: 'Case organization, checklists, forms, and sample letters.', keywords: 'toolkit checklist timeline documents case forms letters' },
    { title: 'About / Sources', url: 'about.html', description: 'Mission, sources, and full legal disclaimer.', keywords: 'about sources disclaimer methodology contact' }
  ];

  function searchSite(query) {
    var terms = query.toLowerCase().trim().split(/\s+/).filter(Boolean);
    if (!terms.length) return [];

    return SITE_SEARCH_INDEX
      .map(function (item) {
        var haystack = [item.title, item.description, item.keywords].join(' ').toLowerCase();
        var score = 0;
        terms.forEach(function (term) {
          if (item.title.toLowerCase().indexOf(term) !== -1) score += 10;
          if (item.description.toLowerCase().indexOf(term) !== -1) score += 5;
          if (item.keywords.toLowerCase().indexOf(term) !== -1) score += 3;
        });
        return { item: item, score: score };
      })
      .filter(function (result) { return result.score > 0; })
      .sort(function (a, b) { return b.score - a.score; })
      .map(function (result) { return result.item; });
  }

  function escapeHtml(text) {
    return text.replace(/&/g, '&amp;').replace(/</g, '&lt;').replace(/>/g, '&gt;');
  }

  function renderSearchResults(results, container) {
    if (!results.length) {
      container.innerHTML = '<p class="search-empty">No matching topic found. Try another word such as housing, debt, appeal, employment, or claims.</p>';
      return;
    }

    container.innerHTML = results.map(function (item) {
      return '<a class="search-result" href="' + item.url + '"><strong>' + escapeHtml(item.title) + '</strong><span>' + escapeHtml(item.description) + '</span></a>';
    }).join('');
  }

  // Search overlay
  function initSearch() {
    var searchBtn = document.querySelector('.search-btn');
    var overlay = document.getElementById('search-overlay');
    var input = document.getElementById('search-input');
    var results = document.getElementById('search-results');
    var closeBtn = document.getElementById('search-close');
    if (!overlay || !input || !results) return;

    function openSearch() {
      overlay.classList.add('is-open');
      input.value = '';
      results.innerHTML = '<p class="search-empty">Type a topic like housing, USERRA, debt, appeal, or discharge.</p>';
      setTimeout(function () { input.focus(); }, 0);
    }

    function closeSearch() {
      overlay.classList.remove('is-open');
      if (searchBtn) searchBtn.focus();
    }

    if (searchBtn) searchBtn.addEventListener('click', openSearch);
    if (closeBtn) closeBtn.addEventListener('click', closeSearch);

    input.addEventListener('input', function () {
      renderSearchResults(searchSite(input.value), results);
    });

    input.addEventListener('keydown', function (e) {
      if (e.key === 'Escape') closeSearch();
      if (e.key === 'Enter') {
        var first = results.querySelector('.search-result');
        if (first) window.location.href = first.getAttribute('href');
      }
    });

    document.addEventListener('keydown', function (e) {
      if (
        e.key === '/' &&
        document.activeElement.tagName !== 'INPUT' &&
        document.activeElement.tagName !== 'TEXTAREA' &&
        document.activeElement.isContentEditable === false
      ) {
        e.preventDefault();
        openSearch();
      }
      if (e.key === 'Escape' && overlay.classList.contains('is-open')) {
        closeSearch();
      }
    });

    overlay.addEventListener('click', function (e) {
      if (e.target === overlay) closeSearch();
    });
  }

  // Mobile menu
  function initMenu() {
    var menuButton = document.querySelector('.menu-btn');
    var mainNav = document.getElementById('main-nav');
    var navOverlay = document.querySelector('.nav-overlay');

    if (!menuButton || !mainNav) return;

    function isOpen() {
      return menuButton.getAttribute('aria-expanded') === 'true';
    }

    function openMenu() {
      menuButton.setAttribute('aria-expanded', 'true');
      menuButton.setAttribute('aria-label', 'Close menu');
      mainNav.classList.add('is-open');
      if (navOverlay) {
        navOverlay.classList.add('is-visible');
        navOverlay.setAttribute('aria-hidden', 'false');
      }
      document.body.classList.add('menu-open');
    }

    function closeMenu() {
      menuButton.setAttribute('aria-expanded', 'false');
      menuButton.setAttribute('aria-label', 'Open menu');
      mainNav.classList.remove('is-open');
      if (navOverlay) {
        navOverlay.classList.remove('is-visible');
        navOverlay.setAttribute('aria-hidden', 'true');
      }
      document.body.classList.remove('menu-open');
    }

    menuButton.addEventListener('click', function () {
      if (isOpen()) closeMenu(); else openMenu();
    });

    if (navOverlay) navOverlay.addEventListener('click', closeMenu);

    mainNav.querySelectorAll('a').forEach(function (link) {
      link.addEventListener('click', closeMenu);
    });

    document.addEventListener('keydown', function (event) {
      if (event.key === 'Escape' && isOpen()) {
        closeMenu();
        menuButton.focus();
      }
    });

    window.addEventListener('resize', function () {
      if (window.innerWidth >= 900 && isOpen()) closeMenu();
    });
  }

  // Secure external links
  function secureExternalLinks() {
    document.querySelectorAll('a[href^="http"], a[href^="//"]').forEach(function (a) {
      if (a.getAttribute('target') === '_blank') {
        var rel = a.getAttribute('rel') || '';
        if (rel.indexOf('noopener') === -1) a.setAttribute('rel', 'noopener noreferrer');
      }
    });
  }

  function init() {
    initMenu();
    initSearch();
    initProgressiveDisclosure();
    secureExternalLinks();
  }

  if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', init);
  } else {
    init();
  }
})();

  // Runtime progressive disclosure: wrap dense section-card subsections into content-tiles
  function initProgressiveDisclosure() {
    var cards = document.querySelectorAll('main .section-card');
    cards.forEach(function(card) {
      if (card.classList.contains('action-ladder')) return;
      if (card.classList.contains('danger-box')) return;

      var h3s = Array.from(card.querySelectorAll(':scope > h3'));
      if (h3s.length < 2) return;

      h3s.forEach(function(h3, index) {
        var details = document.createElement('details');
        details.className = 'content-tile';
        if (index === 0) details.setAttribute('open', '');

        var summary = document.createElement('summary');
        var titleSpan = document.createElement('span');
        titleSpan.textContent = h3.textContent.trim();
        summary.appendChild(titleSpan);
        details.appendChild(summary);

        var body = document.createElement('div');
        body.className = 'content-tile-body';

        var sibling = h3.nextElementSibling;
        while (sibling && sibling.tagName !== 'H3') {
          var next = sibling.nextElementSibling;
          body.appendChild(sibling);
          sibling = next;
        }

        h3.parentNode.insertBefore(details, h3);
        h3.remove();
        details.appendChild(body);
      });
    });
  }

