(function() {
  'use strict';

  // Mobile menu toggle
  function initMenu() {
    var menuBtn = document.querySelector('.menu-btn');
    if (menuBtn) {
      menuBtn.addEventListener('click', function() {
        var sidebar = document.getElementById('sidebar');
        if (sidebar) {
          sidebar.classList.toggle('open');
        }
      });
    }

    // Close sidebar when any nav link is clicked (mobile)
    var sidebar = document.getElementById('sidebar');
    if (sidebar) {
      sidebar.querySelectorAll('a[href^="#"]').forEach(function(link) {
        link.addEventListener('click', function() {
          sidebar.classList.remove('open');
        });
      });
    }
  }

  // Build a lightweight search index from headings and data-search attributes
  function buildSearchIndex() {
    var index = [];
    // Sidebar links
    document.querySelectorAll('#navResults a').forEach(function(a) {
      var text = (a.textContent || '').toLowerCase();
      var search = (a.dataset.search || '').toLowerCase();
      var href = a.getAttribute('href') || '';
      index.push({ el: a, terms: text + ' ' + search + ' ' + href });
    });

    // Section headings and summaries
    document.querySelectorAll('.section-card[id]').forEach(function(section) {
      var id = section.id;
      var heading = section.querySelector('h2');
      var headingText = heading ? (heading.textContent || '').toLowerCase() : '';
      var search = (section.dataset.search || '').toLowerCase();
      var bodyText = (section.textContent || '').toLowerCase();
      // Limit body index to avoid noise but allow real searches
      var snippet = bodyText.slice(0, 800);
      index.push({ el: null, target: id, terms: headingText + ' ' + search + ' ' + snippet });
    });

    return index;
  }

  // Live search
  function doSearch() {
    var q = document.getElementById('searchBox');
    if (!q) return;
    var query = q.value.toLowerCase().trim();
    var links = document.querySelectorAll('#navResults a');
    var any = false;

    if (!query) {
      links.forEach(function(a) {
        a.style.display = 'block';
        a.classList.remove('highlight');
      });
      document.getElementById('noResults').style.display = 'none';
      return;
    }

    // Simple AND search: every word in query must appear somewhere
    var words = query.split(/\s+/).filter(function(w) { return w.length > 0; });

    links.forEach(function(a) {
      var text = (a.textContent || '').toLowerCase();
      var search = (a.dataset.search || '').toLowerCase();
      var href = (a.getAttribute('href') || '').toLowerCase();
      var combined = text + ' ' + search + ' ' + href;
      var match = words.every(function(w) { return combined.indexOf(w) !== -1; });
      a.style.display = match ? 'block' : 'none';
      a.classList.toggle('highlight', match);
      if (match) any = true;
    });

    document.getElementById('noResults').style.display = any ? 'none' : 'block';
  }

  // Clear search on Escape
  function initSearch() {
    var searchBox = document.getElementById('searchBox');
    if (searchBox) {
      searchBox.addEventListener('input', doSearch);
      searchBox.addEventListener('keydown', function(e) {
        if (e.key === 'Escape') {
          searchBox.value = '';
          doSearch();
          searchBox.blur();
        }
      });
    }
  }

  // External links: safety attributes (belt-and-suspenders for dynamically added links)
  function secureExternalLinks() {
    document.querySelectorAll('a[href^="http"], a[href^="//"]').forEach(function(a) {
      if (a.getAttribute('target') === '_blank') {
        if (!a.getAttribute('rel') || a.getAttribute('rel').indexOf('noopener') === -1) {
          a.setAttribute('rel', 'noopener noreferrer');
        }
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