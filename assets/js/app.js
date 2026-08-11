(function() {
  'use strict';

  function initMenu() {
    var menuBtn = document.querySelector('.menu-btn');
    var sidebar = document.getElementById('sidebar');
    if (!menuBtn || !sidebar) return;

    menuBtn.addEventListener('click', function() {
      var isOpen = sidebar.classList.toggle('open');
      menuBtn.setAttribute('aria-expanded', isOpen ? 'true' : 'false');
    });

    sidebar.querySelectorAll('a[href^="#"]').forEach(function(link) {
      link.addEventListener('click', function() {
        sidebar.classList.remove('open');
        menuBtn.setAttribute('aria-expanded', 'false');
      });
    });

    // Close sidebar when clicking outside on mobile
    document.addEventListener('click', function(e) {
      if (window.innerWidth > 900) return;
      if (!sidebar.classList.contains('open')) return;
      if (sidebar.contains(e.target) || menuBtn.contains(e.target)) return;
      sidebar.classList.remove('open');
      menuBtn.setAttribute('aria-expanded', 'false');
    });
  }

  function initSearch() {
    var searchBox = document.getElementById('searchBox');
    var clearBtn = document.querySelector('.search-clear');
    if (!searchBox) return;

    function clearSearch() {
      searchBox.value = '';
      doSearch();
      searchBox.focus();
    }

    searchBox.addEventListener('input', doSearch);
    searchBox.addEventListener('keydown', function(e) {
      if (e.key === 'Escape') {
        clearSearch();
        searchBox.blur();
      }
    });

    if (clearBtn) {
      clearBtn.addEventListener('click', clearSearch);
    }
  }

  function doSearch() {
    var q = document.getElementById('searchBox');
    if (!q) return;
    var query = q.value.toLowerCase().trim();
    var links = document.querySelectorAll('#navResults a');
    var clearBtn = document.querySelector('.search-clear');
    var any = false;

    if (clearBtn) {
      clearBtn.classList.toggle('visible', query.length > 0);
    }

    if (!query) {
      links.forEach(function(a) {
        a.style.display = 'block';
        a.classList.remove('highlight');
      });
      document.getElementById('noResults').style.display = 'none';
      return;
    }

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

  function initScrollSpy() {
    var sidebarLinks = document.querySelectorAll('#navResults a[href^="#"]');
    var sections = Array.from(document.querySelectorAll('.section-card[id]'));
    if (!sections.length || !sidebarLinks.length) return;

    var observer = new IntersectionObserver(function(entries) {
      entries.forEach(function(entry) {
        if (entry.isIntersecting) {
          sidebarLinks.forEach(function(link) {
            link.classList.remove('active');
          });
          var active = document.querySelector('#navResults a[href="#' + entry.target.id + '"]');
          if (active) active.classList.add('active');
        }
      });
    }, {
      rootMargin: '-20% 0px -60% 0px',
      threshold: 0
    });

    sections.forEach(function(section) {
      observer.observe(section);
    });
  }

  function init() {
    initMenu();
    initSearch();
    secureExternalLinks();
    initScrollSpy();
  }

  function initApp() {
    initMenu();
    initSearch();
    secureExternalLinks();
    initScrollSpy();
  }

  document.addEventListener('componentsLoaded', function() {
    initApp();
  });

  if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', initApp);
  } else {
    initApp();
  }
})();