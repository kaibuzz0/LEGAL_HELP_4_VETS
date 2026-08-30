(function() {
  'use strict';

  var NAV_ITEMS = [
    { id: 'index', href: 'index.html', label: 'Home' },
    { id: 'emergency', href: 'emergency.html', label: 'Legal Emergency' },
    { id: 'benefit-reductions', href: 'benefit-reductions.html', label: 'Benefit Changes' },
    { id: 'medical-rights', href: 'medical-rights.html', label: 'Medical Rights' },
    { id: 'find-legal-help', href: 'find-legal-help.html', label: 'Find Legal Help' },
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

  function addLegalEmergencyBanner() {
    var path = (window.location.pathname.split('/').pop() || 'index.html').toLowerCase();
    if (path !== 'housing.html' && path !== 'help-now.html') return;
    var main = document.getElementById('main-content');
    if (!main || document.getElementById('lsvh-emergency-banner')) return;
    var box = document.createElement('section');
    box.id = 'lsvh-emergency-banner';
    box.className = 'section-card';
    box.setAttribute('aria-label', 'Legal help for homelessness and housing risk');
    box.innerHTML = '<h2>Need legal help because you are homeless or may lose housing?</h2>' +
      '<p><strong>LSV-H</strong> is a VA grant program that funds free legal services for eligible Veterans who are homeless or at risk for homelessness. Services vary by grantee and may include eviction or foreclosure matters, family law, income support, certain criminal matters related to homelessness, discharge upgrades, consumer issues, health-care access, and employment law.</p>' +
      '<p><strong>Do not assume every grantee handles every case.</strong> Check the current VA grantee list and ask whether the provider handles your specific legal problem.</p>' +
      '<p><a href="find-legal-help.html#homelessness">Find LSV-H and housing legal help</a> · <a href="emergency.html#homeless">Homeless tonight</a> · <a href="emergency.html#eviction">Eviction emergency</a></p>';
    var firstHeading = main.querySelector('h1');
    if (firstHeading && firstHeading.nextSibling) main.insertBefore(box, firstHeading.nextSibling);
    else main.insertBefore(box, main.firstChild);
  }

  function addPrimaryAuthoritiesRegistry() {
    var path = (window.location.pathname.split('/').pop() || '').toLowerCase();
    if (path !== 'sources.html') return;
    var main = document.getElementById('main-content');
    if (!main || document.getElementById('primary-authorities-registry')) return;
    fetch('data/primary-authorities.json')
      .then(function(r) { if (!r.ok) throw new Error('authority registry unavailable'); return r.json(); })
      .then(function(data) {
        if (!data || !Array.isArray(data.authorities)) return;
        var section = document.createElement('section');
        section.id = 'primary-authorities-registry';
        section.className = 'section-card';
        section.innerHTML = '<h2>Primary Legal Authorities — High-Consequence Claims</h2>' +
          '<p>These statutes, regulations, official forms, and agency instructions are separately tracked for deadlines, benefit reductions, emergency care, medical-harm claims, and other high-consequence procedures. Last registry verification: <strong>' + (data.verified_date || 'not stated') + '</strong>.</p>';
        var dl = document.createElement('dl');
        dl.className = 'sources-list';
        data.authorities.forEach(function(a) {
          var dt = document.createElement('dt');
          dt.id = 'primary-' + a.id;
          dt.textContent = a.title + ' (' + a.authority_level + ')';
          var dd = document.createElement('dd');
          var text = document.createTextNode(a.claim + ' · ');
          var link = document.createElement('a');
          link.href = a.url;
          link.target = '_blank';
          link.rel = 'noopener noreferrer';
          link.textContent = 'Primary source';
          dd.appendChild(text); dd.appendChild(link);
          dd.appendChild(document.createTextNode(' · Verified: ' + a.verified_date));
          dl.appendChild(dt); dl.appendChild(dd);
        });
        section.appendChild(dl);
        var intro = main.querySelector('.section-card');
        if (intro && intro.nextSibling) main.insertBefore(section, intro.nextSibling);
        else main.appendChild(section);
      })
      .catch(function() { });
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
      .catch(function() { });
  }

  function init() {
    addLegalEmergencyBanner();
    addPrimaryAuthoritiesRegistry();
    rotatePsalmBanner();
  }

  if (document.readyState === 'loading') document.addEventListener('DOMContentLoaded', init);
  else init();
})();
