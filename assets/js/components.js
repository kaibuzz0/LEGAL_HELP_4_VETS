(function() {
  'use strict';

  var NAV_ITEMS = [
    { id: 'index', href: 'index.html', label: 'Home' },
    { id: 'help-now', href: 'help-now.html', label: 'Crisis Help' },
    { id: 'claims', href: 'claims.html', label: 'VA Claims' },
    { id: 'appeals', href: 'appeals.html', label: 'Appeals' },
    { id: 'discharge-upgrade', href: 'discharge-upgrade.html', label: 'Discharge Upgrade' },
    { id: 'housing', href: 'housing.html', label: 'Housing' },
    { id: 'employment-money', href: 'employment-money.html', label: 'Money & Employment' },
    { id: 'employment-rights', href: 'employment-rights.html', label: 'USERRA Rights' },
    { id: 'va-debt', href: 'va-debt.html', label: 'VA Debt' },
    { id: 'family-immigration', href: 'family-immigration.html', label: 'Family & Immigration' },
    { id: 'substance-use', href: 'substance-use.html', label: 'Substance Use' },
    { id: 'widows', href: 'widows.html', label: 'Survivor Benefits' },
    { id: 'state-resources', href: 'state-resources.html', label: 'State Resources' },
    { id: 'toolkit', href: 'toolkit.html', label: 'Toolkit' },
    { id: 'legal-library', href: 'legal-library.html', label: 'Legal Library' },
    { id: 'faith-encouragement', href: 'faith-encouragement.html', label: 'Faith' },
    { id: 'about', href: 'about.html', label: 'About / Sources' }
  ];

  

  

  if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', rotatePsalmBanner);
  } else {
    rotatePsalmBanner();
  }

  // Psalm banner rotation
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

  rotatePsalmBanner();
})();
