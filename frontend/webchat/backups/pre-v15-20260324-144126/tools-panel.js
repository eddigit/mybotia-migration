/**
 * MyBotIA V12 — Right Tools Panel
 * Notes, Agent Info, CRM Actions, Tasks (PostgreSQL), Calculator
 */
(function() {
  'use strict';

  // --- Config ---
  var TASKS_API_URL = '/api/notion-tasks.php';
  var NOTES_KEY = 'mybotia-notes-';

  // --- Inject Right Sidebar HTML ---
  function injectToolsPanel() {
    // Add toggle button in header (after btn-theme)
    var btnTheme = document.getElementById('btn-theme');
    if (btnTheme && !document.getElementById('btn-tools-toggle')) {
      var btn = document.createElement('button');
      btn.className = 'btn-tools-toggle';
      btn.id = 'btn-tools-toggle';
      btn.title = 'Outils';
      btn.innerHTML = '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><rect x="3" y="3" width="7" height="7"/><rect x="14" y="3" width="7" height="7"/><rect x="3" y="14" width="7" height="7"/><rect x="14" y="14" width="7" height="7"/></svg>';
      btnTheme.parentNode.insertBefore(btn, btnTheme.nextSibling);
    }

    // Create right sidebar
    if (document.getElementById('right-sidebar')) return;

    var rs = document.createElement('div');
    rs.className = 'right-sidebar';
    rs.id = 'right-sidebar';
    rs.innerHTML = [
      '<div class="rs-header">',
      '  <span class="rs-title">Outils</span>',
      '  <button class="rs-close" id="rs-close" title="Fermer">&times;</button>',
      '</div>',
      '<div class="rs-tabs">',
      '  <button class="rs-tab active" data-rs-tab="notes">',
      '    <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M14 2H6a2 2 0 0 0-2 2v16a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2V8z"/><polyline points="14 2 14 8 20 8"/></svg>',
      '    Notes',
      '  </button>',
      '  <button class="rs-tab" data-rs-tab="agent">',
      '    <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><circle cx="12" cy="12" r="3"/><path d="M19.4 15a1.65 1.65 0 0 0 .33 1.82l.06.06a2 2 0 0 1-2.83 2.83l-.06-.06a1.65 1.65 0 0 0-1.82-.33 1.65 1.65 0 0 0-1 1.51V21a2 2 0 0 1-4 0v-.09A1.65 1.65 0 0 0 9 19.4a1.65 1.65 0 0 0-1.82.33l-.06.06a2 2 0 0 1-2.83-2.83l.06-.06A1.65 1.65 0 0 0 4.68 15a1.65 1.65 0 0 0-1.51-1H3a2 2 0 0 1 0-4h.09A1.65 1.65 0 0 0 4.6 9a1.65 1.65 0 0 0-.33-1.82l-.06-.06a2 2 0 0 1 2.83-2.83l.06.06A1.65 1.65 0 0 0 9 4.68a1.65 1.65 0 0 0 1-1.51V3a2 2 0 0 1 4 0v.09a1.65 1.65 0 0 0 1 1.51 1.65 1.65 0 0 0 1.82-.33l.06-.06a2 2 0 0 1 2.83 2.83l-.06.06A1.65 1.65 0 0 0 19.4 9a1.65 1.65 0 0 0 1.51 1H21a2 2 0 0 1 0 4h-.09a1.65 1.65 0 0 0-1.51 1z"/></svg>',
      '    Agent',
      '  </button>',
      '  <button class="rs-tab" data-rs-tab="crm">',
      '    <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M17 21v-2a4 4 0 0 0-4-4H5a4 4 0 0 0-4 4v2"/><circle cx="9" cy="7" r="4"/><path d="M23 21v-2a4 4 0 0 0-3-3.87"/><path d="M16 3.13a4 4 0 0 1 0 7.75"/></svg>',
      '    CRM',
      '  </button>',
      '  <button class="rs-tab" data-rs-tab="tasks">',
      '    <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M9 11l3 3L22 4"/><path d="M21 12v7a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2V5a2 2 0 0 1 2-2h11"/></svg>',
      '    Taches',
      '  </button>',
      '  <button class="rs-tab" data-rs-tab="calc">',
      '    <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><rect x="4" y="2" width="16" height="20" rx="2"/><line x1="8" y1="6" x2="16" y2="6"/><line x1="8" y1="10" x2="8" y2="10.01"/><line x1="12" y1="10" x2="12" y2="10.01"/><line x1="16" y1="10" x2="16" y2="10.01"/><line x1="8" y1="14" x2="8" y2="14.01"/><line x1="12" y1="14" x2="12" y2="14.01"/><line x1="16" y1="14" x2="16" y2="14.01"/><line x1="8" y1="18" x2="8" y2="18.01"/><line x1="12" y1="18" x2="16" y2="18"/></svg>',
      '    Calc',
      '  </button>',
      '</div>',
      '<div class="rs-content" id="rs-content">',
      '  <!-- NOTES PANEL -->',
      '  <div class="rs-panel active" id="rs-panel-notes">',
      '    <textarea class="rs-notes-area" id="rs-notes-area" placeholder="Vos notes pour cette conversation..."></textarea>',
      '    <div class="rs-notes-status" id="rs-notes-status">Sauvegarde auto</div>',
      '  </div>',
      '  <!-- AGENT PANEL -->',
      '  <div class="rs-panel" id="rs-panel-agent">',
      '    <div class="rs-agent-card">',
      '      <div class="rs-agent-header">',
      '        <div class="rs-agent-avatar" id="rs-agent-avatar">M</div>',
      '        <div>',
      '          <div class="rs-agent-name" id="rs-agent-name">Agent</div>',
      '          <div class="rs-agent-role" id="rs-agent-role">Assistant IA</div>',
      '        </div>',
      '      </div>',
      '      <div class="rs-agent-stat"><span class="rs-agent-stat-label">Statut</span><span class="rs-agent-stat-value" id="rs-agent-status">--</span></div>',
      '      <div class="rs-agent-stat"><span class="rs-agent-stat-label">Modele</span><span class="rs-agent-stat-value" id="rs-agent-model">--</span></div>',
      '      <div class="rs-agent-stat"><span class="rs-agent-stat-label">Session</span><span class="rs-agent-stat-value" id="rs-agent-session">--</span></div>',
      '      <div class="rs-agent-stat"><span class="rs-agent-stat-label">Connexion</span><span class="rs-agent-stat-value" id="rs-agent-ws">--</span></div>',
      '    </div>',
      '    <div class="rs-agent-sources" id="rs-agent-sources">',
      '      <div class="rs-agent-sources-title">Sources actives</div>',
      '      <div id="rs-sources-list"></div>',
      '    </div>',
      '  </div>',
      '  <!-- CRM PANEL -->',
      '  <div class="rs-panel" id="rs-panel-crm">',
      '    <!-- CRM Header with stats -->',
      '    <div class="rs-crm-stats" id="rs-crm-stats"></div>',
      '    <!-- CRM Tabs -->',
      '    <div class="rs-crm-tabs" id="rs-crm-tabs">',
      '      <button class="rs-crm-tab active" data-crm-tab="clients">Clients</button>',
      '      <button class="rs-crm-tab" data-crm-tab="projets">Projets</button>',
      '      <button class="rs-crm-tab" data-crm-tab="paiements">Paiements</button>',
      '    </div>',
      '    <!-- Search + Add -->',
      '    <div class="rs-crm-toolbar">',
      '      <input type="text" class="rs-crm-search" id="rs-crm-search" placeholder="Rechercher...">',
      '      <button class="rs-crm-add-btn" id="rs-crm-add-btn" title="Ajouter">+</button>',
      '    </div>',
      '    <!-- Status filter (clients) -->',
      '    <div class="rs-crm-status-filter" id="rs-crm-status-filter">',
      '      <button class="rs-crm-sf active" data-status="">Tous</button>',
      '      <button class="rs-crm-sf" data-status="Actif">Actifs</button>',
      '      <button class="rs-crm-sf" data-status="Prospect">Prospects</button>',
      '      <button class="rs-crm-sf" data-status="Inactif">Inactifs</button>',
      '    </div>',
      '    <!-- Add Client Form (hidden) -->',
      '    <div class="rs-crm-form" id="rs-crm-form" style="display:none">',
      '      <input type="text" class="rs-task-input" id="rs-crm-f-nom" placeholder="Nom *" maxlength="200">',
      '      <input type="email" class="rs-task-input" id="rs-crm-f-email" placeholder="Email" style="margin-top:6px">',
      '      <input type="text" class="rs-task-input" id="rs-crm-f-tel" placeholder="Telephone" style="margin-top:6px">',
      '      <input type="text" class="rs-task-input" id="rs-crm-f-societe" placeholder="Societe" style="margin-top:6px">',
      '      <div class="rs-task-form-row" style="margin-top:6px">',
      '        <select class="rs-task-select" id="rs-crm-f-status"><option value="Prospect">Prospect</option><option value="En essai">En essai</option><option value="Actif">Actif</option><option value="Inactif">Inactif</option></select>',
      '        <select class="rs-task-select" id="rs-crm-f-abo"><option value="">Abonnement</option><option value="Prospect">Prospect</option><option value="Essai">Essai</option><option value="Premium">Premium</option><option value="Personnel">Personnel</option></select>',
      '      </div>',
      '      <div class="rs-task-form-actions" style="margin-top:8px">',
      '        <button class="rs-task-form-cancel" id="rs-crm-f-cancel">Annuler</button>',
      '        <button class="rs-task-form-submit" id="rs-crm-f-submit">Ajouter</button>',
      '      </div>',
      '    </div>',
      '    <!-- CRM List -->',
      '    <div id="rs-crm-list">',
      '      <div class="rs-tasks-loading">Chargement CRM...</div>',
      '    </div>',
      '    <!-- Client Detail (hidden) -->',
      '    <div id="rs-crm-detail" style="display:none"></div>',
      '  </div>',
      '  <!-- TASKS PANEL -->',
      '  <div class="rs-panel" id="rs-panel-tasks">',
      '    <div class="rs-tasks-header">',
      '      <span class="rs-tasks-date" id="rs-tasks-date">Aujourd\'hui</span>',
      '      <div class="rs-tasks-actions">',
      '        <button class="rs-tasks-add-btn" id="rs-tasks-add-btn" title="Nouvelle tache">+</button>',
      '        <button class="rs-tasks-refresh" id="rs-tasks-refresh" title="Rafraichir">&#8635;</button>',
      '      </div>',
      '    </div>',
      '    <div class="rs-tasks-filters" id="rs-tasks-filters">',
      '      <button class="rs-filter-btn active" data-filter="today">Aujourd\'hui <span class="rs-filter-badge" id="badge-today">0</span></button>',
      '      <button class="rs-filter-btn" data-filter="overdue">En retard <span class="rs-filter-badge rs-badge-danger" id="badge-overdue">0</span></button>',
      '      <button class="rs-filter-btn" data-filter="upcoming">A venir <span class="rs-filter-badge" id="badge-upcoming">0</span></button>',
      '      <button class="rs-filter-btn" data-filter="unplanned">Non planifiees <span class="rs-filter-badge rs-badge-warn" id="badge-unplanned">0</span></button>',
      '      <button class="rs-filter-btn" data-filter="all">Toutes</button>',
      '    </div>',
      '    <!-- Add task form (hidden by default) -->',
      '    <div class="rs-task-form" id="rs-task-form" style="display:none">',
      '      <input type="text" class="rs-task-input" id="rs-task-input-title" placeholder="Titre de la tache..." maxlength="200">',
      '      <div class="rs-task-form-row">',
      '        <select class="rs-task-select" id="rs-task-input-priority">',
      '          <option value="Normale">Normale</option>',
      '          <option value="Urgente">Urgente</option>',
      '          <option value="Haute">Haute</option>',
      '          <option value="Basse">Basse</option>',
      '        </select>',
      '        <input type="date" class="rs-task-input-date" id="rs-task-input-deadline">',
      '      </div>',
      '      <div class="rs-task-form-actions">',
      '        <button class="rs-task-form-cancel" id="rs-task-form-cancel">Annuler</button>',
      '        <button class="rs-task-form-submit" id="rs-task-form-submit">Ajouter</button>',
      '      </div>',
      '    </div>',
      '    <div id="rs-tasks-list">',
      '      <div class="rs-tasks-loading">Chargement des taches...</div>',
      '    </div>',
      '  </div>',
      '  <!-- CALC PANEL -->',
      '  <div class="rs-panel" id="rs-panel-calc">',
      '    <div class="calc-display">',
      '      <div class="calc-history" id="calc-history"></div>',
      '      <div class="calc-screen" id="calc-screen">0</div>',
      '    </div>',
      '    <div class="calc-grid">',
      '      <button class="calc-btn calc-fn" data-calc="clear">C</button>',
      '      <button class="calc-btn calc-fn" data-calc="backspace">&larr;</button>',
      '      <button class="calc-btn calc-fn" data-calc="percent">%</button>',
      '      <button class="calc-btn calc-op" data-calc="/">&divide;</button>',
      '      <button class="calc-btn" data-calc="7">7</button>',
      '      <button class="calc-btn" data-calc="8">8</button>',
      '      <button class="calc-btn" data-calc="9">9</button>',
      '      <button class="calc-btn calc-op" data-calc="*">&times;</button>',
      '      <button class="calc-btn" data-calc="4">4</button>',
      '      <button class="calc-btn" data-calc="5">5</button>',
      '      <button class="calc-btn" data-calc="6">6</button>',
      '      <button class="calc-btn calc-op" data-calc="-">&minus;</button>',
      '      <button class="calc-btn" data-calc="1">1</button>',
      '      <button class="calc-btn" data-calc="2">2</button>',
      '      <button class="calc-btn" data-calc="3">3</button>',
      '      <button class="calc-btn calc-op" data-calc="+">+</button>',
      '      <button class="calc-btn calc-zero" data-calc="0">0</button>',
      '      <button class="calc-btn" data-calc=".">.</button>',
      '      <button class="calc-btn calc-eq" data-calc="=">=</button>',
      '    </div>',
      '    <div class="calc-extras">',
      '      <button class="calc-btn calc-extra" data-calc="tva20" title="TVA 20%">+TVA 20%</button>',
      '      <button class="calc-btn calc-extra" data-calc="ht20" title="HT depuis TTC (TVA 20%)">HT 20%</button>',
      '      <button class="calc-btn calc-extra" data-calc="tva10" title="TVA 10%">+TVA 10%</button>',
      '    </div>',
      '  </div>',
      '</div>'
    ].join('\n');

    // Insert after app-main, before scripts
    var appMain = document.querySelector('.app-main');
    if (appMain && appMain.parentNode) {
      appMain.parentNode.insertBefore(rs, appMain.nextSibling);
    }
  }

  // --- Tab switching ---
  function initTabs() {
    document.querySelectorAll('.rs-tab[data-rs-tab]').forEach(function(tab) {
      tab.addEventListener('click', function() {
        var target = tab.dataset.rsTab;
        document.querySelectorAll('.rs-tab').forEach(function(t) { t.classList.remove('active'); });
        document.querySelectorAll('.rs-panel').forEach(function(p) { p.classList.remove('active'); });
        tab.classList.add('active');
        var panel = document.getElementById('rs-panel-' + target);
        if (panel) panel.classList.add('active');
        // Load on first click
        if (target === 'tasks' && !tasksLoaded) { loadTasks(); }
        if (target === 'crm' && !crmLoaded) { loadCRM(); }
      });
    });
  }

  // --- Toggle sidebar ---
  function initToggle() {
    var btn = document.getElementById('btn-tools-toggle');
    var rs = document.getElementById('right-sidebar');
    var closeBtn = document.getElementById('rs-close');

    if (btn) {
      btn.addEventListener('click', function() {
        rs.classList.toggle('open');
        btn.classList.toggle('active');
      });
    }
    if (closeBtn) {
      closeBtn.addEventListener('click', function() {
        rs.classList.remove('open');
        if (btn) btn.classList.remove('active');
      });
    }
  }

  // --- Notes ---
  var notesSaveTimeout = null;

  function initNotes() {
    var area = document.getElementById('rs-notes-area');
    var status = document.getElementById('rs-notes-status');
    if (!area) return;

    // Load saved notes
    var sessionKey = localStorage.getItem('mybotia-session') || 'main';
    var saved = localStorage.getItem(NOTES_KEY + sessionKey);
    if (saved) area.value = saved;

    area.addEventListener('input', function() {
      if (notesSaveTimeout) clearTimeout(notesSaveTimeout);
      status.textContent = 'Sauvegarde...';
      notesSaveTimeout = setTimeout(function() {
        var key = localStorage.getItem('mybotia-session') || 'main';
        localStorage.setItem(NOTES_KEY + key, area.value);
        status.textContent = 'Sauvegarde auto — ' + new Date().toLocaleTimeString('fr-FR');
      }, 800);
    });
  }

  // --- Agent info ---
  function updateAgentInfo() {
    var headerName = document.getElementById('header-name');
    var headerRole = document.getElementById('header-role');
    var statusDot = document.getElementById('status-dot');

    var rsName = document.getElementById('rs-agent-name');
    var rsRole = document.getElementById('rs-agent-role');
    var rsAvatar = document.getElementById('rs-agent-avatar');
    var rsStatus = document.getElementById('rs-agent-status');
    var rsSession = document.getElementById('rs-agent-session');
    var rsWs = document.getElementById('rs-agent-ws');

    if (rsName && headerName) rsName.textContent = headerName.textContent;
    if (rsRole && headerRole) rsRole.textContent = headerRole.textContent;
    if (rsAvatar && headerName) {
      var initial = headerName.textContent.charAt(0).toUpperCase();
      rsAvatar.textContent = initial;
    }

    if (rsStatus) {
      if (statusDot && statusDot.classList.contains('connected')) {
        rsStatus.textContent = 'En ligne';
        rsStatus.style.color = '#22c55e';
      } else if (statusDot && statusDot.classList.contains('connecting')) {
        rsStatus.textContent = 'Connexion...';
        rsStatus.style.color = '#f59e0b';
      } else {
        rsStatus.textContent = 'Hors ligne';
        rsStatus.style.color = '#ef4444';
      }
    }

    if (rsSession) {
      rsSession.textContent = localStorage.getItem('mybotia-session') || 'main';
    }

    if (rsWs) {
      rsWs.textContent = statusDot && statusDot.classList.contains('connected') ? 'WebSocket OK' : 'Deconnecte';
    }

    var sourcesList = document.getElementById('rs-sources-list');
    if (sourcesList) {
      var chips = document.querySelectorAll('.source-chip');
      var html = '';
      chips.forEach(function(chip) {
        var name = chip.querySelector('.source-name');
        var dot = chip.querySelector('.source-dot');
        var isActive = dot && dot.classList.contains('active');
        html += '<div class="rs-source-item">' +
          '<div class="rs-source-dot" style="background:' + (isActive ? '#22c55e' : '#ef4444') + '"></div>' +
          '<span class="rs-source-name">' + (name ? name.textContent : '') + '</span>' +
          '</div>';
      });
      sourcesList.innerHTML = html;
    }
  }

  // --- CRM ---
  var CRM_API = '/api/crm.php';
  var crmCurrentTab = 'clients';
  var crmCurrentStatus = '';
  var crmLoaded = false;

  function initCRM() {
    // Tab switching
    document.querySelectorAll('.rs-crm-tab').forEach(function(tab) {
      tab.addEventListener('click', function() {
        crmCurrentTab = tab.dataset.crmTab;
        document.querySelectorAll('.rs-crm-tab').forEach(function(t) { t.classList.remove('active'); });
        tab.classList.add('active');
        // Show/hide status filter (only for clients)
        var sf = document.getElementById('rs-crm-status-filter');
        if (sf) sf.style.display = crmCurrentTab === 'clients' ? 'flex' : 'none';
        // Hide detail view
        showCrmList();
        loadCRM();
      });
    });

    // Status filter
    document.querySelectorAll('.rs-crm-sf').forEach(function(btn) {
      btn.addEventListener('click', function() {
        crmCurrentStatus = btn.dataset.status;
        document.querySelectorAll('.rs-crm-sf').forEach(function(b) { b.classList.remove('active'); });
        btn.classList.add('active');
        loadCRM();
      });
    });

    // Search
    var searchInput = document.getElementById('rs-crm-search');
    var searchTimeout = null;
    if (searchInput) {
      searchInput.addEventListener('input', function() {
        if (searchTimeout) clearTimeout(searchTimeout);
        searchTimeout = setTimeout(function() { loadCRM(); }, 400);
      });
    }

    // Add button
    var addBtn = document.getElementById('rs-crm-add-btn');
    if (addBtn) {
      addBtn.addEventListener('click', function() {
        if (crmCurrentTab === 'clients') toggleCrmForm();
      });
    }

    // Form cancel/submit
    var cancelBtn = document.getElementById('rs-crm-f-cancel');
    if (cancelBtn) cancelBtn.addEventListener('click', function() { toggleCrmForm(false); });
    var submitBtn = document.getElementById('rs-crm-f-submit');
    if (submitBtn) submitBtn.addEventListener('click', function() { submitCrmClient(); });
    var nomInput = document.getElementById('rs-crm-f-nom');
    if (nomInput) nomInput.addEventListener('keydown', function(e) { if (e.key === 'Enter') submitCrmClient(); });
  }

  function loadCRM() {
    var list = document.getElementById('rs-crm-list');
    if (!list) return;
    list.innerHTML = '<div class="rs-tasks-loading">Chargement...</div>';

    var search = (document.getElementById('rs-crm-search') || {}).value || '';

    if (crmCurrentTab === 'clients') {
      var url = CRM_API + '?action=clients';
      if (search) url += '&search=' + encodeURIComponent(search);
      if (crmCurrentStatus) url += '&status=' + encodeURIComponent(crmCurrentStatus);

      fetch(url).then(function(r) { return r.json(); }).then(function(data) {
        crmLoaded = true;
        if (!data.clients || data.clients.length === 0) {
          list.innerHTML = '<div class="rs-tasks-empty">Aucun client trouve</div>';
          return;
        }
        renderClientsList(data.clients, list);
        if (data.counts) renderCrmStats(data.counts);
      }).catch(function() {
        list.innerHTML = '<div class="rs-tasks-empty">Erreur chargement CRM</div>';
      });

    } else if (crmCurrentTab === 'projets') {
      fetch(CRM_API + '?action=projets').then(function(r) { return r.json(); }).then(function(data) {
        if (!data.projets || data.projets.length === 0) {
          list.innerHTML = '<div class="rs-tasks-empty">Aucun projet</div>';
          return;
        }
        renderProjetsList(data.projets, list);
      }).catch(function() {
        list.innerHTML = '<div class="rs-tasks-empty">Erreur chargement projets</div>';
      });

    } else if (crmCurrentTab === 'paiements') {
      fetch(CRM_API + '?action=paiements').then(function(r) { return r.json(); }).then(function(data) {
        if (!data.paiements || data.paiements.length === 0) {
          list.innerHTML = '<div class="rs-tasks-empty">Aucun paiement</div>';
          return;
        }
        renderPaiementsList(data.paiements, list);
      }).catch(function() {
        list.innerHTML = '<div class="rs-tasks-empty">Erreur chargement paiements</div>';
      });
    }
  }

  function renderCrmStats(counts) {
    var el = document.getElementById('rs-crm-stats');
    if (!el) return;
    var total = 0;
    Object.values(counts).forEach(function(v) { total += v; });
    el.innerHTML = '<div class="rs-crm-stat-row">' +
      '<div class="rs-crm-stat-box"><div class="rs-crm-stat-num">' + total + '</div><div class="rs-crm-stat-lbl">Total</div></div>' +
      '<div class="rs-crm-stat-box rs-stat-green"><div class="rs-crm-stat-num">' + (counts['Actif'] || 0) + '</div><div class="rs-crm-stat-lbl">Actifs</div></div>' +
      '<div class="rs-crm-stat-box rs-stat-blue"><div class="rs-crm-stat-num">' + (counts['Prospect'] || 0) + '</div><div class="rs-crm-stat-lbl">Prospects</div></div>' +
      '<div class="rs-crm-stat-box rs-stat-gray"><div class="rs-crm-stat-num">' + (counts['Inactif'] || 0) + '</div><div class="rs-crm-stat-lbl">Inactifs</div></div>' +
      '</div>';
  }

  var statusColors = {
    'Actif': '#22c55e', 'En essai': '#f59e0b', 'Prospect': '#6366f1',
    'Inactif': '#64748b', "Liste d'attente": '#94a3b8'
  };

  function renderClientsList(clients, container) {
    var html = '';
    clients.forEach(function(c) {
      var color = statusColors[c.status] || '#64748b';
      var initials = (c.nom || '?').split(' ').map(function(w) { return w.charAt(0); }).join('').substring(0, 2).toUpperCase();
      html += '<div class="rs-crm-item" data-client-id="' + c.id + '">' +
        '<div class="rs-crm-avatar" style="background:' + color + '20;color:' + color + '">' + initials + '</div>' +
        '<div class="rs-crm-item-info">' +
          '<div class="rs-crm-item-name">' + escapeHtml(c.nom) + '</div>' +
          '<div class="rs-crm-item-meta">' +
            '<span class="rs-crm-badge" style="background:' + color + '25;color:' + color + '">' + escapeHtml(c.status || '') + '</span>' +
            (c.societe ? ' <span class="rs-crm-meta-text">' + escapeHtml(c.societe) + '</span>' : '') +
          '</div>' +
        '</div>' +
        '</div>';
    });
    container.innerHTML = html;
    container.querySelectorAll('.rs-crm-item[data-client-id]').forEach(function(item) {
      item.addEventListener('click', function() { loadClientDetail(item.dataset.clientId); });
    });
  }

  function renderProjetsList(projets, container) {
    var statusIcons = { 'En cours': '#22c55e', 'Actif': '#22c55e', 'À démarrer': '#6366f1', 'Bloqué': '#ef4444', 'En attente': '#f59e0b', 'En review': '#f59e0b', 'Terminé': '#64748b' };
    var html = '';
    projets.forEach(function(p) {
      var color = statusIcons[p.status] || '#64748b';
      html += '<div class="rs-crm-item">' +
        '<div class="rs-crm-avatar rs-crm-av-sm" style="background:' + color + '20;color:' + color + '">P</div>' +
        '<div class="rs-crm-item-info">' +
          '<div class="rs-crm-item-name">' + escapeHtml(p.nom) + '</div>' +
          '<div class="rs-crm-item-meta">' +
            '<span class="rs-crm-badge" style="background:' + color + '25;color:' + color + '">' + escapeHtml(p.status || '') + '</span>' +
            (p.client_nom ? ' <span class="rs-crm-meta-text">' + escapeHtml(p.client_nom) + '</span>' : '') +
            (p.budget ? ' <span class="rs-crm-meta-text">' + Number(p.budget).toLocaleString('fr-FR') + '\u20ac</span>' : '') +
          '</div>' +
        '</div>' +
        '</div>';
    });
    container.innerHTML = html;
  }

  function renderPaiementsList(paiements, container) {
    var statutColors = { 'En retard': '#ef4444', 'En attente': '#f59e0b', 'Partiel': '#f59e0b', 'Payé': '#22c55e', 'Annulé': '#64748b', 'En réflexion': '#6366f1' };
    var html = '';
    paiements.forEach(function(p) {
      var color = statutColors[p.statut] || '#64748b';
      var montant = p.montant_attendu ? Number(p.montant_attendu).toLocaleString('fr-FR') + '\u20ac' : '--';
      html += '<div class="rs-crm-item">' +
        '<div class="rs-crm-avatar rs-crm-av-sm" style="background:' + color + '20;color:' + color + '">\u20ac</div>' +
        '<div class="rs-crm-item-info">' +
          '<div class="rs-crm-item-name">' + escapeHtml(p.label) + '</div>' +
          '<div class="rs-crm-item-meta">' +
            '<span class="rs-crm-badge" style="background:' + color + '25;color:' + color + '">' + escapeHtml(p.statut || '') + '</span>' +
            ' <span class="rs-crm-meta-text">' + montant + '</span>' +
            (p.client_nom ? ' <span class="rs-crm-meta-text">' + escapeHtml(p.client_nom) + '</span>' : '') +
          '</div>' +
        '</div>' +
        '</div>';
    });
    container.innerHTML = html;
  }

  function loadClientDetail(clientId) {
    var detail = document.getElementById('rs-crm-detail');
    var list = document.getElementById('rs-crm-list');
    var toolbar = document.getElementById('rs-crm-status-filter');
    if (!detail || !list) return;

    list.style.display = 'none';
    if (toolbar) toolbar.style.display = 'none';
    detail.style.display = 'block';
    detail.innerHTML = '<div class="rs-tasks-loading">Chargement fiche...</div>';

    fetch(CRM_API + '?action=client&id=' + clientId).then(function(r) { return r.json(); }).then(function(data) {
      if (data.error) { detail.innerHTML = '<div class="rs-tasks-empty">' + escapeHtml(data.error) + '</div>'; return; }
      var c = data.client;
      var color = statusColors[c.status] || '#64748b';
      var initials = (c.nom || '?').split(' ').map(function(w) { return w.charAt(0); }).join('').substring(0, 2).toUpperCase();

      var html = '<div class="rs-crm-detail-header">' +
        '<button class="rs-crm-back" id="rs-crm-back">&larr;</button>' +
        '<div class="rs-crm-avatar rs-crm-av-lg" style="background:' + color + '20;color:' + color + '">' + initials + '</div>' +
        '<div class="rs-crm-detail-name">' + escapeHtml(c.nom) + '</div>' +
        '<span class="rs-crm-badge" style="background:' + color + '25;color:' + color + '">' + escapeHtml(c.status) + '</span>' +
        '</div>';

      // Info fields
      html += '<div class="rs-crm-fields">';
      if (c.societe) html += '<div class="rs-crm-field"><span class="rs-crm-field-lbl">Societe</span><span class="rs-crm-field-val">' + escapeHtml(c.societe) + '</span></div>';
      if (c.email) html += '<div class="rs-crm-field"><span class="rs-crm-field-lbl">Email</span><span class="rs-crm-field-val">' + escapeHtml(c.email) + '</span></div>';
      if (c.telephone) html += '<div class="rs-crm-field"><span class="rs-crm-field-lbl">Tel</span><span class="rs-crm-field-val">' + escapeHtml(c.telephone) + '</span></div>';
      if (c.abonnement) html += '<div class="rs-crm-field"><span class="rs-crm-field-lbl">Abo</span><span class="rs-crm-field-val">' + escapeHtml(c.abonnement) + '</span></div>';
      if (c.canal) html += '<div class="rs-crm-field"><span class="rs-crm-field-lbl">Canal</span><span class="rs-crm-field-val">' + escapeHtml(c.canal) + '</span></div>';
      if (c.agent_assigne) html += '<div class="rs-crm-field"><span class="rs-crm-field-lbl">Agent</span><span class="rs-crm-field-val">' + escapeHtml(c.agent_assigne) + '</span></div>';
      if (c.notes) html += '<div class="rs-crm-field rs-crm-field-full"><span class="rs-crm-field-lbl">Notes</span><span class="rs-crm-field-val rs-crm-notes">' + escapeHtml(c.notes) + '</span></div>';
      html += '</div>';

      // Inline edit status
      html += '<div class="rs-crm-inline-edit">' +
        '<select class="rs-task-select rs-crm-edit-status" id="rs-crm-edit-status" data-client-id="' + c.id + '">' +
        '<option' + (c.status === 'Prospect' ? ' selected' : '') + '>Prospect</option>' +
        '<option' + (c.status === 'En essai' ? ' selected' : '') + '>En essai</option>' +
        '<option' + (c.status === 'Actif' ? ' selected' : '') + '>Actif</option>' +
        '<option' + (c.status === 'Inactif' ? ' selected' : '') + '>Inactif</option>' +
        '<option' + (c.status === "Liste d\'attente" ? ' selected' : '') + ">Liste d'attente</option>" +
        '</select>' +
        '<button class="rs-task-delete rs-crm-del-btn" id="rs-crm-del-client" data-client-id="' + c.id + '" title="Supprimer" style="opacity:1">&times;</button>' +
        '</div>';

      // Projets
      if (data.projets && data.projets.length > 0) {
        html += '<div class="rs-section-title" style="margin-top:12px">Projets (' + data.projets.length + ')</div>';
        data.projets.forEach(function(p) {
          var pc = statusColors[p.status] || '#64748b';
          html += '<div class="rs-crm-sub-item"><span class="rs-crm-badge" style="background:' + pc + '25;color:' + pc + '">' + escapeHtml(p.status || '') + '</span> ' + escapeHtml(p.nom) +
            (p.budget ? ' <span class="rs-crm-meta-text">' + Number(p.budget).toLocaleString('fr-FR') + '\u20ac</span>' : '') + '</div>';
        });
      }

      // Paiements
      if (data.paiements && data.paiements.length > 0) {
        html += '<div class="rs-section-title" style="margin-top:12px">Paiements (' + data.paiements.length + ')</div>';
        data.paiements.forEach(function(p) {
          var sc = { 'En retard': '#ef4444', 'En attente': '#f59e0b', 'Partiel': '#f59e0b', 'Payé': '#22c55e', 'Annulé': '#64748b' };
          var pc = sc[p.statut] || '#64748b';
          var m = p.montant_attendu ? Number(p.montant_attendu).toLocaleString('fr-FR') + '\u20ac' : '';
          html += '<div class="rs-crm-sub-item"><span class="rs-crm-badge" style="background:' + pc + '25;color:' + pc + '">' + escapeHtml(p.statut || '') + '</span> ' + escapeHtml(p.label) + (m ? ' <span class="rs-crm-meta-text">' + m + '</span>' : '') + '</div>';
        });
      }

      detail.innerHTML = html;

      // Back button
      var backBtn = document.getElementById('rs-crm-back');
      if (backBtn) backBtn.addEventListener('click', function() { showCrmList(); loadCRM(); });

      // Status change
      var statusSel = document.getElementById('rs-crm-edit-status');
      if (statusSel) {
        statusSel.addEventListener('change', function() {
          fetch(CRM_API + '?action=client&id=' + statusSel.dataset.clientId, {
            method: 'PATCH',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ status: statusSel.value })
          }).then(function(r) { return r.json(); }).then(function(d) {
            if (d.success) loadClientDetail(statusSel.dataset.clientId);
          });
        });
      }

      // Delete button
      var delBtn = document.getElementById('rs-crm-del-client');
      if (delBtn) {
        delBtn.addEventListener('click', function() {
          if (!confirm('Supprimer ce client ?')) return;
          fetch(CRM_API + '?action=client&id=' + delBtn.dataset.clientId, { method: 'DELETE' })
            .then(function(r) { return r.json(); })
            .then(function(d) { if (d.success) { showCrmList(); loadCRM(); } });
        });
      }
    }).catch(function() {
      detail.innerHTML = '<div class="rs-tasks-empty">Erreur chargement fiche</div>';
    });
  }

  function showCrmList() {
    var detail = document.getElementById('rs-crm-detail');
    var list = document.getElementById('rs-crm-list');
    var sf = document.getElementById('rs-crm-status-filter');
    if (detail) detail.style.display = 'none';
    if (list) list.style.display = 'block';
    if (sf && crmCurrentTab === 'clients') sf.style.display = 'flex';
  }

  function toggleCrmForm(show) {
    var form = document.getElementById('rs-crm-form');
    if (!form) return;
    if (show === undefined) show = form.style.display === 'none';
    form.style.display = show ? 'block' : 'none';
    if (show) {
      var nomInput = document.getElementById('rs-crm-f-nom');
      if (nomInput) { nomInput.value = ''; nomInput.focus(); }
      ['rs-crm-f-email', 'rs-crm-f-tel', 'rs-crm-f-societe'].forEach(function(id) {
        var el = document.getElementById(id);
        if (el) el.value = '';
      });
    }
  }

  function submitCrmClient() {
    var nom = (document.getElementById('rs-crm-f-nom').value || '').trim();
    if (!nom) return;

    var body = {
      nom: nom,
      email: (document.getElementById('rs-crm-f-email').value || '').trim() || null,
      telephone: (document.getElementById('rs-crm-f-tel').value || '').trim() || null,
      societe: (document.getElementById('rs-crm-f-societe').value || '').trim() || null,
      status: document.getElementById('rs-crm-f-status').value,
      abonnement: document.getElementById('rs-crm-f-abo').value || null
    };

    var btn = document.getElementById('rs-crm-f-submit');
    if (btn) { btn.disabled = true; btn.textContent = '...'; }

    fetch(CRM_API + '?action=client', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(body)
    }).then(function(r) { return r.json(); }).then(function(data) {
      if (data.success) {
        toggleCrmForm(false);
        loadCRM();
      } else {
        alert(data.error || 'Erreur');
      }
    }).catch(function(err) {
      alert('Erreur: ' + err.message);
    }).finally(function() {
      if (btn) { btn.disabled = false; btn.textContent = 'Ajouter'; }
    });
  }

  // --- Tasks ---
  var tasksLoaded = false;
  var currentFilter = 'today';

  function loadTasks(filter) {
    if (filter) currentFilter = filter;
    var list = document.getElementById('rs-tasks-list');
    var dateEl = document.getElementById('rs-tasks-date');
    if (!list) return;

    // Set header text
    var today = new Date();
    var options = { weekday: 'long', day: 'numeric', month: 'long' };
    var labels = { today: "Aujourd'hui", overdue: 'En retard', upcoming: 'A venir', unplanned: 'Non planifiees', all: 'Toutes les taches' };
    if (dateEl) {
      dateEl.textContent = labels[currentFilter] || today.toLocaleDateString('fr-FR', options);
    }

    // Update filter buttons
    document.querySelectorAll('.rs-filter-btn').forEach(function(btn) {
      btn.classList.toggle('active', btn.dataset.filter === currentFilter);
    });

    list.innerHTML = '<div class="rs-tasks-loading">Chargement...</div>';

    fetch(TASKS_API_URL + '?filter=' + currentFilter)
      .then(function(r) {
        if (!r.ok) throw new Error('HTTP ' + r.status);
        return r.json();
      })
      .then(function(data) {
        tasksLoaded = true;

        // Update badges
        if (data.counts) {
          var bToday = document.getElementById('badge-today');
          var bOverdue = document.getElementById('badge-overdue');
          var bUpcoming = document.getElementById('badge-upcoming');
          if (bToday) bToday.textContent = data.counts.today || 0;
          if (bOverdue) bOverdue.textContent = data.counts.overdue || 0;
          if (bUpcoming) bUpcoming.textContent = data.counts.upcoming || 0;
          var bUnplanned = document.getElementById('badge-unplanned');
          if (bUnplanned) bUnplanned.textContent = data.counts.unplanned || 0;
        }

        if (!data.tasks || data.tasks.length === 0) {
          var emptyMsg = {
            today: 'Aucune tache pour aujourd\'hui',
            overdue: 'Aucune tache en retard',
            upcoming: 'Aucune tache a venir',
            unplanned: 'Aucune tache non planifiee',
            all: 'Aucune tache'
          };
          list.innerHTML = '<div class="rs-tasks-empty">' + (emptyMsg[currentFilter] || 'Aucune tache') + '</div>';
          return;
        }

        var html = '';
        data.tasks.forEach(function(task) {
          var priorityClass = 'low';
          if (task.priority === 'Urgente' || task.priority === 'Haute') priorityClass = 'high';
          else if (task.priority === 'Normale' || task.priority === 'Moyenne') priorityClass = 'medium';

          var dateHtml = task.due
            ? '<span class="rs-task-date-edit" data-task-id="' + task.id + '" data-raw="' + escapeHtml(task.dueRaw || '') + '" title="Cliquer pour modifier la date">' + escapeHtml(task.due) + '</span>'
            : '<span class="rs-task-quick-dates" data-task-id="' + task.id + '">' +
                '<button class="rs-quick-date" data-action="today" title="Planifier aujourd\'hui">Auj.</button>' +
                '<button class="rs-quick-date" data-action="tomorrow" title="Planifier demain">Demain</button>' +
                '<button class="rs-quick-date" data-action="pick" title="Choisir une date">&#128197;</button>' +
              '</span>';

          html += '<div class="rs-task-item" data-task-id="' + task.id + '">' +
            '<div class="rs-task-check" title="Marquer comme fait"></div>' +
            '<div class="rs-task-info">' +
              '<div class="rs-task-title">' + escapeHtml(task.title || '') + '</div>' +
              '<div class="rs-task-meta">' +
                '<span class="rs-task-priority ' + priorityClass + '"></span> ' +
                escapeHtml(task.priority || '') +
                ' &middot; ' + dateHtml +
              '</div>' +
            '</div>' +
            '<button class="rs-task-delete" title="Supprimer" data-task-id="' + task.id + '">&times;</button>' +
            '</div>';
        });
        list.innerHTML = html;

        // Attach event handlers
        list.querySelectorAll('.rs-task-check').forEach(function(check) {
          check.addEventListener('click', function() {
            completeTask(check.closest('.rs-task-item'));
          });
        });

        list.querySelectorAll('.rs-task-delete').forEach(function(btn) {
          btn.addEventListener('click', function(e) {
            e.stopPropagation();
            deleteTask(btn.dataset.taskId, btn.closest('.rs-task-item'));
          });
        });

        // Inline date editing (tasks with existing date)
        list.querySelectorAll('.rs-task-date-edit').forEach(function(el) {
          el.addEventListener('click', function(e) {
            e.stopPropagation();
            editTaskDate(el);
          });
        });

        // Quick date buttons (tasks without date)
        list.querySelectorAll('.rs-quick-date').forEach(function(btn) {
          btn.addEventListener('click', function(e) {
            e.stopPropagation();
            var taskId = btn.closest('.rs-task-quick-dates').dataset.taskId;
            var action = btn.dataset.action;
            if (action === 'pick') {
              // Replace with date input
              var span = btn.closest('.rs-task-quick-dates');
              var fakeEl = document.createElement('span');
              fakeEl.dataset.taskId = taskId;
              fakeEl.dataset.raw = '';
              span.replaceWith(fakeEl);
              editTaskDate(fakeEl);
            } else {
              var d = new Date();
              if (action === 'tomorrow') d.setDate(d.getDate() + 1);
              var iso = d.getFullYear() + '-' + String(d.getMonth()+1).padStart(2,'0') + '-' + String(d.getDate()).padStart(2,'0');
              quickSetDate(taskId, iso, btn.closest('.rs-task-item'));
            }
          });
        });
      })
      .catch(function(err) {
        console.error('Tasks load error:', err);
        list.innerHTML = '<div class="rs-tasks-empty">Impossible de charger les taches.<br><small style="color:#64748b">Verifiez la connexion PostgreSQL.</small></div>';
        tasksLoaded = true;
      });
  }

  function completeTask(itemEl) {
    if (!itemEl) return;
    var taskId = itemEl.dataset.taskId;

    // Visual feedback immediately
    itemEl.classList.add('done');
    itemEl.style.opacity = '0.5';

    fetch(TASKS_API_URL + '?id=' + taskId, {
      method: 'PATCH',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ status: 'Terminé' })
    })
    .then(function(r) { return r.json(); })
    .then(function(data) {
      if (data.success) {
        // Animate out then remove
        itemEl.style.transition = 'opacity 0.4s, transform 0.4s, max-height 0.4s';
        itemEl.style.opacity = '0';
        itemEl.style.transform = 'translateX(20px)';
        itemEl.style.maxHeight = '0';
        itemEl.style.marginBottom = '0';
        itemEl.style.padding = '0 12px';
        itemEl.style.overflow = 'hidden';
        setTimeout(function() {
          itemEl.remove();
          // Refresh to update counts
          loadTasks();
        }, 450);
      }
    })
    .catch(function() {
      itemEl.classList.remove('done');
      itemEl.style.opacity = '1';
    });
  }

  function deleteTask(taskId, itemEl) {
    if (!confirm('Supprimer cette tache ?')) return;

    if (itemEl) {
      itemEl.style.opacity = '0.3';
    }

    fetch(TASKS_API_URL + '?id=' + taskId, { method: 'DELETE' })
      .then(function(r) { return r.json(); })
      .then(function(data) {
        if (data.success) {
          if (itemEl) {
            itemEl.style.transition = 'opacity 0.3s, transform 0.3s, max-height 0.3s';
            itemEl.style.opacity = '0';
            itemEl.style.transform = 'translateX(-20px)';
            itemEl.style.maxHeight = '0';
            itemEl.style.marginBottom = '0';
            itemEl.style.padding = '0 12px';
            itemEl.style.overflow = 'hidden';
            setTimeout(function() {
              itemEl.remove();
              loadTasks();
            }, 350);
          } else {
            loadTasks();
          }
        }
      })
      .catch(function() {
        if (itemEl) itemEl.style.opacity = '1';
      });
  }

  function quickSetDate(taskId, dateStr, itemEl) {
    if (itemEl) itemEl.style.opacity = '0.5';
    fetch(TASKS_API_URL + '?id=' + taskId, {
      method: 'PATCH',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ deadline: dateStr })
    })
    .then(function(r) { return r.json(); })
    .then(function(data) {
      if (data.success) {
        if (itemEl) {
          itemEl.style.transition = 'opacity 0.3s, transform 0.3s';
          itemEl.style.opacity = '0';
          itemEl.style.transform = 'translateX(20px)';
          setTimeout(function() { loadTasks(); }, 300);
        } else {
          loadTasks();
        }
      }
    })
    .catch(function() { if (itemEl) itemEl.style.opacity = '1'; });
  }

  function editTaskDate(el) {
    var taskId = el.dataset.taskId;
    var currentRaw = el.dataset.raw || '';
    // Replace the span with an inline date input
    var input = document.createElement('input');
    input.type = 'date';
    input.className = 'rs-task-date-inline';
    input.value = currentRaw;
    input.style.cssText = 'font-size:11px;padding:2px 4px;border:1px solid var(--accent,#a78bfa);border-radius:4px;background:var(--bg-primary,#1a1f2e);color:var(--text-primary,#e2e8f0);width:120px;';
    el.replaceWith(input);
    input.focus();

    function save() {
      var newDate = input.value || null;
      fetch(TASKS_API_URL + '?id=' + taskId, {
        method: 'PATCH',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ deadline: newDate })
      })
      .then(function(r) { return r.json(); })
      .then(function(data) {
        if (data.success) loadTasks();
      })
      .catch(function() { loadTasks(); });
    }

    input.addEventListener('change', save);
    input.addEventListener('blur', function() {
      // Small delay to allow change to fire first
      setTimeout(function() { if (document.body.contains(input)) save(); }, 150);
    });
    input.addEventListener('keydown', function(e) {
      if (e.key === 'Escape') loadTasks();
    });
  }

  function toggleTaskForm(show) {
    var form = document.getElementById('rs-task-form');
    if (!form) return;
    if (show === undefined) show = form.style.display === 'none';
    form.style.display = show ? 'block' : 'none';
    if (show) {
      var titleInput = document.getElementById('rs-task-input-title');
      if (titleInput) { titleInput.value = ''; titleInput.focus(); }
      var prioSelect = document.getElementById('rs-task-input-priority');
      if (prioSelect) prioSelect.value = 'Normale';
      var deadlineInput = document.getElementById('rs-task-input-deadline');
      if (deadlineInput) deadlineInput.value = '';
    }
  }

  function submitNewTask() {
    var title = (document.getElementById('rs-task-input-title').value || '').trim();
    if (!title) return;

    var priority = document.getElementById('rs-task-input-priority').value;
    var deadline = document.getElementById('rs-task-input-deadline').value || null;

    var submitBtn = document.getElementById('rs-task-form-submit');
    if (submitBtn) { submitBtn.disabled = true; submitBtn.textContent = '...'; }

    fetch(TASKS_API_URL, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ title: title, priority: priority, deadline: deadline })
    })
    .then(function(r) { return r.json(); })
    .then(function(data) {
      if (data.success) {
        toggleTaskForm(false);
        loadTasks();
      } else {
        alert(data.error || 'Erreur lors de la creation');
      }
    })
    .catch(function(err) {
      alert('Erreur: ' + err.message);
    })
    .finally(function() {
      if (submitBtn) { submitBtn.disabled = false; submitBtn.textContent = 'Ajouter'; }
    });
  }

  function initTasks() {
    // Filter buttons
    document.querySelectorAll('.rs-filter-btn').forEach(function(btn) {
      btn.addEventListener('click', function() {
        loadTasks(btn.dataset.filter);
      });
    });

    // Refresh
    var refreshBtn = document.getElementById('rs-tasks-refresh');
    if (refreshBtn) {
      refreshBtn.addEventListener('click', function() { loadTasks(); });
    }

    // Add task button
    var addBtn = document.getElementById('rs-tasks-add-btn');
    if (addBtn) {
      addBtn.addEventListener('click', function() { toggleTaskForm(); });
    }

    // Form cancel
    var cancelBtn = document.getElementById('rs-task-form-cancel');
    if (cancelBtn) {
      cancelBtn.addEventListener('click', function() { toggleTaskForm(false); });
    }

    // Form submit
    var submitBtn = document.getElementById('rs-task-form-submit');
    if (submitBtn) {
      submitBtn.addEventListener('click', function() { submitNewTask(); });
    }

    // Enter key in title input
    var titleInput = document.getElementById('rs-task-input-title');
    if (titleInput) {
      titleInput.addEventListener('keydown', function(e) {
        if (e.key === 'Enter') { e.preventDefault(); submitNewTask(); }
      });
    }
  }

  // --- Calculator ---
  var calcState = { current: '0', previous: '', operator: '', resetNext: false };

  function initCalc() {
    var grid = document.querySelector('.calc-grid');
    var extras = document.querySelector('.calc-extras');
    if (!grid) return;

    grid.addEventListener('click', function(e) {
      var btn = e.target.closest('.calc-btn');
      if (!btn) return;
      handleCalcInput(btn.dataset.calc);
    });

    if (extras) {
      extras.addEventListener('click', function(e) {
        var btn = e.target.closest('.calc-btn');
        if (!btn) return;
        handleCalcInput(btn.dataset.calc);
      });
    }
  }

  function handleCalcInput(val) {
    var screen = document.getElementById('calc-screen');
    var history = document.getElementById('calc-history');
    if (!screen) return;

    switch (val) {
      case 'clear':
        calcState = { current: '0', previous: '', operator: '', resetNext: false };
        if (history) history.textContent = '';
        break;
      case 'backspace':
        if (calcState.current.length > 1) {
          calcState.current = calcState.current.slice(0, -1);
        } else {
          calcState.current = '0';
        }
        break;
      case 'percent':
        var pVal = parseFloat(calcState.current);
        if (!isNaN(pVal)) {
          if (calcState.previous && calcState.operator) {
            calcState.current = String(parseFloat(calcState.previous) * pVal / 100);
          } else {
            calcState.current = String(pVal / 100);
          }
        }
        break;
      case '+': case '-': case '*': case '/':
        if (calcState.operator && calcState.previous && !calcState.resetNext) {
          calcState.previous = String(calcCompute(parseFloat(calcState.previous), parseFloat(calcState.current), calcState.operator));
        } else {
          calcState.previous = calcState.current;
        }
        calcState.operator = val;
        calcState.resetNext = true;
        if (history) history.textContent = calcFormatNum(calcState.previous) + ' ' + calcOpSymbol(val);
        break;
      case '=':
        if (calcState.operator && calcState.previous) {
          var result = calcCompute(parseFloat(calcState.previous), parseFloat(calcState.current), calcState.operator);
          if (history) history.textContent = calcFormatNum(calcState.previous) + ' ' + calcOpSymbol(calcState.operator) + ' ' + calcFormatNum(calcState.current) + ' =';
          calcState.current = String(result);
          calcState.previous = '';
          calcState.operator = '';
          calcState.resetNext = true;
        }
        break;
      case 'tva20':
        var ttc20 = parseFloat(calcState.current) * 1.20;
        if (history) history.textContent = calcFormatNum(calcState.current) + ' + TVA 20% =';
        calcState.current = String(Math.round(ttc20 * 100) / 100);
        calcState.resetNext = true;
        break;
      case 'ht20':
        var ht20 = parseFloat(calcState.current) / 1.20;
        if (history) history.textContent = calcFormatNum(calcState.current) + ' HT (TVA 20%) =';
        calcState.current = String(Math.round(ht20 * 100) / 100);
        calcState.resetNext = true;
        break;
      case 'tva10':
        var ttc10 = parseFloat(calcState.current) * 1.10;
        if (history) history.textContent = calcFormatNum(calcState.current) + ' + TVA 10% =';
        calcState.current = String(Math.round(ttc10 * 100) / 100);
        calcState.resetNext = true;
        break;
      case '.':
        if (calcState.resetNext) { calcState.current = '0'; calcState.resetNext = false; }
        if (calcState.current.indexOf('.') === -1) {
          calcState.current += '.';
        }
        break;
      default:
        if (calcState.resetNext) { calcState.current = ''; calcState.resetNext = false; }
        if (calcState.current === '0' && val !== '0') {
          calcState.current = val;
        } else if (calcState.current !== '0' || val !== '0') {
          calcState.current += val;
        }
        break;
    }

    screen.textContent = calcFormatNum(calcState.current);
  }

  function calcCompute(a, b, op) {
    switch (op) {
      case '+': return a + b;
      case '-': return a - b;
      case '*': return a * b;
      case '/': return b !== 0 ? a / b : 0;
      default: return b;
    }
  }

  function calcOpSymbol(op) {
    switch (op) {
      case '+': return '+';
      case '-': return '\u2212';
      case '*': return '\u00d7';
      case '/': return '\u00f7';
      default: return op;
    }
  }

  function calcFormatNum(val) {
    var n = parseFloat(val);
    if (isNaN(n)) return val;
    if (String(val).endsWith('.')) return val;
    if (n === Math.floor(n) && !String(val).includes('.')) return n.toLocaleString('fr-FR');
    return n.toLocaleString('fr-FR', { minimumFractionDigits: 0, maximumFractionDigits: 6 });
  }

  // --- Helpers ---
  function escapeHtml(str) {
    return str.replace(/&/g, '&amp;').replace(/</g, '&lt;').replace(/>/g, '&gt;');
  }

  // --- Auto-update agent info ---
  function startAgentInfoUpdater() {
    setInterval(updateAgentInfo, 5000);
    updateAgentInfo();
  }

  // --- Init ---
  function init() {
    injectToolsPanel();
    initTabs();
    initToggle();
    initNotes();
    initCRM();
    initTasks();
    initCalc();
    startAgentInfoUpdater();
  }

  if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', init);
  } else {
    init();
  }

})();
