(function() {
  'use strict';

  // Unified mobile menu
  function initMenu() {
    var menuBtn = document.querySelector('.menu-btn');
    var nav = document.getElementById('main-nav');
    var overlay = document.querySelector('.nav-overlay');
    if (!menuBtn || !nav) return;

    function setOpen(isOpen) {
      nav.classList.toggle('open', isOpen);
      if (overlay) overlay.classList.toggle('open', isOpen);
      menuBtn.setAttribute('aria-expanded', isOpen ? 'true' : 'false');
    }

    menuBtn.addEventListener('click', function() {
      setOpen(!nav.classList.contains('open'));
    });

    if (overlay) {
      overlay.addEventListener('click', function() { setOpen(false); });
    }

    nav.querySelectorAll('a').forEach(function(link) {
      link.addEventListener('click', function() {
        if (window.innerWidth <= 900) setOpen(false);
      });
    });

    document.addEventListener('keydown', function(e) {
      if (e.key === 'Escape' && nav.classList.contains('open')) {
        setOpen(false);
        menuBtn.focus();
      }
    });
  }

  // Site search overlay
  var searchIndex = [];
  function initSearch() {
    var searchBtn = document.querySelector('.search-btn');
    var overlay = document.getElementById('search-overlay');
    var input = document.getElementById('search-input');
    var results = document.getElementById('search-results');
    var closeBtn = document.getElementById('search-close');
    if (!overlay || !input || !results) return;

    function openSearch() {
      overlay.classList.add('open');
      input.value = '';
      input.focus();
      results.innerHTML = '<p class="search-empty">Type a topic like "housing", "USERRA", "debt", or "appeal".</p>';
    }

    function closeSearch() {
      overlay.classList.remove('open');
      if (searchBtn) searchBtn.focus();
    }

    if (searchBtn) searchBtn.addEventListener('click', openSearch);
    if (closeBtn) closeBtn.addEventListener('click', closeSearch);

    document.addEventListener('keydown', function(e) {
      if ((e.key === '/' && !e.ctrlKey && !e.metaKey && document.activeElement.tagName !== 'INPUT' && document.activeElement.tagName !== 'TEXTAREA') ||
          ((e.ctrlKey || e.metaKey) && e.key === 'k')) {
        e.preventDefault();
        openSearch();
      }
      if (e.key === 'Escape' && overlay.classList.contains('open')) {
        closeSearch();
      }
    });

    input.addEventListener('input', function() {
      renderResults(input.value.trim().toLowerCase());
    });

    input.addEventListener('keydown', function(e) {
      if (e.key === 'Escape') closeSearch();
      if (e.key === 'Enter') {
        var first = results.querySelector('.search-result');
        if (first) window.location.href = first.href;
      }
    });

    function renderResults(query) {
      if (!query) {
        results.innerHTML = '<p class="search-empty">Type a topic like "housing", "USERRA", "debt", or "appeal".</p>';
        return;
      }
      var words = query.split(/\s+/).filter(Boolean);
      var matches = searchIndex.filter(function(item) {
        var hay = (item.title + ' ' + item.h1 + ' ' + item.description + ' ' + item.excerpt + ' ' + item.page).toLowerCase();
        return words.every(function(w) { return hay.indexOf(w) !== -1; });
      }).slice(0, 12);

      if (!matches.length) {
        results.innerHTML = '<p class="search-empty">No results. Try "housing", "USERRA", "debt", "appeal", or "discharge".</p>';
        return;
      }

      results.innerHTML = matches.map(function(item) {
        var url = item.url;
        if (item.anchor) url += '#' + item.anchor;
        return '<a class="search-result" href="' + url + '"><h4>' + escapeHtml(item.description || item.title) + '</h4><p>' + escapeHtml(item.excerpt) + '</p><small>' + escapeHtml(item.page.replace('.html','')) + '</small></a>';
      }).join('');
    }

    loadSearchIndex();
  }

  function loadSearchIndex() {
    var path = 'assets/js/search-index.json';
    fetch(path)
      .then(function(r) { return r.json(); })
      .then(function(data) {
        if (Array.isArray(data)) searchIndex = data;
      })
      .catch(function() {
        // Search will remain empty; fallback is the navigation menu
      });
  }

  function escapeHtml(text) {
    return (text || '').replace(/&/g,'&amp;').replace(/</g,'&lt;').replace(/>/g,'&gt;');
  }

  // Secure external links
  function secureExternalLinks() {
    document.querySelectorAll('a[href^="http"], a[href^="//"]').forEach(function(a) {
      if (a.getAttribute('target') === '_blank') {
        var rel = a.getAttribute('rel') || '';
        if (rel.indexOf('noopener') === -1) {
          a.setAttribute('rel', 'noopener noreferrer');
        }
      }
    });
  }

  function initApp() {
    initMenu();
    initSearch();
    secureExternalLinks();
  }

  if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', initApp);
  } else {
    initApp();
  }
})();
