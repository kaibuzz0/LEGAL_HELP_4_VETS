(function () {
  'use strict';

  // Static section-level search index — navigation only, no generated answers
  var SITE_SEARCH_INDEX = [
    { title: 'Home', page: 'index.html', section: '', sectionId: '', description: 'Veteran Rights Field Manual and starting hub.', keywords: 'home start overview veteran rights' },
    { title: 'Help Now', page: 'help-now.html', section: '', sectionId: '', description: '988, emergency housing, and immediate veteran assistance.', keywords: 'crisis 988 emergency suicide homeless help now' },
    { title: 'VA Claims', page: 'claims.html', section: '', sectionId: '', description: 'VA disability claims, effective dates, evidence, and C&P exams.', keywords: 'claim disability va benefits evidence effective date compensation' },
    { title: 'Effective Dates', page: 'claims.html', section: 'Effective Dates', sectionId: 'effective-dates', description: 'How VA sets effective dates for disability claims.', keywords: 'effective date intent to file itf' },
    { title: 'Appeals', page: 'appeals.html', section: '', sectionId: '', description: 'VA appeals: Higher-Level Review, Supplemental Claim, Board Appeal.', keywords: 'appeal denial higher level review supplemental board nod' },
    { title: 'Higher-Level Review', page: 'appeals.html', section: 'Higher-Level Review', sectionId: 'higher-level-review', description: 'Request a fresh review of a VA decision.', keywords: 'hlr higher level review appeal' },
    { title: 'Supplemental Claim', page: 'appeals.html', section: 'Supplemental Claim', sectionId: 'supplemental-claim', description: 'Add new and relevant evidence to a VA claim.', keywords: 'supplemental claim new evidence' },
    { title: 'Board Appeal', page: 'appeals.html', section: 'Board Appeal', sectionId: 'board-appeal', description: 'Appeal to the Board of Veterans Appeals.', keywords: 'board appeal bva nod notice of disagreement' },
    { title: 'Discharge Upgrade', page: 'discharge-upgrade.html', section: '', sectionId: '', description: 'Discharge upgrade, DD-214 correction, and military records.', keywords: 'discharge dd214 upgrade military records drb bcgr bcnr' },
    { title: 'Housing', page: 'housing.html', section: '', sectionId: '', description: 'Housing, eviction, homelessness, and VA homeless programs.', keywords: 'housing eviction homeless homelessness rent shelter hud vash ssaf' },
    { title: 'Stop Eviction', page: 'housing.html', section: 'Stop Eviction', sectionId: 'stop-eviction', description: 'Steps to take if you are facing eviction.', keywords: 'eviction notice tenant landlord' },
    { title: 'VA Home Loan', page: 'housing.html', section: 'VA Home Loan', sectionId: 'va-home-loan', description: 'Trouble with a VA-backed home loan.', keywords: 'va home loan foreclosure forbearance' },
    { title: 'HUD-VASH', page: 'housing.html', section: 'HUD-VASH', sectionId: 'hud-vash', description: 'Housing vouchers for homeless veterans.', keywords: 'hud vash homeless voucher' },
    { title: 'Employment & Money', page: 'employment-money.html', section: '', sectionId: '', description: 'SCRA, VA debts, unemployment, and veteran income.', keywords: 'employment money scrm debt unemployment income finance' },
    { title: 'Employment Rights / USERRA', page: 'employment-rights.html', section: '', sectionId: '', description: 'USERRA employment and reemployment rights.', keywords: 'userra employment job discrimination retaliation reemployment dol vets esgr' },
    { title: 'Return Deadlines', page: 'employment-rights.html', section: 'Return Deadlines', sectionId: 'return-deadlines', description: 'USERRA reemployment deadlines by service length.', keywords: 'userra deadline return reemployment 90 180 days' },
    { title: 'VA Debt', page: 'va-debt.html', section: '', sectionId: '', description: 'VA debt, overpayments, disputes, waivers, and repayment.', keywords: 'va debt overpayment waiver debt collection dispute treasury' },
    { title: 'Dispute VA Debt', page: 'va-debt.html', section: 'Dispute the Debt', sectionId: 'dispute', description: 'How to dispute a VA overpayment or debt.', keywords: 'va debt dispute overpayment challenge' },
    { title: 'VA Debt Waiver', page: 'va-debt.html', section: 'Request a Waiver', sectionId: 'waiver', description: 'Request a waiver or hardship relief from VA debt.', keywords: 'va debt waiver hardship financial' },
    { title: 'Family & Immigration', page: 'family-immigration.html', section: '', sectionId: '', description: 'Military naturalization, family petitions, and deportation defense.', keywords: 'immigration citizenship family i130 i485 naturalization vawa deportation' },
    { title: 'Substance Use & Recovery', page: 'substance-use.html', section: '', sectionId: '', description: 'VA substance use treatment and recovery options.', keywords: 'substance use recovery addiction drugs alcohol treatment va' },
    { title: 'Widows & Surviving Spouses', page: 'widows.html', section: '', sectionId: '', description: 'DIC, SBP, CHAMPVA, education, and survivor benefits.', keywords: 'widow survivor dic sbp champva education benefits spouse' },
    { title: 'State & Local Resources', page: 'state-resources.html', section: '', sectionId: '', description: 'State veterans affairs offices and local legal aid.', keywords: 'state resources local directory veterans affairs legal aid' },
    { title: 'Faith & Encouragement', page: 'faith-encouragement.html', section: '', sectionId: '', description: 'Selected Psalms for veterans and families.', keywords: 'faith encouragement psalm prayer bible kjv scripture' },
    { title: 'Legal Library', page: 'legal-library.html', section: '', sectionId: '', description: 'Legal reference language and citations for veteran advocacy.', keywords: 'legal library reference law citation language words' },
    { title: 'Toolkit', page: 'toolkit.html', section: '', sectionId: '', description: 'Case organization, checklists, forms, and sample letters.', keywords: 'toolkit checklist timeline documents case forms letters' },
    { title: 'About / Sources', page: 'about.html', section: '', sectionId: '', description: 'Mission, sources, and full legal disclaimer.', keywords: 'about sources disclaimer methodology contact' }
  ];

  function searchSite(query) {
    var terms = query.toLowerCase().trim().split(/\s+/).filter(Boolean);
    if (!terms.length) return [];

    return SITE_SEARCH_INDEX
      .map(function (item) {
        var haystack = [item.title, item.section, item.description, item.keywords].join(' ').toLowerCase();
        var score = 0;
        terms.forEach(function (term) {
          if (item.section && item.section.toLowerCase().indexOf(term) !== -1) score += 12;
          else if (item.title.toLowerCase().indexOf(term) !== -1) score += 10;
          if (item.description.toLowerCase().indexOf(term) !== -1) score += 5;
          if (item.keywords.toLowerCase().indexOf(term) !== -1) score += 3;
        });
        return { item: item, score: score };
      })
      .filter(function (result) { return result.score > 0; })
      .sort(function (a, b) { return b.score - b.score; })
      .map(function (result) { return result.item; });
  }

  function escapeHtml(text) {
    return text.replace(/&/g, '&amp;').replace(/</g, '&lt;').replace(/>/g, '&gt;');
  }

  function renderSearchResults(results, container) {
    if (!results.length) {
      container.innerHTML = '<p class="search-empty">No matching topic found. Try: housing, eviction, VA debt, USERRA, appeal, or discharge.</p>';
      return;
    }

    // Deduplicate by page URL to avoid showing many sections from the same page near the top
    var seen = {};
    var unique = [];
    results.forEach(function (item) {
      var key = item.page + (item.section ? '#' + item.sectionId : '');
      if (!seen[key]) {
        seen[key] = true;
        unique.push(item);
      }
    });

    container.innerHTML = unique.slice(0, 8).map(function (item) {
      var url = item.page + (item.sectionId ? '#' + item.sectionId : '');
      var pageLabel = escapeHtml(item.title);
      var sectionLabel = item.section ? escapeHtml(item.section) : '';
      var desc = escapeHtml(item.description);
      return '<a class="search-result" href="' + url + '">' +
        '<strong>' + escapeHtml(item.section || item.title) + '</strong>' +
        (sectionLabel ? '<span class="result-page">' + pageLabel + '</span>' : '') +
        '<span>' + desc + '</span>' +
        '</a>';
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
    secureExternalLinks();
  }

  if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', init);
  } else {
    init();
  }
})();
