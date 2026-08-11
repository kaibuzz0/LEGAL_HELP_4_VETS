(function() {
  'use strict';

  var COMPONENTS = {
    'skip-link': function(el) {
      el.innerHTML = '<a href="#main-content" class="skip-link">Skip to main content</a>';
    },
    'legal-disclaimer': function(el) {
      el.innerHTML = '<div class="legal-disclaimer" role="banner"><strong>Legal Information, Not Legal Advice.</strong> Laws, deadlines, phone numbers, and procedures change. Before making decisions that affect your benefits, housing, immigration status, or liberty, speak with a licensed attorney or VA-accredited representative.</div>';
    },
    'psalm-banner': function(el) {
      var position = el.dataset.position || 'top';
      var ref = el.dataset.verse || 'psalm-23-1-2';
      el.innerHTML = '<div class="psalm-banner psalm-' + position + '" data-verse="' + ref + '"><span class="psalm-loading" aria-live="polite">Loading...</span></div>';
      loadPsalm(el.querySelector('.psalm-banner'), ref);
    },
    'site-header': function(el) {
      el.innerHTML = '<div class="topbar"><h1><a href="index.html">Veteran Rights Field Manual</a></h1><button class="menu-btn" aria-label="Open navigation menu" aria-expanded="false" aria-controls="sidebar"><span aria-hidden="true">≡</span><span class="sr-only">Menu</span></button><div><a href="tel:988">988 · 1</a><a href="tel:18774243838">1-877-4AID-VET</a><a href="tel:18007997233">1-800-799-SAFE</a></div></div>';
    },
    'site-nav': function(el) {
      var current = el.dataset.current || '';
      var items = [
        { id: 'index', href: 'index.html', label: 'Home' },
        { id: 'help-now', href: 'help-now.html', label: 'I Need Help Now' },
        { id: 'claims', href: 'claims.html', label: 'Claims' },
        { id: 'appeals', href: 'appeals.html', label: 'Appeals' },
        { id: 'discharge-upgrade', href: 'discharge-upgrade.html', label: 'Discharge Upgrade' },
        { id: 'housing', href: 'housing.html', label: 'Housing' },
        { id: 'employment-money', href: 'employment-money.html', label: 'Employment & Money' },
        { id: 'family-immigration', href: 'family-immigration.html', label: 'Family & Immigration' },
        { id: 'legal-library', href: 'legal-library.html', label: 'Legal Library' },
        { id: 'toolkit', href: 'toolkit.html', label: 'Toolkit' },
        { id: 'about', href: 'about.html', label: 'About / Sources' }
      ];
      var html = '<nav class="sidebar" id="sidebar" aria-label="Main navigation"><div class="search-wrap"><input id="searchBox" type="search" placeholder="Find a section..." aria-label="Search sections" autocomplete="off"><button class="search-clear" type="button" aria-label="Clear search" title="Clear search"><span aria-hidden="true">✕</span></button></div><div id="noResults" class="no-results">No sections found.</div><div id="navResults">';
      items.forEach(function(item) {
        var isCurrent = item.id === current;
        var cls = isCurrent ? ' class="current"' : '';
        var aria = isCurrent ? ' aria-current="page"' : '';
        var dataSearch = item.label.toLowerCase();
        html += '<a href="' + item.href + '"' + cls + aria + ' data-search="' + dataSearch + '">' + item.label + '</a>';
      });
      html += '</div></nav>';
      el.innerHTML = html;
    },
    'site-footer': function(el) {
      el.innerHTML = '<footer>Veteran Rights Field Manual · Legal Information, Not Legal Advice · Built to help veterans fight for what they earned. <a class="back-to-top" href="#main-content">↑ Back to top</a></footer>';
    }
  };

  var psalmCache = null;

  function loadPsalm(container, ref) {
    if (psalmCache) {
      renderPsalm(container, ref, psalmCache);
      return;
    }
    var xhr = new XMLHttpRequest();
    xhr.open('GET', 'data/psalms.json', true);
    xhr.onreadystatechange = function() {
      if (xhr.readyState === 4) {
        var data = null;
        if (xhr.status === 200) {
          try {
            data = JSON.parse(xhr.responseText);
          } catch(e) {}
        }
        psalmCache = data || { version: 'KJV', verses: [] };
        renderPsalm(container, ref, psalmCache);
      }
    };
    xhr.send();
  }

  function renderPsalm(container, ref, data) {
    var verse = null;
    if (data && data.verses) {
      for (var i = 0; i < data.verses.length; i++) {
        if (data.verses[i].id === ref) {
          verse = data.verses[i];
          break;
        }
      }
      if (!verse && data.verses.length) {
        verse = data.verses[0];
      }
    }
    if (verse && verse.text && verse.reference) {
      container.innerHTML = '<span class="psalm-ref">' + escapeHtml(verse.reference) + '</span> <span class="psalm-text">"' + escapeHtml(verse.text) + '"</span>';
      container.removeAttribute('aria-live');
    } else {
      container.innerHTML = '<span class="psalm-text">—</span>';
    }
  }

  function escapeHtml(text) {
    return text.replace(/[&<>"']/g, function(m) {
      return { '&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;', "'": '&#039;' }[m];
    });
  }

  function injectComponents() {
    var placeholders = document.querySelectorAll('[data-component]');
    placeholders.forEach(function(el) {
      var name = el.dataset.component;
      if (COMPONENTS[name]) {
        COMPONENTS[name](el);
      }
    });
    document.dispatchEvent(new CustomEvent('componentsLoaded'));
  }

  if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', injectComponents);
  } else {
    injectComponents();
  }
})();