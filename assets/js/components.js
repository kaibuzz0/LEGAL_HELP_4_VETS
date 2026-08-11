(function() {
  'use strict';

  var COMPONENTS = {
    'site-nav': function(el) {
      // If a noscript nav is already present, leave it as fallback. Build enhanced nav.
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
        { id: 'substance-use', href: 'substance-use.html', label: 'Substance Use & Recovery' },
        { id: 'widows', href: 'widows.html', label: 'Widows & Surviving Spouses' },
        { id: 'state-resources', href: 'state-resources.html', label: 'State & Local Resources' },
        { id: 'faith-encouragement', href: 'faith-encouragement.html', label: 'Faith & Encouragement' },
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
    }
  };

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

  function rotatePsalmBanner() {
    var banners = document.querySelectorAll('.psalm-banner');
    if (!banners.length) return;
    fetch('data/psalms.json')
      .then(function(r) { return r.json(); })
      .then(function(data) {
        if (!data || !data.verses || !data.verses.length) return;
        var index = Math.floor(Math.random() * data.verses.length);
        var verse = data.verses[index];
        banners.forEach(function(banner) {
          var refEl = banner.querySelector('.psalm-ref');
          var textEl = banner.querySelector('.psalm-text');
          if (refEl) refEl.textContent = verse.reference;
          if (textEl) textEl.textContent = '"' + verse.text + '"';
        });
      })
      .catch(function() {
        // leave static fallback in place
      });
  }

  // Run Psalm rotation after components load
  document.addEventListener('componentsLoaded', rotatePsalmBanner);

})();