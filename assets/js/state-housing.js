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

  function renderClock(clock) {
    if (!clock) return '<p><span class="legal-tag legal-tag-deadline">⚠️ DEADLINE</span> Deadline not yet verified for this route — check the controlling document/source or get legal help.</p>';
    if (clock.verified !== true) return '<p><span class="legal-tag legal-tag-deadline">⚠️ DEADLINE</span> Deadline not yet verified for publication.</p>';
    var html = '<div class="action-now"><strong>⚠️ POSSIBLE IMMEDIATE DEADLINE:</strong><br/>' + escapeHtml(clock.display || clock.label) + '</div>';
    html += '<p><strong>Clock attaches to:</strong> ' + escapeHtml(clock.deadline_trigger || 'trigger not separately stated') + '</p>';
    if (Array.isArray(clock.exceptions) && clock.exceptions.length) html += '<p><strong>Check exceptions:</strong> ' + escapeHtml(clock.exceptions.join('; ')) + '</p>';
    return html;
  }

  function renderRoute(key) {
    var output = document.getElementById('state-route-output');
    if (!output || !stateData || !stateData.document_routes) return;
    var route = stateData.document_routes[key];
    if (!route) return;

    var publishable = route.status === 'verified' || route.status === 'partially_verified';
    var html = '<section class="emergency-step" id="route-' + escapeHtml(key) + '">';
    if (!publishable) {
      html += '<span class="legal-tag legal-tag-lawyer">🚨 GET A LAWYER</span>';
      html += '<h2>' + escapeHtml(route.label) + ' — procedure not yet verified for publication</h2>';
    } else {
      html += '<span class="legal-tag legal-tag-action">🛠️ DO THIS FIRST</span><h2>' + escapeHtml(route.label) + '</h2>';
      if (route.status === 'partially_verified') html += '<p><strong>Verification status:</strong> Core distinction verified; not every deadline/remedy for this category is published.</p>';
    }

    if (route.immediate_clock !== undefined) html += renderClock(route.immediate_clock);
    if (route.court) html += '<p><strong>Court / forum:</strong> ' + escapeHtml(route.court) + '</p>';
    if (route.required_filing) html += '<p><strong>Required filing when using this remedy:</strong> ' + escapeHtml(route.required_filing) + '</p>';
    if (route.optional_filing) html += '<p><strong>Optional filing:</strong> ' + escapeHtml(route.optional_filing) + '</p>';
    if (Array.isArray(route.do_now)) html += '<h3>What to do today</h3><ol>' + route.do_now.map(function (item) { return '<li>' + escapeHtml(item) + '</li>'; }).join('') + '</ol>';
    if (route.remedy) html += '<p><strong>Remedy:</strong> ' + escapeHtml(route.remedy) + '</p>';
    if (route.stay_possession_consequence) html += '<p><strong>Possession consequence:</strong> ' + escapeHtml(route.stay_possession_consequence) + '</p>';
    if (route.execution) html += '<p><strong>Execution:</strong> ' + escapeHtml(route.execution.summary) + ' <strong>Local warning:</strong> ' + escapeHtml(route.execution.local_practice_warning) + '</p>';
    if (route.sale_baseline) html += '<p><strong>Sale baseline:</strong> ' + escapeHtml(route.sale_baseline.summary) + '</p>';
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
      if (!r || r.status === 'unverified') return;
      var contact = r.phone ? ' · <a href="tel:' + escapeHtml(r.phone.replace(/[^0-9+]/g, '')) + '">' + escapeHtml(r.phone) + '</a>' : '';
      rows.push('<dt>' + escapeHtml(r.name) + '</dt><dd>' + safeLink(r.url, 'Official / locator page') + contact + (r.routing ? ' · Route: ' + escapeHtml(r.routing) : '') + (r.note ? ' · ' + escapeHtml(r.note) : '') + '</dd>');
    });
    output.innerHTML = rows.length ? '<dl class="sources-list">' + rows.join('') + '</dl>' : '<p>No verified state resources are published yet.</p>';
  }

  function renderFederal() {
    var output = document.getElementById('federal-overlay-output');
    if (!output || !federalData || !Array.isArray(federalData.overlays)) return;
    output.innerHTML = federalData.overlays.map(function (item) {
      return '<div class="emergency-step"><h3>' + escapeHtml(item.title) + '</h3><p><strong>Status:</strong> ' + escapeHtml(item.status) + '</p><p>' + escapeHtml(item.rule) + '</p><p><strong>Limit:</strong> ' + escapeHtml(item.warning) + '</p><p><span class="legal-tag legal-tag-authority">📚 AUTHORITY</span> ' + safeLink(item.url, item.authority) + '</p></div>';
    }).join('');

    var ra = document.getElementById('reasonable-accommodation-output');
    var wf = federalData.reasonable_accommodation_workflow;
    if (ra && wf && Array.isArray(wf.steps)) {
      ra.innerHTML = '<ol>' + wf.steps.map(function (s) { return '<li>' + escapeHtml(s) + '</li>'; }).join('') + '</ol>' +
        '<p><strong>Limits:</strong> ' + escapeHtml((wf.limits || []).join(' ')) + '</p>' +
        '<p><strong>HUD/FHEO:</strong> ' + safeLink(wf.hud_complaint && wf.hud_complaint.url, 'Report housing discrimination') +
        (wf.hud_complaint && wf.hud_complaint.phone ? ' · <a href="tel:' + escapeHtml(wf.hud_complaint.phone.replace(/[^0-9+]/g, '')) + '">' + escapeHtml(wf.hud_complaint.phone) + '</a>' : '') +
        ' · ' + escapeHtml(wf.hud_complaint && wf.hud_complaint.deadline_summary) + '</p>';
    }
  }

  function renderLocalRuleWarning() {
    var output = document.getElementById('local-rule-output');
    var local = stateData && stateData.local_variation;
    if (!output || !local) return;
    output.innerHTML = '<p>' + escapeHtml(local.statewide_rule) + '</p><p>' + safeLink(local.local_rule_locator, 'Search Texas local rules, forms, and standing orders') + '</p>';
  }

  function showFailure(message) {
    var output = document.getElementById('state-route-output');
    if (output) output.innerHTML = '<section class="emergency-step"><span class="legal-tag legal-tag-lawyer">🚨 GET LEGAL HELP</span><h2>State procedure could not load</h2><p>' + escapeHtml(message) + '</p><p><a href="find-legal-help.html#homelessness">Find veteran housing legal help</a> · <a href="housing.html">Open national housing resources</a></p></section>';
  }

  function bindRoutes() {
    document.querySelectorAll('[data-route]').forEach(function (link) {
      link.addEventListener('click', function () { renderRoute(link.getAttribute('data-route')); });
    });
  }

  Promise.all([
    fetch('data/states/texas.json').then(function (r) { if (!r.ok) throw new Error('Texas state procedure data unavailable'); return r.json(); }),
    fetch('data/housing-federal.json').then(function (r) { if (!r.ok) throw new Error('Federal housing overlay unavailable'); return r.json(); })
  ]).then(function (data) {
    stateData = data[0]; federalData = data[1];
    renderResources(); renderFederal(); renderLocalRuleWarning(); bindRoutes();
  }).catch(function (err) {
    showFailure(err && err.message ? err.message : 'The state guide could not load.');
  });
})();
