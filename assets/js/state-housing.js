(function () {
  'use strict';

  var stateData = null;
  var federalData = null;

  function escapeHtml(value) {
    return String(value == null ? '' : value)
      .replace(/&/g, '&amp;').replace(/</g, '&lt;').replace(/>/g, '&gt;')
      .replace(/"/g, '&quot;').replace(/'/g, '&#039;');
  }

  function safeLink(url, label) {
    if (!url || !/^https:\/\//i.test(url)) return escapeHtml(label || 'Source unavailable');
    return '<a href="' + escapeHtml(url) + '" target="_blank" rel="noopener noreferrer">' + escapeHtml(label || url) + '</a>';
  }

  function findAuthority(id) {
    if (!stateData || !Array.isArray(stateData.primary_authorities)) return null;
    return stateData.primary_authorities.find(function (a) { return a.id === id; }) || null;
  }

  function authorityList(ids) {
    if (!Array.isArray(ids) || !ids.length) return '';
    var links = ids.map(function (id) {
      var a = findAuthority(id);
      return a ? safeLink(a.url, a.title) : escapeHtml(id);
    });
    return '<p><span class="legal-tag legal-tag-authority">📚 AUTHORITY</span> ' + links.join(' · ') + '</p>';
  }

  function renderRoute(key) {
    var output = document.getElementById('state-route-output');
    if (!output || !stateData || !stateData.document_routes) return;
    var route = stateData.document_routes[key];
    if (!route) return;

    var html = '<section class="emergency-step" id="route-' + escapeHtml(key) + '">';
    if (route.status === 'not_yet_verified') {
      html += '<span class="legal-tag legal-tag-lawyer">🚨 GET A LAWYER</span>';
      html += '<h2>' + escapeHtml(route.label) + ' — procedure not yet verified for publication</h2>';
    } else {
      html += '<span class="legal-tag legal-tag-action">🛠️ DO THIS FIRST</span>';
      html += '<h2>' + escapeHtml(route.label) + '</h2>';
    }
    if (Array.isArray(route.do_now)) {
      html += '<ol>' + route.do_now.map(function (item) { return '<li>' + escapeHtml(item) + '</li>'; }).join('') + '</ol>';
    }
    if (route.deadline) html += '<p><span class="legal-tag legal-tag-deadline">⚠️ DEADLINE</span> ' + escapeHtml(route.deadline) + '</p>';
    if (route.answer_deadline) html += '<p><span class="legal-tag legal-tag-deadline">⚠️ ANSWER / APPEARANCE</span> ' + escapeHtml(route.answer_deadline) + '</p>';
    if (route.appeal_deadline) html += '<p><span class="legal-tag legal-tag-deadline">⚠️ APPEAL</span> ' + escapeHtml(route.appeal_deadline) + '</p>';
    if (route.hearing_process) html += '<p><strong>Court process:</strong> ' + escapeHtml(route.hearing_process) + '</p>';
    if (route.rule_510_timing) html += '<p><strong>Writ timing:</strong> ' + escapeHtml(route.rule_510_timing) + '</p>';
    if (route.posting_warning) html += '<p><strong>Officer warning:</strong> ' + escapeHtml(route.posting_warning) + '</p>';
    if (route.next_stage) html += '<p><strong>What comes next:</strong> ' + escapeHtml(route.next_stage) + '</p>';
    html += authorityList(route.authorities);
    html += '</section>';
    output.innerHTML = html;
  }

  function renderResources() {
    var output = document.getElementById('state-resource-output');
    if (!output || !stateData || !stateData.resources) return;
    var rows = [];
    Object.keys(stateData.resources).forEach(function (key) {
      var r = stateData.resources[key];
      if (!r) return;
      var contact = r.phone ? ' · <a href="tel:' + escapeHtml(r.phone.replace(/[^0-9+]/g, '')) + '">' + escapeHtml(r.phone) + '</a>' : '';
      rows.push('<dt>' + escapeHtml(r.name) + '</dt><dd>' + safeLink(r.url, 'Official / locator page') + contact + (r.note ? ' · ' + escapeHtml(r.note) : '') + '</dd>');
    });
    output.innerHTML = rows.length ? '<dl class="sources-list">' + rows.join('') + '</dl>' : '<p>No verified state resources are published yet.</p>';
  }

  function renderFederal() {
    var output = document.getElementById('federal-overlay-output');
    if (!output || !federalData || !Array.isArray(federalData.overlays)) return;
    output.innerHTML = federalData.overlays.map(function (item) {
      return '<div class="emergency-step"><h3>' + escapeHtml(item.title) + '</h3>' +
        '<p>' + escapeHtml(item.rule) + '</p>' +
        '<p><strong>Limit:</strong> ' + escapeHtml(item.warning) + '</p>' +
        '<p><span class="legal-tag legal-tag-authority">📚 AUTHORITY</span> ' + safeLink(item.url, item.authority) + '</p></div>';
    }).join('');
  }

  function showFailure(message) {
    var output = document.getElementById('state-route-output');
    if (output) output.innerHTML = '<section class="emergency-step"><span class="legal-tag legal-tag-lawyer">🚨 GET LEGAL HELP</span><h2>State procedure could not load</h2><p>' + escapeHtml(message) + '</p><p><a href="find-legal-help.html#homelessness">Find veteran housing legal help</a> · <a href="housing.html">Open national housing resources</a></p></section>';
  }

  function bindRoutes() {
    document.querySelectorAll('[data-route]').forEach(function (link) {
      link.addEventListener('click', function () { renderRoute(link.getAttribute('data-route')); });
    });
    var hash = window.location.hash || '';
    if (hash.indexOf('#route-') === 0) renderRoute(hash.slice(7));
  }

  Promise.all([
    fetch('data/states/texas.json').then(function (r) { if (!r.ok) throw new Error('Texas state procedure data unavailable'); return r.json(); }),
    fetch('data/housing-federal.json').then(function (r) { if (!r.ok) throw new Error('Federal housing overlay unavailable'); return r.json(); })
  ]).then(function (data) {
    stateData = data[0];
    federalData = data[1];
    renderResources();
    renderFederal();
    bindRoutes();
  }).catch(function (err) {
    showFailure(err && err.message ? err.message : 'The state guide could not load.');
  });
})();
