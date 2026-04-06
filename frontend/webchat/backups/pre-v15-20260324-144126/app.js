(function() {
  'use strict';

  // === Global Error Boundary ===
  var _errToastTimer;
  function _showErrorToast(msg) {
    var t = document.getElementById('error-toast');
    if (!t) {
      t = document.createElement('div');
      t.id = 'error-toast';
      t.style.cssText = 'position:fixed;bottom:24px;left:50%;transform:translateX(-50%);background:rgba(239,68,68,0.9);color:#fff;padding:10px 20px;border-radius:10px;font-size:13px;z-index:100000;max-width:90vw;text-align:center;opacity:0;transition:opacity .3s;pointer-events:none;';
      document.body.appendChild(t);
    }
    t.textContent = msg;
    t.style.opacity = '1';
    clearTimeout(_errToastTimer);
    _errToastTimer = setTimeout(function() { t.style.opacity = '0'; }, 5000);
  }
  window.onerror = function(msg, src, line) {
    console.error('[MyBotIA]', msg, src, line);
    _showErrorToast('Erreur inattendue — vérifiez la console');
    return true;
  };
  window.onunhandledrejection = function(e) {
    console.error('[MyBotIA] Unhandled promise:', e.reason);
    _showErrorToast('Erreur async — vérifiez la console');
  };

  // === Styled Modal System (replaces native alert/confirm/prompt) ===
  function _createModalOverlay() {
    var ov = document.createElement('div');
    ov.className = 'mbt-modal-overlay';
    document.body.appendChild(ov);
    requestAnimationFrame(function() { ov.classList.add('visible'); });
    return ov;
  }
  function _createModalBox(title) {
    var box = document.createElement('div');
    box.className = 'mbt-modal-box';
    var h = document.createElement('div');
    h.className = 'mbt-modal-title';
    h.textContent = title || '';
    box.appendChild(h);
    return box;
  }
  function _closeModal(ov, box) {
    ov.classList.remove('visible');
    box.classList.add('closing');
    setTimeout(function() { if (ov.parentNode) ov.parentNode.removeChild(ov); }, 250);
  }

  function mybotiaAlert(title, message) {
    return new Promise(function(resolve) {
      var ov = _createModalOverlay();
      var box = _createModalBox(title);
      var body = document.createElement('div');
      body.className = 'mbt-modal-body';
      body.innerHTML = message.replace(/\n/g, '<br>');
      box.appendChild(body);
      var actions = document.createElement('div');
      actions.className = 'mbt-modal-actions';
      var btn = document.createElement('button');
      btn.className = 'mbt-modal-btn primary';
      btn.textContent = 'OK';
      btn.onclick = function() { _closeModal(ov, box); resolve(); };
      actions.appendChild(btn);
      box.appendChild(actions);
      ov.appendChild(box);
      requestAnimationFrame(function() { box.classList.add('visible'); btn.focus(); });
    });
  }

  function mybotiaConfirm(title, message) {
    return new Promise(function(resolve) {
      var ov = _createModalOverlay();
      var box = _createModalBox(title);
      var body = document.createElement('div');
      body.className = 'mbt-modal-body';
      body.textContent = message;
      box.appendChild(body);
      var actions = document.createElement('div');
      actions.className = 'mbt-modal-actions';
      var cancelBtn = document.createElement('button');
      cancelBtn.className = 'mbt-modal-btn secondary';
      cancelBtn.textContent = 'Annuler';
      cancelBtn.onclick = function() { _closeModal(ov, box); resolve(false); };
      var okBtn = document.createElement('button');
      okBtn.className = 'mbt-modal-btn primary';
      okBtn.textContent = 'Confirmer';
      okBtn.onclick = function() { _closeModal(ov, box); resolve(true); };
      actions.appendChild(cancelBtn);
      actions.appendChild(okBtn);
      box.appendChild(actions);
      ov.appendChild(box);
      requestAnimationFrame(function() { box.classList.add('visible'); okBtn.focus(); });
      // ESC to cancel
      ov.addEventListener('keydown', function(e) { if (e.key === 'Escape') { _closeModal(ov, box); resolve(false); } });
    });
  }

  function mybotiaPrompt(title, defaultValue) {
    return new Promise(function(resolve) {
      var ov = _createModalOverlay();
      var box = _createModalBox(title);
      var input = document.createElement('input');
      input.type = 'text';
      input.className = 'mbt-modal-input';
      input.value = defaultValue || '';
      box.appendChild(input);
      var actions = document.createElement('div');
      actions.className = 'mbt-modal-actions';
      var cancelBtn = document.createElement('button');
      cancelBtn.className = 'mbt-modal-btn secondary';
      cancelBtn.textContent = 'Annuler';
      cancelBtn.onclick = function() { _closeModal(ov, box); resolve(null); };
      var okBtn = document.createElement('button');
      okBtn.className = 'mbt-modal-btn primary';
      okBtn.textContent = 'OK';
      okBtn.onclick = function() { _closeModal(ov, box); resolve(input.value); };
      actions.appendChild(cancelBtn);
      actions.appendChild(okBtn);
      box.appendChild(actions);
      ov.appendChild(box);
      requestAnimationFrame(function() { box.classList.add('visible'); input.focus(); input.select(); });
      input.addEventListener('keydown', function(e) { if (e.key === 'Enter') { _closeModal(ov, box); resolve(input.value); } if (e.key === 'Escape') { _closeModal(ov, box); resolve(null); } });
    });
  }


  // --- Config from URL params ---
  const params = new URLSearchParams(window.location.search);

  // --- Subdomain auto-detection ---
  var _subdomain = '';
  var _hostParts = window.location.hostname.split('.');
  if (_hostParts.length >= 3 && _hostParts[_hostParts.length - 2] === 'mybotia') {
    _subdomain = _hostParts[0].toLowerCase();
    if (_subdomain === 'app' || _subdomain === 'www') _subdomain = ''; // not agent subdomains
  }
  var _agentConfig = null; // will be set if subdomain matches

  // Token priority: URL param (?t=) for admin, otherwise fetched from ws-token.php
  var TOKEN = params.get('t') || '';
  var AGENT_NAME = params.get('name') || '';
  var AGENT_ROLE = params.get('role') || '';
  var SESSION_KEY = params.get('session') || localStorage.getItem('mybotia-session') || 'main';

  // --- Login screen refs ---
  var $loginScreen = document.getElementById('login-screen');
  var $loginEmail = document.getElementById('login-email');
  var $loginPassword = document.getElementById('login-password');
  var $loginBtn = document.getElementById('login-btn');
  var $loginError = document.getElementById('login-error');
  var $loginRemember = document.getElementById('login-remember');

  // --- Client state (populated after email login) ---
  var _clientInfo = null;      // {id, company_name, contact_name, plan, max_tokens, is_admin}
  var _collaborateurs = [];    // [{subdomain, name, role, is_default}]
  var _activeCollab = '';      // current subdomain
  var _authType = '';          // 'email' or 'token'

  function dismissSkeleton() {
    var sk = document.getElementById('skeleton-screen');
    if (sk) { sk.classList.add('hidden'); setTimeout(function() { if (sk.parentNode) sk.parentNode.removeChild(sk); }, 400); }
  }

  function showLogin() {
    dismissSkeleton();
    $loginScreen.classList.remove('hidden');
    if ($loginEmail) $loginEmail.value = '';
    if ($loginPassword) $loginPassword.value = '';
    $loginError.classList.remove('visible');
    if ($loginEmail) $loginEmail.focus();
  }

  function hideLogin() {
    dismissSkeleton();
    $loginScreen.classList.add('hidden');
  }

  function showLoginError(msg) {
    $loginError.textContent = msg;
    $loginError.classList.add('visible');
    $loginBtn.disabled = false;
    $loginBtn.innerHTML = 'Se connecter';
  }

  function attemptLogin() {
    var email = $loginEmail ? $loginEmail.value.trim() : '';
    var password = $loginPassword ? $loginPassword.value.trim() : '';
    if (!email || !password) {
      showLoginError('Veuillez entrer votre email et mot de passe.');
      return;
    }

    $loginBtn.disabled = true;
    $loginBtn.innerHTML = '<span class="login-spinner"></span>Connexion...';
    $loginError.classList.remove('visible');

    // Auth via email/password API
    fetch('/api/auth.php', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ email: email, password: password, subdomain: _subdomain })
    }).then(function(res) { return res.json(); }).then(function(data) {
      if (!data.ok) {
        showLoginError(data.error || 'Erreur de connexion');
        return;
      }
      // Store client state
      _authType = 'email';
      _clientInfo = data.client;
      _collaborateurs = data.collaborateurs || [];
      _activeCollab = data.active_collaborateur || '';
      SESSION_KEY = data.session_key || 'main';

      // Update sidebar with client info
      updateClientSidebar(data);

      // Remember login
      if ($loginRemember.checked) {
        localStorage.setItem('mybotia-auth-type', 'email');
      }

      hideLogin();
      loginPending = true;
      // Fetch token via secure endpoint then connect
      fetchGatewayToken(function(err) {
        if (err) { showLoginError('Erreur token gateway'); return; }
        connectWS();
      });
    }).catch(function(err) {
      showLoginError('Erreur réseau : ' + err.message);
    });
  }

  // Login button + Enter key
  $loginBtn.addEventListener('click', attemptLogin);
  if ($loginEmail) $loginEmail.addEventListener('keydown', function(e) {
    if (e.key === 'Enter') { e.preventDefault(); if ($loginPassword) $loginPassword.focus(); }
  });
  if ($loginPassword) $loginPassword.addEventListener('keydown', function(e) {
    if (e.key === 'Enter') { e.preventDefault(); attemptLogin(); }
  });

  var loginPending = false;

  // --- Shared: apply agent config to UI (avatar, name, cards, sources) ---
  function applyAgentConfig(agent) {
    if (!agent) return;
    _agentConfig = agent;
    AGENT_NAME = agent.displayName || agent.name || '';
    if (agent.session) SESSION_KEY = agent.session;

    // Header name & role
    if (AGENT_NAME) {
      if ($headerName) $headerName.textContent = AGENT_NAME;
      var $wt = document.getElementById('welcome-title');
      if ($wt) $wt.textContent = 'Bienvenue, je suis ' + AGENT_NAME;
    }
    if (agent.role && $headerRole) $headerRole.textContent = agent.role;

    // Avatar
    if (agent.avatar) {
      if ($headerAvatar) {
        $headerAvatar.textContent = '';
        var img = document.createElement('img');
        img.src = agent.avatar;
        img.alt = AGENT_NAME;
        img.onerror = function() { this.remove(); };
        $headerAvatar.appendChild(img);
      }
      var da = document.getElementById('dashboard-avatar');
      if (da) da.innerHTML = '<img src="' + agent.avatar + '" alt="' + AGENT_NAME + '" style="width:100%;height:100%;object-fit:cover;border-radius:50%;">';
    }

    // Dynamic cards or agent-specific UI
    if (agent.cards && agent.cards.length > 0 && typeof renderDynamicCards === 'function') {
      renderDynamicCards(agent.cards);
    } else if (_subdomain) {
      configureAgentUI(_subdomain);
    }
  }

  function loadAgentConfig(subdomain) {
    if (!subdomain) return Promise.resolve(null);
    return fetch('/config.php?sub=' + subdomain)
      .then(function(r) { if (!r.ok) throw new Error('not found'); return r.json(); })
      .then(function(agent) { applyAgentConfig(agent); return agent; })
      .catch(function() { configureAgentUI(subdomain); return null; });
  }

  // --- Init: check existing PHP session first, then subdomain, then token ---
  function initAuth() {
    // 1. If ?t=TOKEN in URL -> legacy token flow (admin/Gilles)
    if (params.get('t')) {
      _authType = 'token';
      TOKEN = params.get('t');
      hideLogin();
      if ($loginRemember && $loginRemember.checked && params.get('session')) {
        localStorage.setItem('mybotia-session', SESSION_KEY);
      }
      loadAgentConfig(_subdomain);
      connectWS();
      return;
    }

    // 2. Try to recover existing PHP session (email auth)
    fetch('/api/auth.php', { method: 'GET', credentials: 'same-origin' })
      .then(function(r) { return r.json(); })
      .then(function(data) {
        if (data.ok && data.auth_type === 'email') {
          // Recovered email session
          _authType = 'email';
          _clientInfo = data.client;
          _collaborateurs = data.collaborateurs || [];
          _activeCollab = data.active_collaborateur || '';
          SESSION_KEY = data.session_key || 'main';

          // CRITICAL: subdomain is the source of truth
          if (_subdomain && _subdomain !== _activeCollab) {
            var matchedCollab = null;
            _collaborateurs.forEach(function(c) {
              if (c.subdomain === _subdomain) matchedCollab = c;
            });
            if (matchedCollab) {
              _activeCollab = _subdomain;
              SESSION_KEY = 'agent:' + matchedCollab.agentId + ':main';
              fetch('/api/auth.php', {
                method: 'PATCH',
                headers: { 'Content-Type': 'application/json' },
                credentials: 'same-origin',
                body: JSON.stringify({ subdomain: _subdomain })
              }).catch(function() {});
            }
          }

          loadAgentConfig(_subdomain);
          updateClientSidebar(data);
          hideLogin();
          fetchGatewayToken(function(err) {
            if (err) { showLogin(); return; }
            connectWS();
          });
          return;
        }
        // 3. If subdomain, show login + pre-load agent UI
        if (_subdomain) {
          loadAgentConfig(_subdomain);
          setStatus('idle');
          showLogin();
          return;
        }
        // 4. Check localStorage token (legacy)
        if (TOKEN) {
          _authType = 'token';
          hideLogin();
          connectWS();
          return;
        }
        // 5. No auth -> show login
        setStatus('idle');
        showLogin();
      }).catch(function() {
        // PHP session check failed, fallback
        if (_subdomain) {
          loadAgentConfig(_subdomain);
          setStatus('idle');
          showLogin();
        } else if (TOKEN) {
          _authType = 'token';
          hideLogin();
          connectWS();
        } else {
          setStatus('idle');
          showLogin();
        }
      });
  }
  initAuth();

  // --- Auth session management (Sprint 3.2) ---
  function createAuthSession(token) {
    fetch('/api/auth.php', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ token: token })
    }).then(function(res) {
      if (res.ok) console.log('[auth] PHP session created');
    }).catch(function(err) {
      console.warn('[auth] Failed to create session:', err.message);
    });
  }

  function destroyAuthSession() {
    fetch('/api/auth.php', { method: 'DELETE' }).catch(function() {});
  }

  // Logout function
  function doLogout() {
    destroyAuthSession();
    TOKEN = '';
    SESSION_KEY = 'main';
    _clientInfo = null;
    _collaborateurs = [];
    _activeCollab = '';
    _authType = '';
    localStorage.removeItem('mybotia-token');
    localStorage.removeItem('mybotia-session');
    localStorage.removeItem('mybotia-auth-type');
    if (ws) { ws.close(); ws = null; }
    connected = false;
    setStatus('disconnected');
    // Clear URL params
    var cleanUrl = window.location.pathname;
    history.replaceState(null, '', cleanUrl);
    showLogin();
  }

  // --- DOM refs ---
  const $messages = document.getElementById('messages');
  const $welcome = document.getElementById('welcome');
  const $input = document.getElementById('chat-input');
  const $btnSend = document.getElementById('btn-send');
  const $btnStop = document.getElementById('btn-stop');
  const $typing = document.getElementById('typing');
  const $streaming = document.getElementById('streaming');
  const $streamingText = document.getElementById('streaming-text');
  const $statusDot = document.getElementById('status-dot');
  const $wsStatus = document.getElementById('ws-status');
  const $statusLabel = document.getElementById('status-label');
  const $reconnectBanner = document.getElementById('reconnect-banner');
  const $reconnectText = document.getElementById('reconnect-text');
  const $reconnectNowBtn = document.getElementById('reconnect-now-btn');
  const $statusPanel = document.getElementById('status-panel');
  const $statusPanelBody = document.getElementById('status-panel-body');
  const $statusPanelFooter = document.getElementById('status-panel-footer');
  const $statusPanelRefresh = document.getElementById('status-panel-refresh');

  // Manual reconnect button (Sprint 1.3)
  if ($reconnectNowBtn) $reconnectNowBtn.addEventListener('click', function() {
    if (reconnectTimer) {
      clearTimeout(reconnectTimer);
      reconnectTimer = null;
    }
    backoffMs = 800;
    setStatus('connecting');
    connectWS();
  });

  // --- Status panel logic ---
  var statusPanelOpen = false;

  function toggleStatusPanel() {
    if (!$statusPanel) return;
    statusPanelOpen = !statusPanelOpen;
    if (statusPanelOpen) {
      $statusPanel.classList.remove('hidden');
      fetchSystemStatus();
      // Close on outside click
      setTimeout(function() {
        document.addEventListener('click', closeStatusPanelOutside);
      }, 10);
    } else {
      $statusPanel.classList.add('hidden');
      document.removeEventListener('click', closeStatusPanelOutside);
    }
  }

  function closeStatusPanelOutside(e) {
    if ($statusPanel && !$statusPanel.contains(e.target) && !$statusDot.contains(e.target)) {
      statusPanelOpen = false;
      $statusPanel.classList.add('hidden');
      document.removeEventListener('click', closeStatusPanelOutside);
    }
  }

  function fetchSystemStatus() {
    if (!TOKEN || !$statusPanelBody) return;
    if ($statusPanelRefresh) {
      $statusPanelRefresh.classList.add('spinning');
    }
    $statusPanelBody.innerHTML = '<div class="status-panel-loading">Chargement...</div>';

    fetch('/api/status.php?t=' + encodeURIComponent(TOKEN))
      .then(function(res) { return res.json(); })
      .then(function(data) {
        if ($statusPanelRefresh) $statusPanelRefresh.classList.remove('spinning');
        if (!data.ok || !data.services) {
          $statusPanelBody.innerHTML = '<div class="status-panel-loading">Erreur de chargement</div>';
          return;
        }
        renderStatusPanel(data);
      })
      .catch(function(err) {
        if ($statusPanelRefresh) $statusPanelRefresh.classList.remove('spinning');
        $statusPanelBody.innerHTML = '<div class="status-panel-loading">Erreur : ' + err.message + '</div>';
      });
  }

  function renderStatusPanel(data) {
    if (!$statusPanelBody) return;
    var html = '';
    var services = data.services;
    var order = ['gateway', 'agent', 'database', 'php', 'ssl', 'disk', 'preferences'];
    
    // Add WS connection as first row (from JS state, not API)
    html += '<div class="svc-row">';
    html += '<div class="svc-dot ' + (connected ? 'ok' : 'error') + '"></div>';
    html += '<div class="svc-info">';
    html += '<div class="svc-label">Connexion WebSocket</div>';
    html += '<div class="svc-detail">' + (connected ? 'Active' : 'Déconnectée') + '</div>';
    html += '</div></div>';

    order.forEach(function(key) {
      var svc = services[key];
      if (!svc) return;
      html += '<div class="svc-row">';
      html += '<div class="svc-dot ' + svc.status + '"></div>';
      html += '<div class="svc-info">';
      html += '<div class="svc-label">' + svc.label + '</div>';
      html += '<div class="svc-detail">' + svc.detail + '</div>';
      html += '</div></div>';
    });

    $statusPanelBody.innerHTML = html;
    if ($statusPanelFooter) {
      var ts = new Date(data.timestamp);
      $statusPanelFooter.textContent = 'Vérifié à ' + ts.toLocaleTimeString('fr-FR');
    }
  }

  // Technical panel via settings menu (Sprint 4) — handled in account-menu section below

  // Refresh button
  if ($statusPanelRefresh) {
    $statusPanelRefresh.addEventListener('click', function(e) {
      e.stopPropagation();
      fetchSystemStatus();
    });
  }
  const $errorBanner = document.getElementById('error-banner');
  const $headerName = document.getElementById('header-name');
  const $headerRole = document.getElementById('header-role');
  const $headerAvatar = document.getElementById('header-avatar');
  const $welcomeTitle = document.getElementById('welcome-title');

  // --- Dashboard recreation (Sprint 4) ---
  function showDashboard() {
    // If welcome/dashboard already in DOM, skip
    if (document.getElementById('welcome')) return;
    var dash = document.createElement('div');
    dash.className = 'welcome';
    dash.id = 'welcome';
    dash.innerHTML = '<div class="dashboard-header">' +
      '<div class="dashboard-avatar" id="dashboard-avatar">' +
      '<img src="https://res.cloudinary.com/dniurvpzd/image/upload/v1772032713/Logo_Collaborateur_IA_coujhr.svg" alt="Collaborateur ia">' +
      '</div>' +
      '<h2 id="welcome-title">Bonjour, comment puis-je vous aider ?</h2>' +
      '<p id="welcome-text">Choisissez une action rapide ou posez directement votre question.</p>' +
      '</div>' +
      '<div class="dashboard-cards" id="suggestions">' +
      '<div class="dashboard-card" data-prompt="Quel est mon planning du jour ? Résume mes rendez-vous et tâches prioritaires.">' +
      '<div class="dashboard-card-icon"><svg viewBox="0 0 24 24" width="28" height="28" fill="none" stroke="currentColor" stroke-width="1.5"><rect x="3" y="4" width="18" height="18" rx="2"/><line x1="16" y1="2" x2="16" y2="6"/><line x1="8" y1="2" x2="8" y2="6"/><line x1="3" y1="10" x2="21" y2="10"/></svg></div>' +
      '<div class="dashboard-card-text"><div class="dashboard-card-title">Mon planning du jour</div><div class="dashboard-card-desc">Rendez-vous, tâches et priorités</div></div></div>' +
      '<div class="dashboard-card" data-prompt="Fais-moi un point complet : emails importants, dernières transactions bancaires, tâches en cours et prochains rendez-vous.">' +
      '<div class="dashboard-card-icon"><svg viewBox="0 0 24 24" width="28" height="28" fill="none" stroke="currentColor" stroke-width="1.5"><path d="M14 2H6a2 2 0 0 0-2 2v16a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2V8z"/><polyline points="14 2 14 8 20 8"/><line x1="16" y1="13" x2="8" y2="13"/><line x1="16" y1="17" x2="8" y2="17"/></svg></div>' +
      '<div class="dashboard-card-text"><div class="dashboard-card-title">Point complet</div><div class="dashboard-card-desc">Emails, banque, tâches et agenda</div></div></div>' +
      '<div class="dashboard-card" data-prompt="Lis mes derniers emails et résume-moi ceux qui nécessitent une action de ma part.">' +
      '<div class="dashboard-card-icon"><svg viewBox="0 0 24 24" width="28" height="28" fill="none" stroke="currentColor" stroke-width="1.5"><path d="M4 4h16c1.1 0 2 .9 2 2v12c0 1.1-.9 2-2 2H4c-1.1 0-2-.9-2-2V6c0-1.1.9-2 2-2z"/><polyline points="22,6 12,13 2,6"/></svg></div>' +
      '<div class="dashboard-card-text"><div class="dashboard-card-title">Mes emails urgents</div><div class="dashboard-card-desc">Résumé et actions nécessaires</div></div></div>' +
      '<div class="dashboard-card" data-prompt="Rédige un email professionnel adapté à mon contexte. Je vais te donner les détails.">' +
      '<div class="dashboard-card-icon"><svg viewBox="0 0 24 24" width="28" height="28" fill="none" stroke="currentColor" stroke-width="1.5"><path d="M11 4H4a2 2 0 0 0-2 2v14a2 2 0 0 0 2 2h14a2 2 0 0 0 2-2v-7"/><path d="M18.5 2.5a2.121 2.121 0 0 1 3 3L12 15l-4 1 1-4 9.5-9.5z"/></svg></div>' +
      '<div class="dashboard-card-text"><div class="dashboard-card-title">Rédiger un email</div><div class="dashboard-card-desc">Email professionnel sur mesure</div></div></div>' +
      '</div>';
    $messages.prepend(dash);
    // Rebind click handlers on new cards
    dash.querySelectorAll('.dashboard-card').forEach(function(card) {
      card.addEventListener('click', function() {
        var p = card.getAttribute('data-prompt');
        if (p && connected) { $input.value = p; sendMessage(); }
      });
    });
  }


  // --- Attachments ---
  const $fileInput = document.getElementById('file-input');
  const $btnAttach = document.getElementById('btn-attach');
  const $attachPreview = document.getElementById('attach-preview');
  let pendingAttachments = []; // { file, base64, mimeType, fileName }

  $btnAttach.addEventListener('click', function() {
    $fileInput.click();
  });

  $fileInput.addEventListener('change', function() {
    if (this.files) {
      Array.from(this.files).forEach(handleFile);
    }
    this.value = '';
  });

  // Drag & drop on messages area
  $messages.addEventListener('dragover', function(e) {
    e.preventDefault();
    $messages.classList.add('drag-over');
  });
  $messages.addEventListener('dragleave', function(e) {
    e.preventDefault();
    $messages.classList.remove('drag-over');
  });
  $messages.addEventListener('drop', function(e) {
    e.preventDefault();
    $messages.classList.remove('drag-over');
    if (e.dataTransfer && e.dataTransfer.files) {
      Array.from(e.dataTransfer.files).forEach(handleFile);
    }
  });

  // Paste image
  document.addEventListener('paste', function(e) {
    if (!e.clipboardData || !e.clipboardData.items) return;
    Array.from(e.clipboardData.items).forEach(function(item) {
      if (item.type.startsWith('image/')) {
        var file = item.getAsFile();
        if (file) handleFile(file);
      }
    });
  });

  // Max ~350Ko raw = ~470Ko base64 (gateway limit 512Ko per WS frame)
  var MAX_IMAGE_BYTES = 4000000; // 4MB (WS limit = 25MB)
  var MAX_IMAGE_DIM = 1200;

  function handleFile(file) {
    var imageTypes = ['image/png', 'image/jpeg', 'image/gif', 'image/webp'];
    var documentTypes = ['application/pdf', 'application/msword',
      'application/vnd.openxmlformats-officedocument.wordprocessingml.document',
      'application/vnd.ms-excel',
      'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet',
      'text/plain', 'text/csv', 'application/zip'];
    var isImage = imageTypes.indexOf(file.type) !== -1;
    var isDocument = documentTypes.indexOf(file.type) !== -1;
    if (!isImage && !isDocument) {
      showError('Type non support\u00e9 (images, PDF, Word, Excel, CSV, TXT)');
      setTimeout(hideError, 3000);
      return;
    }
    if (file.size > 25 * 1024 * 1024) {
      showError('Fichier trop volumineux (max 25 Mo)');
      setTimeout(hideError, 3000);
      return;
    }
    if (isDocument) {
      uploadFileToServer(file);
      return;
    }
    // Image: if small enough JPEG, send directly
    if (file.size <= MAX_IMAGE_BYTES && file.type === 'image/jpeg') {
      var reader = new FileReader();
      reader.onload = function(e) {
        addAttachmentFromDataUrl(e.target.result, file.name, file.type);
      };
      reader.readAsDataURL(file);
      return;
    }
    // Otherwise compress via canvas
    compressImage(file, function(dataUrl) {
      addAttachmentFromDataUrl(dataUrl, file.name, 'image/jpeg');
    });
  }

  function addAttachmentFromDataUrl(dataUrl, fileName, mimeType) {
    var base64 = dataUrl.split(',')[1];
    pendingAttachments.push({
      base64: base64,
      mimeType: mimeType,
      fileName: fileName,
      dataUrl: dataUrl
    });
    renderAttachPreviews();
  }

  function compressImage(file, callback) {
    var img = new Image();
    img.onload = function() {
      var w = img.width;
      var h = img.height;
      // Resize if too large
      if (w > MAX_IMAGE_DIM || h > MAX_IMAGE_DIM) {
        var ratio = Math.min(MAX_IMAGE_DIM / w, MAX_IMAGE_DIM / h);
        w = Math.round(w * ratio);
        h = Math.round(h * ratio);
      }
      var canvas = document.createElement('canvas');
      canvas.width = w;
      canvas.height = h;
      var ctx = canvas.getContext('2d');
      ctx.drawImage(img, 0, 0, w, h);

      // Try quality levels until under limit
      var quality = 0.85;
      var dataUrl;
      do {
        dataUrl = canvas.toDataURL('image/jpeg', quality);
        var size = Math.round(dataUrl.split(',')[1].length * 0.75);
        if (size <= MAX_IMAGE_BYTES) break;
        quality -= 0.1;
      } while (quality > 0.2);

      callback(dataUrl);
      URL.revokeObjectURL(img.src);
    };
    img.onerror = function() {
      showError('Impossible de lire cette image');
      setTimeout(hideError, 3000);
    };
    img.src = URL.createObjectURL(file);
  }

  // --- Upload document (PDF, Word, Excel, etc.) to server ---
  function uploadFileToServer(file) {
    // Add a placeholder attachment immediately (shows uploading state)
    var placeholderIdx = pendingAttachments.length;
    pendingAttachments.push({
      type: 'document',
      fileName: file.name,
      mimeType: file.type,
      uploading: true,
      filePath: null,
      fileSize: file.size
    });
    renderAttachPreviews();

    // Upload via multipart form to our PHP endpoint
    var formData = new FormData();
    formData.append('file', file);

    fetch('/api/upload.php', {
      method: 'POST',
      body: formData
    })
    .then(function(res) { return res.json(); })
    .then(function(data) {
      if (data.success && data.file) {
        // Update the placeholder with real path
        pendingAttachments[placeholderIdx].uploading = false;
        pendingAttachments[placeholderIdx].filePath = data.file.path;
        pendingAttachments[placeholderIdx].fileSize = data.file.size;
        renderAttachPreviews();
      } else {
        // Remove placeholder on error
        pendingAttachments.splice(placeholderIdx, 1);
        renderAttachPreviews();
        showError('Erreur upload: ' + (data.error || 'Erreur inconnue'));
        setTimeout(hideError, 4000);
      }
    })
    .catch(function(err) {
      // Remove placeholder on network error
      pendingAttachments.splice(placeholderIdx, 1);
      renderAttachPreviews();
      showError('Erreur réseau pendant l\'upload');
      setTimeout(hideError, 4000);
    });
  }

  function renderAttachPreviews() {
    $attachPreview.innerHTML = '';
    if (pendingAttachments.length === 0) {
      $attachPreview.classList.remove('visible');
      return;
    }
    $attachPreview.classList.add('visible');
    pendingAttachments.forEach(function(att, idx) {
      var thumb = document.createElement('div');
      thumb.className = 'attach-thumb';

      if (att.type === 'document') {
        var icon = document.createElement('div');
        icon.className = 'attach-doc-icon';
        icon.textContent = att.uploading ? '\u23f3' : '\ud83d\udcc4';
        thumb.appendChild(icon);
      } else {
        var img = document.createElement('img');
        img.src = att.dataUrl;
        thumb.appendChild(img);
      }

      var name = document.createElement('div');
      name.className = 'attach-name';
      name.textContent = att.fileName + (att.uploading ? ' (upload...)' : '');
      thumb.appendChild(name);

      var removeBtn = document.createElement('button');
      removeBtn.className = 'attach-remove';
      removeBtn.textContent = '\u00d7';
      removeBtn.addEventListener('click', function() {
        pendingAttachments.splice(idx, 1);
        renderAttachPreviews();
      });
      thumb.appendChild(removeBtn);

      $attachPreview.appendChild(thumb);
    });
  }

  // --- State ---
  let ws = null;
  let connected = false;
  let pendingRequests = new Map();
  let chatRunId = null;
  let streamText = '';
  let _isGenerating = false;
  var unreadCounts = {};  // sessionKey -> unread message count
  let connectNonce = null;
  let connectSent = false;
  let reconnectTimer = null;
  let backoffMs = 800;
  let reconnectAttempt = 0;

  // --- Token check ---
  if (!TOKEN) {
    showError('Token manquant. Ajoutez ?t=VOTRE_TOKEN dans l\'URL.');
    $input.disabled = true;
    $btnSend.disabled = true;
  }

  // --- URL params customization ---
  if (AGENT_NAME) {
    $headerName.textContent = AGENT_NAME;
    $welcomeTitle.textContent = 'Bienvenue chez ' + AGENT_NAME;
  }
  if (AGENT_ROLE) {
    $headerRole.textContent = AGENT_ROLE;
  }

  // --- UUID ---
  function uuid() {
    if (crypto && crypto.randomUUID) return crypto.randomUUID();
    return 'xxxxxxxx-xxxx-4xxx-yxxx-xxxxxxxxxxxx'.replace(/[xy]/g, function(c) {
      var r = Math.random() * 16 | 0;
      return (c === 'x' ? r : (r & 0x3 | 0x8)).toString(16);
    });
  }

  // --- Time formatting ---
  function formatTime(ts) {
    if (!ts) return '';
    var d = new Date(ts);
    return d.toLocaleTimeString('fr-FR', { hour: '2-digit', minute: '2-digit' });
  }

  // --- Parse WhatsApp metadata from message ---
  function parseWhatsAppMetadata(text) {
    if (!text) return { segments: [{ text: text, sender: null }] };

    // Check if this is a batched message with multiple "--- Queued #N" segments
    var queuePattern = /---\s*\nQueued\s+#\d+\s*\n/g;
    var queueMatches = [];
    var m;
    while ((m = queuePattern.exec(text)) !== null) {
      queueMatches.push({ index: m.index, length: m[0].length });
    }

    // If batched: split into segments
    var rawSegments = [];
    if (queueMatches.length > 0) {
      for (var i = 0; i < queueMatches.length; i++) {
        var segStart = queueMatches[i].index + queueMatches[i].length;
        var segEnd = (i + 1 < queueMatches.length) ? queueMatches[i + 1].index : text.length;
        rawSegments.push(text.substring(segStart, segEnd).trim());
      }
    } else {
      rawSegments.push(text);
    }

    // Parse each segment for metadata
    var segments = [];
    for (var s = 0; s < rawSegments.length; s++) {
      var seg = rawSegments[s];
      var parsed = { text: seg, sender: null, conversationInfo: null };

      // Strip media prefix from segment
      var segMediaPrefix = seg.match(/^\[media attached:[^\]]*\][\s\S]*?(?=Conversation info|Sender \(untrusted)/i);
      if (segMediaPrefix) {
        seg = seg.slice(segMediaPrefix[0].length);
      } else {
        seg = seg.replace(/^\[media attached:[^\]]*\]\s*/i, '');
      }

      // Conversation info
      var convMatch = seg.match(/^Conversation info\s*\(untrusted metadata\)\s*:\s*```json\s*([\s\S]*?)```\s*/i);
      if (convMatch) {
        try { parsed.conversationInfo = JSON.parse(convMatch[1].trim()); } catch(e) {}
        seg = seg.slice(convMatch[0].length);
      }

      // Sender info
      var senderMatch = seg.match(/^Sender\s*\(untrusted metadata\)\s*:\s*```json\s*([\s\S]*?)```\s*/i);
      if (senderMatch) {
        try {
          var senderData = JSON.parse(senderMatch[1].trim());
          if (senderData.label) senderData.label = senderData.label.replace(/\s*\([+\d]+\)\s*$/, '').trim();
          if (senderData.name) senderData.name = senderData.name.replace(/\s*\([+\d]+\)\s*$/, '').trim();
          parsed.sender = senderData;
        } catch(e) {}
        seg = seg.slice(senderMatch[0].length);
      }

      // Strip timestamp
      seg = seg.replace(/^\[([\w\s\-:+\/]+)\]\s*/i, '');
      parsed.text = seg.trim();

      // Only add if there's actual text content
      if (parsed.text || parsed.sender) {
        segments.push(parsed);
      }
    }

    // If no segments parsed, return as single segment with original text
    if (segments.length === 0) {
      // Also try single-message format (no Queued prefix)
      // Strip media prefix if present
      var smPfx = text.match(/^\[media attached:[^\]]*\][\s\S]*?(?=Conversation info|Sender \(untrusted)/i);
      if (smPfx) {
        text = text.slice(smPfx[0].length);
      } else {
        text = text.replace(/^\[media attached:[^\]]*\]\s*/i, '');
      }
      var single = { text: text, sender: null, conversationInfo: null };
      var singleConv = text.match(/^Conversation info\s*\(untrusted metadata\)\s*:\s*```json\s*([\s\S]*?)```\s*/i);
      if (singleConv) {
        try { single.conversationInfo = JSON.parse(singleConv[1].trim()); } catch(e) {}
        text = text.slice(singleConv[0].length);
      }
      var singleSender = text.match(/^Sender\s*\(untrusted metadata\)\s*:\s*```json\s*([\s\S]*?)```\s*/i);
      if (singleSender) {
        try {
          var sd = JSON.parse(singleSender[1].trim());
          if (sd.label) sd.label = sd.label.replace(/\s*\([+\d]+\)\s*$/, '').trim();
          if (sd.name) sd.name = sd.name.replace(/\s*\([+\d]+\)\s*$/, '').trim();
          single.sender = sd;
        } catch(e) {}
        text = text.slice(singleSender[0].length);
      }
      text = text.replace(/^\[([\w\s\-:+\/]+)\]\s*/i, '');
      single.text = text.trim();
      segments.push(single);
    }

    return { segments: segments };
  }

  // --- Render WhatsApp sender header ---
  function renderWaSenderHeader(sender) {
    if (!sender) return null;
    var name = sender.label || sender.name || sender.pushName || '';
    var phone = sender.e164 || sender.phone || '';
    if (!name && !phone) return null;

    var header = document.createElement('div');
    header.className = 'wa-sender-header';

    // Avatar with initials
    var avatar = document.createElement('div');
    avatar.className = 'wa-sender-avatar';
    var initials = name ? name.split(' ').map(function(w) { return w[0]; }).slice(0, 2).join('').toUpperCase() : '?';
    avatar.textContent = initials;
    // Consistent color from name
    var hue = 0;
    for (var i = 0; i < name.length; i++) hue = (hue + name.charCodeAt(i) * 37) % 360;
    avatar.style.backgroundColor = 'hsl(' + hue + ', 55%, 45%)';
    header.appendChild(avatar);

    var info = document.createElement('div');
    info.className = 'wa-sender-info';
    var nameEl = document.createElement('span');
    nameEl.className = 'wa-sender-name';
    nameEl.textContent = name;
    info.appendChild(nameEl);
    if (phone) {
      var phoneEl = document.createElement('span');
      phoneEl.className = 'wa-sender-phone';
      phoneEl.textContent = phone;
      info.appendChild(phoneEl);
    }
    header.appendChild(info);
    return header;
  }

  // --- Strip OpenClaw metadata prefix ---
  function cleanText(text) {
    if (!text) return '';
    // Pattern: "Conversation info (untrusted metadata): ```json { ... } ```  [timestamp] actual message"
    var cleaned = text.replace(/^Conversation info\s*\(untrusted metadata\)\s*:\s*```json\s*\{[^}]*\}\s*```\s*/i, '');
    // Strip leading timestamp like [Thu 2026-02-19 20:46 GMT+1]
    cleaned = cleaned.replace(/^\[[\w\s\-:+\/]+\]\s*/i, '');
    return cleaned.trim();
  }

  // --- Extract text from message content ---
  // --- Extract text from message content ---
  function extractText(msg) {
    if (!msg) return '';
    var content = msg.content || msg;
    if (typeof content === 'string') return content;
    if (Array.isArray(content)) {
      return content
        .filter(function(c) { return c.type === 'text' && c.text; })
        .map(function(c) { return c.text; })
        .join('\n');
    }
    if (typeof msg.text === 'string') return msg.text;
    return '';
  }

  // --- Extract images from message content ---
  function extractImages(msg) {
    if (!msg) return [];
    var content = msg.content || msg;
    if (!Array.isArray(content)) return [];
    var images = [];
    content.forEach(function(block) {
      // Claude API format: { type: 'image', source: { type: 'base64', media_type: '...', data: '...' } }
      if (block.type === 'image' && block.source) {
        if (block.source.type === 'base64' && block.source.data) {
          var mime = block.source.media_type || block.source.mimeType || 'image/png';
          images.push('data:' + mime + ';base64,' + block.source.data);
        } else if (block.source.type === 'url' && block.source.url) {
          images.push(block.source.url);
        }
      }
      // Alternative format: { type: 'image', data: '...', mimeType: '...' }
      if (block.type === 'image' && block.data && !block.source) {
        var mime2 = block.mimeType || block.media_type || 'image/png';
        images.push('data:' + mime2 + ';base64,' + block.data);
      }
      // Tool result with image content
      if (block.type === 'tool_result' && Array.isArray(block.content)) {
        block.content.forEach(function(sub) {
          if (sub.type === 'image' && sub.source && sub.source.data) {
            var mime3 = sub.source.media_type || 'image/png';
            images.push('data:' + mime3 + ';base64,' + sub.source.data);
          }
        });
      }
    });
    return images;
  }


  // --- UI helpers ---
  function showError(msg) {
    $errorBanner.textContent = msg;
    $errorBanner.classList.add('visible');
  }

  function hideError() {
    $errorBanner.classList.remove('visible');
  }

  function setStatus(state, info) {
    $statusDot.className = 'status-dot ' + state;
    var label = '';
    var title = '';
    
    // Always hide banner first — only reconnecting state shows it
    if ($reconnectBanner) $reconnectBanner.classList.add('hidden');
    
    if (state === 'connected') {
      title = 'Connecté';
      label = 'Connecté';
      if ($wsStatus) $wsStatus.classList.remove('show-label');
      reconnectAttempt = 0;
      // Flash green label briefly on reconnection
      if (info === 'reconnected') {
        if ($statusLabel) $statusLabel.style.color = '#22c55e';
        label = 'Reconnecté !';
        if ($wsStatus) $wsStatus.classList.add('show-label');
        setTimeout(function() {
          if ($wsStatus) $wsStatus.classList.remove('show-label');
          if ($statusLabel) $statusLabel.style.color = '';
        }, 3000);
        // Restore typing indicator if still generating
        if (_isGenerating) {
          showTyping();
        }
      }
    } else if (state === 'connecting') {
      title = 'Connexion...';
      label = 'Connexion...';
      if ($wsStatus) $wsStatus.classList.add('show-label');
    } else if (state === 'reconnecting') {
      $statusDot.className = 'status-dot connecting';
      title = 'Reconnexion (tentative ' + reconnectAttempt + ')';
      label = 'Tentative ' + reconnectAttempt + '...';
      if ($wsStatus) $wsStatus.classList.add('show-label');
      // Show banner (override the hidden we set above)
      if ($reconnectBanner) $reconnectBanner.classList.remove('hidden');
      var nextSec = Math.round(backoffMs / 1000);
      if ($reconnectText) $reconnectText.textContent = 'Connexion perdue — tentative ' + reconnectAttempt + ' dans ' + nextSec + 's...';
    } else if (state === 'idle') {
      // Pre-login state — don't show alarming "Déconnecté"
      title = '';
      label = '';
      $statusDot.className = 'status-dot idle';
      if ($wsStatus) $wsStatus.classList.remove('show-label');
    } else {
      // disconnected
      title = 'Déconnecté';
      label = 'Déconnecté';
      if ($wsStatus) $wsStatus.classList.add('show-label');
    }
    
    $statusDot.title = title;
    if ($statusLabel) $statusLabel.textContent = label;
  }

  // --- Image lightbox ---
  function openLightbox(src) {
    var overlay = document.createElement('div');
    overlay.className = 'lightbox-overlay';
    var img = document.createElement('img');
    img.className = 'lightbox-img';
    img.src = src;
    img.alt = 'Image';
    var closeBtn = document.createElement('button');
    closeBtn.className = 'lightbox-close';
    closeBtn.innerHTML = '&times;';
    var dlBtn = document.createElement('a');
    dlBtn.className = 'lightbox-download';
    dlBtn.href = src;
    dlBtn.download = 'image';
    dlBtn.innerHTML = '<svg viewBox="0 0 24 24" width="20" height="20" fill="none" stroke="currentColor" stroke-width="2"><path d="M21 15v4a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2v-4"/><polyline points="7 10 12 15 17 10"/><line x1="12" y1="15" x2="12" y2="3"/></svg>';
    function close() { overlay.remove(); }
    overlay.addEventListener('click', function(e) { if (e.target === overlay) close(); });
    closeBtn.addEventListener('click', close);
    document.addEventListener('keydown', function handler(e) {
      if (e.key === 'Escape') { close(); document.removeEventListener('keydown', handler); }
    });
    overlay.appendChild(img);
    overlay.appendChild(closeBtn);
    overlay.appendChild(dlBtn);
    document.body.appendChild(overlay);
    requestAnimationFrame(function() { overlay.classList.add('visible'); });
  }

  // --- Smart auto-scroll: pause when user scrolls up ---
  var _userScrolledUp = false;
  var _scrollFab = null;

  function scrollToBottom(smooth) {
    if (_userScrolledUp) return; // Don't auto-scroll if user scrolled up
    requestAnimationFrame(function() {
      $messages.scrollTo({
        top: $messages.scrollHeight,
        behavior: smooth ? 'smooth' : 'instant'
      });
    });
  }

  function forceScrollToBottom() {
    _userScrolledUp = false;
    hideScrollFab();
    requestAnimationFrame(function() {
      $messages.scrollTo({ top: $messages.scrollHeight, behavior: 'smooth' });
    });
  }

  function showScrollFab() {
    if (_scrollFab) return;
    _scrollFab = document.createElement('button');
    _scrollFab.className = 'scroll-fab';
    _scrollFab.title = 'Aller en bas';
    _scrollFab.innerHTML = '<svg viewBox="0 0 24 24" width="20" height="20" fill="none" stroke="currentColor" stroke-width="2"><polyline points="6 9 12 15 18 9"/></svg>';
    _scrollFab.addEventListener('click', forceScrollToBottom);
    document.querySelector('.app-main').appendChild(_scrollFab);
  }

  function hideScrollFab() {
    if (_scrollFab) { _scrollFab.remove(); _scrollFab = null; }
  }

  $messages.addEventListener('scroll', function() {
    var threshold = 120;
    var atBottom = ($messages.scrollHeight - $messages.scrollTop - $messages.clientHeight) < threshold;
    if (atBottom) {
      _userScrolledUp = false;
      hideScrollFab();
    } else {
      _userScrolledUp = true;
      showScrollFab();
    }
  });


  // --- Enhanced Markdown parser (V12-2) ---
  // Markdown cache: avoid re-parsing identical text
  var _mdCache = { key: '', val: '' };

  function parseMarkdown(text) {
    if (!text) return '';
    if (text === _mdCache.key) return _mdCache.val;
    var html = text;

    // Escape HTML entities first (security)
    html = html.replace(/&/g, '&amp;').replace(/</g, '&lt;').replace(/>/g, '&gt;');

    // ── 0. Extract thinking blocks (collapsible) ──
    var thinkingBlocks = [];
    html = html.replace(/&lt;thinking&gt;([\s\S]*?)&lt;\/thinking&gt;/g, function(m, content) {
      var idx = thinkingBlocks.length;
      thinkingBlocks.push(content.trim());
      return '%%THINKING_' + idx + '%%';
    });

    // ── 1. Extract code blocks FIRST to protect from other transforms ──
    var codeBlocks = [];
    html = html.replace(/```(\w*)\n([\s\S]*?)```/g, function(m, lang, code) {
      var idx = codeBlocks.length;
      var langLabel = lang ? '<div class="code-header"><span class="code-lang">' + lang + '</span><button class="code-copy-btn" data-action="copy-code">Copier</button></div>' : '';
      var wrapClass = lang ? ' has-lang' : '';
      codeBlocks.push('<div class="code-wrapper' + wrapClass + '">' + langLabel + '<pre><code>' + code.trim() + '</code></pre></div>');
      return '%%CODEBLOCK_' + idx + '%%';
    });

    // Extract inline code to protect from other transforms
    var inlineCodes = [];
    html = html.replace(/`([^`]+)`/g, function(m, code) {
      var idx = inlineCodes.length;
      inlineCodes.push('<code class="inline-code">' + code + '</code>');
      return '%%INLINE_' + idx + '%%';
    });

    // ── 2. Extract tables BEFORE other transforms ──
    var tables = [];
    html = html.replace(/((?:^\|.+\|[ ]*\n)+)/gm, function(tableBlock) {
      var rows = tableBlock.trim().split('\n');
      if (rows.length < 2) return tableBlock;

      // Check if row 2 is separator (|---|---|)
      var isSeparator = /^\|[\s\-:]+(\|[\s\-:]+)+\|?$/.test(rows[1]);
      if (!isSeparator) return tableBlock;

      // Parse alignment from separator row
      var aligns = rows[1].replace(/^\||\|$/g, '').split('|').map(function(cell) {
        cell = cell.trim();
        if (cell.charAt(0) === ':' && cell.charAt(cell.length - 1) === ':') return 'center';
        if (cell.charAt(cell.length - 1) === ':') return 'right';
        return 'left';
      });

      // Detect if this is a task table (has "Tâche" or "Tache" column)
      var headerCells = rows[0].replace(/^\||\|$/g, '').split('|').map(function(c) { return c.trim(); });
      var taskColIdx = -1;
      var statusColIdx = -1;
      headerCells.forEach(function(h, i) {
        var hl = h.toLowerCase().replace(/\*\*/g, '');
        if (hl === 'tâche' || hl === 'tache' || hl === 'task') taskColIdx = i;
        if (hl === 'status' || hl === 'statut') statusColIdx = i;
      });
      var isTaskTable = (taskColIdx >= 0);

      // Build header
      var thead = '<thead><tr>';
      if (isTaskTable) {
        thead += '<th class="task-check-col"></th>';
      }
      headerCells.forEach(function(cell, i) {
        var align = aligns[i] || 'left';
        thead += '<th style="text-align:' + align + '">' + cell + '</th>';
      });
      thead += '</tr></thead>';

      // Build body
      var tbody = '<tbody>';
      for (var r = 2; r < rows.length; r++) {
        if (!rows[r].trim()) continue;
        var cells = rows[r].replace(/^\||\|$/g, '').split('|').map(function(c) { return c.trim(); });

        // Get task title and status for task tables
        var taskTitle = isTaskTable && taskColIdx >= 0 ? cells[taskColIdx] || '' : '';
        var taskStatus = isTaskTable && statusColIdx >= 0 ? cells[statusColIdx] || '' : '';
        // Clean markdown bold from task title
        taskTitle = taskTitle.replace(/\*\*/g, '').trim();
        // Check if task is already done
        var isDone = /done|terminé|fait|✅/i.test(taskStatus);

        var trClass = isTaskTable ? (isDone ? ' class="task-row task-row-done"' : ' class="task-row"') : '';
        tbody += '<tr' + trClass + '>';

        if (isTaskTable) {
          var safeTitle = taskTitle.replace(/'/g, '&#39;').replace(/"/g, '&quot;');
          if (isDone) {
            tbody += '<td class="task-check-col"><span class="task-table-check checked" title="Déjà terminée"></span></td>';
          } else {
            tbody += '<td class="task-check-col"><button class="task-table-check" data-task-title="' + safeTitle + '" title="Marquer comme fait"></button></td>';
          }
        }

        cells.forEach(function(cell, i) {
          var align = aligns[i] || 'left';
          tbody += '<td style="text-align:' + align + '">' + cell + '</td>';
        });
        tbody += '</tr>';
      }
      tbody += '</tbody>';

      var wrapperClass = isTaskTable ? 'table-wrapper task-table' : 'table-wrapper';
      var idx = tables.length;
      tables.push('<div class="' + wrapperClass + '"><table>' + thead + tbody + '</table></div>');
      return '%%TABLE_' + idx + '%%\n';
    });

    // ── 3. Text formatting ──

    // Bold (**text** or __text__)
    html = html.replace(/\*\*(.+?)\*\*/g, '<strong>$1</strong>');
    html = html.replace(/__(.+?)__/g, '<strong>$1</strong>');

    // Italic (*text* or _text_)
    html = html.replace(/(?<![\w*])\*([^*]+)\*(?![\w*])/g, '<em>$1</em>');
    html = html.replace(/(?<![\w_])_([^_]+)_(?![\w_])/g, '<em>$1</em>');

    // Strikethrough (~~text~~)
    html = html.replace(/~~(.+?)~~/g, '<del>$1</del>');

    // Highlight (==text==)
    html = html.replace(/==(.+?)==/g, '<mark>$1</mark>');

    // ── 4. Block elements ──

    // Headers (### ... at start of line)
    html = html.replace(/^#### (.+)$/gm, '<h4>$1</h4>');
    html = html.replace(/^### (.+)$/gm, '<h3>$1</h3>');
    html = html.replace(/^## (.+)$/gm, '<h2>$1</h2>');
    html = html.replace(/^# (.+)$/gm, '<h1>$1</h1>');

    // Blockquotes (multi-line support — merge consecutive)
    html = html.replace(/^&gt; (.+)$/gm, '<blockquote>$1</blockquote>');
    html = html.replace(/<\/blockquote>\n<blockquote>/g, '<br>');

    // Horizontal rules
    html = html.replace(/^---$/gm, '<hr>');

    // ── 5. Lists ──

    // Task lists (- [ ] or - [x])
    html = html.replace(/^[\-\*] \[x\] (.+)$/gm, '<li class="task-item task-done"><span class="task-check checked"></span>$1</li>');
    html = html.replace(/^[\-\*] \[ \] (.+)$/gm, '<li class="task-item"><span class="task-check"></span>$1</li>');

    // Unordered lists (- item or * item) — but NOT task items already converted
    html = html.replace(/^[\-\*] (.+)$/gm, function(match, content) {
      if (content.indexOf('class="task-check') !== -1) return match;
      return '<li>' + content + '</li>';
    });

    // Wrap task lists
    html = html.replace(/((?:<li class="task-item[^"]*">.*<\/li>\n?)+)/g, function(m) {
      return '<ul class="task-list">' + m + '</ul>';
    });

    // Wrap regular unordered lists
    html = html.replace(/((?:<li>(?!class).*<\/li>\n?)+)/g, function(m) {
      return '<ul>' + m + '</ul>';
    });

    // Ordered lists (1. item) — wrap in <ol>
    html = html.replace(/^\d+\. (.+)$/gm, '<oli>$1</oli>');
    html = html.replace(/((?:<oli>.*<\/oli>\n?)+)/g, function(m) {
      return '<ol>' + m.replace(/<\/?oli>/g, function(t) { return t.replace('oli', 'li'); }) + '</ol>';
    });

    // ── 6. Links ──

    // Links [text](url) — with action:// and nav:// protocol support
    html = html.replace(/\[([^\]]+)\]\(([^)]+)\)/g, function(match, text, url) {
      // action://type/id — internal action links (open client card, etc.)
      var actionMatch = url.match(/^action:\/\/(\w+)\/(.+)$/);
      if (actionMatch) {
        return '<a href="#" class="action-link" data-action="' + actionMatch[1] + '" data-id="' + actionMatch[2] + '" title="' + text + '">' +
          '<svg class="link-icon" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><circle cx="12" cy="12" r="10"/><path d="M12 8v8M8 12h8"/></svg>' +
          text + '</a>';
      }
      // nav://target — internal navigation links (folders, settings, etc.)
      var navMatch = url.match(/^nav:\/\/(.+)$/);
      if (navMatch) {
        return '<a href="#" class="nav-link" data-nav="' + navMatch[1] + '" title="' + text + '">' +
          '<svg class="link-icon" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M5 12h14M12 5l7 7-7 7"/></svg>' +
          text + '</a>';
      }
      // Default: external URL
      return '<a href="' + url + '" target="_blank" rel="noopener noreferrer">' + text + '</a>';
    });

    // Auto-link bare URLs (skip URLs already inside <a> tags)
    html = html.replace(/((?:<a\s[^>]*>.*?<\/a>)|(?:href="[^"]*")|(https?:\/\/[^\s<>"'\)]+))/g, function(match, full, url) {
      if (url) return '<a href="' + url + '" target="_blank" rel="noopener noreferrer">' + url + '</a>';
      return match;
    });

    // ── 7. Paragraphs & line breaks ──

    // Paragraphs: convert double newlines to paragraph breaks
    html = html.replace(/\n\n/g, '</p><p>');

    // Single newlines to <br>
    html = html.replace(/\n/g, '<br>');

    // Wrap in paragraph if not already wrapped in block elements or placeholders
    if (!/^(<[hupolb]|%%CODEBLOCK|%%TABLE)/.test(html)) {
      html = '<p>' + html + '</p>';
    }

    // ── 8. Cleanup ──
    html = html.replace(/<p><\/p>/g, '');
    html = html.replace(/<p><br><\/p>/g, '');
    html = html.replace(/<p>(%%CODEBLOCK_\d+%%)<\/p>/g, '$1');
    html = html.replace(/<p>(%%TABLE_\d+%%)<\/p>/g, '$1');
    html = html.replace(/<br>(%%TABLE_\d+%%)/g, '$1');
    html = html.replace(/(%%TABLE_\d+%%)<br>/g, '$1');

    // ── 9. Restore protected blocks (LAST step) ──
    html = html.replace(/%%CODEBLOCK_(\d+)%%/g, function(m, idx) {
      return codeBlocks[parseInt(idx)];
    });
    html = html.replace(/%%TABLE_(\d+)%%/g, function(m, idx) {
      return tables[parseInt(idx)];
    });
    html = html.replace(/%%INLINE_(\d+)%%/g, function(m, idx) {
      return inlineCodes[parseInt(idx)];
    });

    // ── 10. Restore thinking blocks (collapsible) ──
    html = html.replace(/<p>(%%THINKING_\d+%%)<\/p>/g, '$1');
    html = html.replace(/%%THINKING_(\d+)%%/g, function(m, idx) {
      var content = thinkingBlocks[parseInt(idx)];
      return '<details class="thinking-block"><summary class="thinking-summary"><svg viewBox="0 0 24 24" width="14" height="14" fill="none" stroke="currentColor" stroke-width="2"><path d="M12 2a7 7 0 0 1 7 7c0 2.38-1.19 4.47-3 5.74V17a2 2 0 0 1-2 2h-4a2 2 0 0 1-2-2v-2.26C6.19 13.47 5 11.38 5 9a7 7 0 0 1 7-7z"/><line x1="10" y1="22" x2="14" y2="22"/></svg> Réflexion</summary><div class="thinking-content">' + content + '</div></details>';
    });

    _mdCache.key = text;
    _mdCache.val = html;
    return html;
  }

  // ── Complete task from table checkbox → Notion API ──
  window.completeTaskFromTable = function(btn) {
    var taskTitle = btn.getAttribute('data-task-title');
    if (!taskTitle) return;

    // Prevent double-click
    if (btn.classList.contains('loading') || btn.classList.contains('checked')) return;
    btn.classList.add('loading');
    btn.title = 'Mise à jour en cours...';

    var row = btn.closest('tr');

    fetch('/api/notion-tasks.php', {
      method: 'PATCH',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ title: taskTitle, status: 'Done' })
    })
    .then(function(res) { return res.json().then(function(data) { return { ok: res.ok, data: data }; }); })
    .then(function(result) {
      btn.classList.remove('loading');
      if (result.ok && result.data.success) {
        // Success: animate to checked
        btn.classList.add('checked');
        btn.disabled = true;
        btn.title = 'Terminée ✓';
        if (row) {
          row.classList.add('task-row-done');
          // Add completion animation
          row.style.transition = 'opacity 0.3s';
        }
        // Show subtle toast
        showTaskToast('✓ ' + taskTitle, 'success');
      } else {
        // Error
        btn.classList.add('error');
        btn.title = result.data.error || 'Erreur';
        setTimeout(function() { btn.classList.remove('error'); btn.title = 'Marquer comme fait'; }, 3000);
        showTaskToast('Erreur: ' + (result.data.error || 'Tâche non trouvée'), 'error');
      }
    })
    .catch(function(err) {
      btn.classList.remove('loading');
      btn.classList.add('error');
      btn.title = 'Erreur réseau';
      setTimeout(function() { btn.classList.remove('error'); btn.title = 'Marquer comme fait'; }, 3000);
      showTaskToast('Erreur réseau', 'error');
    });
  };

  // Mini-toast for task completion feedback
  function showTaskToast(message, type) {
    var existing = document.querySelector('.task-toast');
    if (existing) existing.remove();

    var toast = document.createElement('div');
    toast.className = 'task-toast task-toast-' + type;
    toast.textContent = message;
    document.body.appendChild(toast);

    // Trigger animation
    requestAnimationFrame(function() {
      toast.classList.add('visible');
    });

    setTimeout(function() {
      toast.classList.remove('visible');
      setTimeout(function() { toast.remove(); }, 300);
    }, 3000);
  }

  // Batch mode: when loading history, collect into fragment instead of live DOM
  var _batchFragment = null;

  function addMessage(role, text, timestamp, images) {
    if (!_batchFragment && $welcome.parentNode) $welcome.remove();

    var msgDiv = document.createElement('div');
    msgDiv.className = 'msg ' + role;

    var bubble = document.createElement('div');
    bubble.className = 'msg-bubble';

    // Render images if any
    if (images && images.length > 0) {
      images.forEach(function(src) {
        var img = document.createElement('img');
        img.className = 'msg-image';
        img.src = src;
        img.alt = 'Image';
        img.style.cursor = 'pointer';
        img.addEventListener('click', function() {
          openLightbox(src);
        });
        bubble.appendChild(img);
      });
    }

    // Render text (with WhatsApp metadata parsing for user messages)
    if (text) {
      if (role === 'assistant') {
        var textDiv = document.createElement('div');
        textDiv.innerHTML = parseMarkdown(text);
        bubble.appendChild(textDiv);
      } else {
        var waMeta = parseWhatsAppMetadata(text);
        var segs = waMeta.segments;
        var hasAnySender = segs.some(function(s) { return !!s.sender; });
        if (hasAnySender) msgDiv.classList.add('wa-message');

        segs.forEach(function(seg, idx) {
          // Add separator between batched segments
          if (idx > 0 && segs.length > 1) {
            var sep = document.createElement('hr');
            sep.className = 'wa-segment-sep';
            bubble.appendChild(sep);
          }
          // Sender header
          if (seg.sender) {
            var senderHeader = renderWaSenderHeader(seg.sender);
            if (senderHeader) bubble.appendChild(senderHeader);
          }
          // Message text
          if (seg.text) {
            var userTextDiv = document.createElement('div');
            userTextDiv.className = 'msg-text';
            userTextDiv.textContent = seg.text;
            bubble.appendChild(userTextDiv);
          }
        });
      }
    }

    var time = document.createElement('div');
    time.className = 'msg-time';
    time.textContent = formatTime(timestamp || Date.now());

    // Sprint 13: wrap in msg-row with avatar for assistant
    var row = document.createElement('div');
    row.className = 'msg-row';
    var avatarDiv = document.createElement('div');
    avatarDiv.className = 'msg-avatar';
    if (role === 'assistant') {
      var hdrAv = document.getElementById('header-avatar');
      var hdrImg = hdrAv ? hdrAv.querySelector('img') : null;
      if (hdrImg) {
        var avImg = document.createElement('img');
        avImg.src = hdrImg.src;
        avImg.alt = '';
        avatarDiv.appendChild(avImg);
      }
    }
    var contentDiv = document.createElement('div');
    contentDiv.className = 'msg-content';
    contentDiv.appendChild(bubble);
    contentDiv.appendChild(time);
    row.appendChild(avatarDiv);
    row.appendChild(contentDiv);
    msgDiv.appendChild(row);

    // Sprint 13: groupement — check if previous message is same role
    var container = _batchFragment || $messages;
    var prevMsg = container.lastElementChild;
    if (prevMsg && prevMsg.classList && prevMsg.classList.contains('msg')) {
      if ((prevMsg.classList.contains('assistant') && role === 'assistant') ||
          (prevMsg.classList.contains('user') && role === 'user')) {
        msgDiv.classList.add('grouped');
      }
    }

    if(role==='user'&&text){
      msgDiv.dataset.originalText=text;
      var editBtn=document.createElement('button');
      editBtn.className='msg-edit-btn';
      editBtn.title='Modifier et renvoyer';
      editBtn.innerHTML='<svg viewBox="0 0 24 24" width="14" height="14" fill="none" stroke="currentColor" stroke-width="2"><path d="M17 3a2.828 2.828 0 1 1 4 4L7.5 20.5 2 22l1.5-5.5L17 3z"/></svg>';
      editBtn.addEventListener('click',function(){startEditMessage(msgDiv)});
      contentDiv.appendChild(editBtn);
    }
    if(role==='assistant'){msgDiv.dataset.userText=lastUserMessage||'';contentDiv.appendChild(createActionBar(msgDiv))}
    if (_batchFragment) {
      _batchFragment.appendChild(msgDiv);
    } else {
      $messages.appendChild(msgDiv);
      scrollToBottom(true);
    }
    if(role==='assistant'){addCopyButtons(bubble);if(!_batchFragment)addLinkPreviews(bubble)}
  }


  function addImageMessage(role, src, fileName) {
    if ($welcome.parentNode) $welcome.remove();

    var msgDiv = document.createElement('div');
    msgDiv.className = 'msg ' + role;

    var bubble = document.createElement('div');
    bubble.className = 'msg-bubble';

    var img = document.createElement('img');
    img.className = 'msg-image';
    img.src = src;
    img.alt = fileName || 'Image';
    bubble.appendChild(img);

    var time = document.createElement('div');
    time.className = 'msg-time';
    time.textContent = formatTime(Date.now());

    msgDiv.appendChild(bubble);
    msgDiv.appendChild(time);

    $messages.appendChild(msgDiv);
    scrollToBottom(true);
  }

  function showTyping() {
    if(typeof updateTypingAvatar==='function')updateTypingAvatar();
    $typing.classList.add('visible');
    $messages.appendChild($typing);
    scrollToBottom(true);
  }

  function hideTyping() {
    $typing.classList.remove('visible');
    if ($typing.parentNode) $typing.parentNode.removeChild($typing);
  }

  // Debounced streaming: raw text during deltas, parsed only every 120ms
  var _streamParseTimer = null;
  var _streamLastParsed = 0;
  var _streamRawText = '';

  var _streamActivityTimer = null;
  var _streamLastDelta = 0;

  function showStreaming(text) {
    $streaming.classList.add('visible');
    _streamRawText = text;
    _streamLastDelta = Date.now();
    // Reset working state — text is flowing
    $streaming.classList.remove('working');
    // Start a timer: if no new delta for 3s, show "working" indicator
    clearTimeout(_streamActivityTimer);
    _streamActivityTimer = setTimeout(function _checkStall() {
      if (_isGenerating && Date.now() - _streamLastDelta > 2800) {
        $streaming.classList.add('working');
      }
      // Keep checking every 2s
      if (_isGenerating) {
        _streamActivityTimer = setTimeout(_checkStall, 2000);
      }
    }, 3000);
    // Smooth streaming: buffer text and render every 350ms for fluid feel
    if (!_streamParseTimer) {
      _streamParseTimer = setTimeout(function() {
        _streamParseTimer = null;
        _streamLastParsed = Date.now();
        $streamingText.innerHTML = parseMarkdown(_streamRawText);
        scrollToBottom(false);
      }, 350);
    }
    if (!$streaming.parentNode || $streaming.parentNode !== $messages) {
      $messages.appendChild($streaming);
    }
    scrollToBottom(false);
  }

  function hideStreaming() {
    clearTimeout(_streamActivityTimer);
    $streaming.classList.remove('working');
    if (_streamParseTimer) { clearTimeout(_streamParseTimer); _streamParseTimer = null; }
    // Final parse with full text before hiding
    if (_streamRawText) {
      $streamingText.innerHTML = parseMarkdown(_streamRawText);
      _streamRawText = '';
    }
    $streaming.classList.remove('visible');
    $streamingText.textContent = '';
    if ($streaming.parentNode) $streaming.parentNode.removeChild($streaming);
  }

  function setGenerating(isGen) {
    _isGenerating = isGen;
    var streamAv = document.getElementById('streaming-avatar');
    if (isGen) {
      $btnSend.style.display = 'none';
      $btnStop.classList.add('visible');
      // Populate streaming avatar from header avatar
      if (streamAv) {
        var hdrAv = document.getElementById('header-avatar');
        var hdrImg = hdrAv ? hdrAv.querySelector('img') : null;
        if (hdrImg && !streamAv.querySelector('img')) {
          var avImg = document.createElement('img');
          avImg.src = hdrImg.src;
          avImg.alt = '';
          streamAv.appendChild(avImg);
        }
        streamAv.classList.add('working');
      }
    } else {
      $btnSend.style.display = 'flex';
      $btnStop.classList.remove('visible');
      if (streamAv) streamAv.classList.remove('working');
    }
  }

  // --- Auto-resize textarea ---
  $input.addEventListener('input', function() {
    this.style.height = 'auto';
    this.style.height = Math.min(this.scrollHeight, 200) + 'px';
  });

  // --- Fetch gateway token from server (session-based, no token in client) ---
  function fetchGatewayToken(callback) {
    fetch('/api/ws-token.php', { credentials: 'same-origin' })
      .then(function(r) { return r.json(); })
      .then(function(data) {
        if (data.token) {
          TOKEN = data.token;
          callback(null);
        } else {
          callback(new Error(data.error || 'No token'));
        }
      })
      .catch(function(err) { callback(err); });
  }

  // --- WebSocket ---
  function connectWS() {
    if (ws) { ws.close(); ws = null; }
    if (!TOKEN) return;

    setStatus('connecting');
    connectNonce = null;
    connectSent = false;

    var protocol = window.location.protocol === 'https:' ? 'wss:' : 'ws:';
    var wsUrl;
    if (window.location.protocol === 'https:') {
      // HTTPS: use Apache WSS proxy on /ws
      wsUrl = 'wss://' + window.location.host + '/ws';
    } else {
      // HTTP fallback: direct connection to gateway port
      var wsHost = params.get('host') || window.location.hostname;
      var wsPort = params.get('port') || '18789';
      wsUrl = 'ws://' + wsHost + ':' + wsPort;
    }

    ws = new WebSocket(wsUrl);

    ws.addEventListener('open', function() {
      // Wait for connect.challenge from gateway
    });

    ws.addEventListener('message', function(evt) {
      var data;
      try { data = JSON.parse(evt.data); } catch(e) { return; }
      handleMessage(data);
    });

    ws.addEventListener('close', function(evt) {
      connected = false;
      ws = null;
      setStatus('disconnected');
      flushPending(new Error('Déconnecté'));
      if (loginPending) {
        loginPending = false;
        showLoginError('Connexion échouée. Vérifiez votre clé d\'accès.');
        TOKEN = '';
        return;
      }
      if (evt.code !== 1000) {
        scheduleReconnect();
      }
    });

    ws.addEventListener('error', function() {});
  }

  function scheduleReconnect() {
    if (reconnectTimer) return;
    reconnectAttempt++;
    setStatus('reconnecting');
    reconnectTimer = setTimeout(function() {
      reconnectTimer = null;
      setStatus('connecting');
      connectWS();
    }, backoffMs);
    backoffMs = Math.min(backoffMs * 1.7, 15000);
  }

  function sendJSON(obj) {
    if (ws && ws.readyState === WebSocket.OPEN) {
      ws.send(JSON.stringify(obj));
    }
  }

  function request(method, params) {
    return new Promise(function(resolve, reject) {
      if (!ws || ws.readyState !== WebSocket.OPEN) {
        reject(new Error('Non connecté'));
        return;
      }
      var id = uuid();
      var frame = { type: 'req', id: id, method: method, params: params };
      pendingRequests.set(id, { resolve: resolve, reject: reject });
      ws.send(JSON.stringify(frame));

      // Timeout after 30s
      setTimeout(function() {
        if (pendingRequests.has(id)) {
          pendingRequests.delete(id);
          reject(new Error('Timeout'));
        }
      }, 30000);
    });
  }

  function flushPending(err) {
    pendingRequests.forEach(function(p) { p.reject(err); });
    pendingRequests.clear();
  }

  function sendConnect() {
    if (connectSent) return;
    connectSent = true;

    var connectParams = {
      minProtocol: 3,
      maxProtocol: 3,
      client: {
        id: 'openclaw-control-ui',
        version: '1.0.0',
        platform: 'web',
        mode: 'ui'
      },
      role: 'operator',
      scopes: ['operator.read', 'operator.write'],
      caps: [],
      auth: { token: TOKEN },
      locale: 'fr-FR',
      userAgent: 'CollaborateurIA-Chat/1.0.0'
    };

    // No device field — dangerouslyDisableDeviceAuth is enabled
    request('connect', connectParams).then(function(payload) {
      connected = true;
      var wasReconnecting = reconnectAttempt > 0;
      backoffMs = 800;
      setStatus('connected', wasReconnecting ? 'reconnected' : null);
      hideError();

      // Re-enable input (may have been disabled on page load if no token)
      $input.disabled = false;
      $btnSend.disabled = false;

      // Finalize login if pending
      if (loginPending) {
        loginPending = false;
        if ($loginRemember.checked) {
          localStorage.setItem('mybotia-session', SESSION_KEY);
        }
        hideLogin();
        $loginBtn.disabled = false;
        $loginBtn.innerHTML = 'Se connecter';

        // Update sidebar with client info if available (email login)
        if (_clientInfo && _authType === 'email') {
          updateClientSidebar({
            client: _clientInfo,
            collaborateurs: _collaborateurs,
            active_collaborateur: _activeCollab,
            usage: null
          });
          // Fetch fresh usage
          fetch('/api/usage.php', { method: 'GET', credentials: 'same-origin' })
            .then(function(r) { return r.json(); })
            .then(function(udata) {
              if (udata.ok) {
                var cv = document.getElementById('credits-value');
                var cf = document.getElementById('credits-fill');
                var pct = udata.usage.percentage || 0;
                if (cv) cv.textContent = formatNumber(udata.usage.tokens_used) + ' / ' + formatNumber(udata.usage.tokens_max);
                if (cf) {
                  cf.style.width = Math.min(pct, 100) + '%';
                  if (pct > 85) cf.style.background = 'linear-gradient(90deg, #ef4444, #dc2626)';
                  else if (pct > 60) cf.style.background = 'linear-gradient(90deg, #f59e0b, #d97706)';
                  else cf.style.background = 'linear-gradient(90deg, #a78bfa, #7c3aed)';
                }
              }
            }).catch(function() {});
        }

        // Clean token from URL for security (Sprint 3.2)
        if (params.get('t')) {
          var cleanUrl = window.location.pathname;
          if (params.get('session')) cleanUrl += '?session=' + encodeURIComponent(SESSION_KEY);
          history.replaceState(null, '', cleanUrl);
        }
      }

      // Ensure PHP auth session exists (Sprint 3.2)
      // Don't overwrite email session with token session
      if (_authType !== 'email') {
        createAuthSession(TOKEN);
      }

      // Load agent identity
      loadAgentIdentity();

      // Load chat history
      loadHistory();

      // Load preferences from server, then sidebar sessions
      loadPrefsFromServer().then(function() {
        loadSessions();
      }).catch(function() {
        loadSessions();
      });

    }).catch(function(err) {
      if (loginPending) {
        loginPending = false;
        showLoginError('Clé d\'accès invalide ou connexion refusée.');
        TOKEN = '';
        $loginBtn.disabled = false;
        $loginBtn.innerHTML = 'Se connecter';
        if (ws) { ws.close(); ws = null; }
        return;
      }
      showError('Erreur de connexion : ' + err.message);
      if (ws) ws.close(4008, 'connect failed');
    });
  }

  function handleMessage(data) {
    // Event
    if (data.type === 'event') {
      if (data.event === 'connect.challenge') {
        connectNonce = data.payload && data.payload.nonce ? data.payload.nonce : null;
        sendConnect();
        return;
      }

      if (data.event === 'chat') {
        handleChatEvent(data.payload);
        return;
      }
      // Handle agent lifecycle events for activity tracking
      if (data.event === 'agent' && data.payload) {
        var agPayload = data.payload;
        var agStream = agPayload.stream;
        var agData = agPayload.data || {};
        
        if (agStream === 'lifecycle') {
          if (agData.phase === 'start') {
            // Agent started working — show working indicator
            if (!_isGenerating) {
              showTyping();
              setGenerating(true);
            }
            // Start a timer: if no text arrives in 3s, show progressive activity steps
            _agentWorkingSteps = 0;
            clearInterval(_agentWorkingTimer);
            _agentWorkingTimer = setInterval(function() {
              if (!_isGenerating) { clearInterval(_agentWorkingTimer); return; }
              _agentWorkingSteps++;
              // Safety: stop after 60s (20 ticks) to avoid infinite loop
              if (_agentWorkingSteps > 20) { clearInterval(_agentWorkingTimer); return; }
              var steps = [
                '🧠 Analyse de la demande...',
                '🔍 Recherche d\'informations...',
                '⚡ Exécution des actions...',
                '📝 Rédaction de la réponse...'
              ];
              var stepIdx = Math.min(_agentWorkingSteps - 1, steps.length - 1);
              showToolIndicator(steps[stepIdx]);
            }, 3000);
          } else if (agData.phase === 'end') {
            clearInterval(_agentWorkingTimer);
          }
        } else if (agStream === 'assistant' && agData.delta) {
          // First text arriving — clear the working timer
          clearInterval(_agentWorkingTimer);
        }
      }
      return;
    }

    // Response
    if (data.type === 'res') {
      var pending = pendingRequests.get(data.id);
      if (!pending) return;
      pendingRequests.delete(data.id);
      if (data.ok) {
        pending.resolve(data.payload);
      } else {
        var errMsg = (data.error && data.error.message) ? data.error.message : 'Erreur';
        pending.reject(new Error(errMsg));
      }
      return;
    }
  }

  // --- Sprint 13: Typing label mapping for real-time activity ---
  var _typingLabels = {
    'judilibre': { emoji: '\ud83d\udd0d', text: 'Recherche sur Judilibre...', source: 'Judilibre' },
    'legifrance': { emoji: '\ud83d\udcd6', text: 'Consultation L\u00e9gifrance...', source: 'L\u00e9gifrance' },
    'gmail': { emoji: '\ud83d\udce7', text: 'Lecture des emails...', source: 'Gmail' },
    'send_email': { emoji: '\ud83d\udce7', text: 'Envoi d\u2019email...', source: 'Gmail' },
    'qonto': { emoji: '\ud83d\udcb0', text: 'Consultation bancaire...', source: 'Banque' },
    'web_search': { emoji: '\ud83c\udf10', text: 'Recherche en cours...', source: 'Web' },
    'search': { emoji: '\ud83c\udf10', text: 'Recherche en cours...', source: 'Web' },
    'google_search': { emoji: '\ud83c\udf10', text: 'Recherche en cours...', source: 'Web' },
    'notion': { emoji: '\ud83d\udccb', text: 'Consultation Notion...', source: 'Notion' },
    'whatsapp': { emoji: '\ud83d\udcac', text: 'Envoi WhatsApp...', source: 'WhatsApp' },
    'telegram': { emoji: '\ud83d\udcac', text: 'Envoi Telegram...', source: 'Telegram' },
    'crm': { emoji: '\ud83d\udccb', text: 'Consultation CRM...', source: 'CRM' },
    'eur_lex': { emoji: '\ud83c\udf10', text: 'Recherche EUR-Lex...', source: 'EUR-Lex' }
  };

  function updateTypingLabel(toolName) {
    var tn = document.getElementById('typing-name');
    var tl = tn ? tn.parentNode : null;
    if (!tl) return;
    var matched = null;
    if (toolName) {
      var lower = toolName.toLowerCase();
      for (var key in _typingLabels) {
        if (lower.indexOf(key) !== -1) { matched = _typingLabels[key]; break; }
      }
    }
    if (matched) {
      tl.innerHTML = '<span>' + matched.emoji + ' ' + matched.text + '</span>';
      pulseSourceChip(matched.source);
    } else {
      tl.innerHTML = '<span>\ud83d\udcad R\u00e9flexion en cours</span><span class="typing-dots-inline"><span></span><span></span><span></span></span>';
    }
  }

  var _activePulseTimers = {};
  var _sourceLastUsed = {};
  function pulseSourceChip(sourceName) {
    if (!sourceName) return;
    _sourceLastUsed[sourceName] = Date.now();
    var chips = document.querySelectorAll('.source-chip');
    chips.forEach(function(chip) {
      var nameEl = chip.querySelector('.source-name');
      if (nameEl && nameEl.textContent.trim() === sourceName) {
        chip.classList.add('active-pulse');
        updateSourceTooltip(chip, sourceName);
        if (_activePulseTimers[sourceName]) clearTimeout(_activePulseTimers[sourceName]);
        _activePulseTimers[sourceName] = setTimeout(function() {
          chip.classList.remove('active-pulse');
          delete _activePulseTimers[sourceName];
        }, 3000);
      }
    });
  }

  function updateSourceTooltip(chip, sourceName) {
    var ts = _sourceLastUsed[sourceName];
    if (!ts) return;
    var ago = Math.round((Date.now() - ts) / 1000);
    var label;
    if (ago < 5) label = 'en cours';
    else if (ago < 60) label = 'il y a ' + ago + 's';
    else if (ago < 3600) label = 'il y a ' + Math.round(ago / 60) + ' min';
    else label = 'il y a ' + Math.round(ago / 3600) + 'h';
    chip.title = sourceName + ' \u2014 Derni\u00e8re utilisation ' + label;
  }

  // Refresh tooltips every 30s
  setInterval(function() {
    document.querySelectorAll('.source-chip').forEach(function(chip) {
      var nameEl = chip.querySelector('.source-name');
      if (nameEl) updateSourceTooltip(chip, nameEl.textContent.trim());
    });
  }, 30000);

  function clearAllSourcePulses() {
    document.querySelectorAll('.source-chip.active-pulse').forEach(function(c) { c.classList.remove('active-pulse'); });
    for (var k in _activePulseTimers) { clearTimeout(_activePulseTimers[k]); }
    _activePulseTimers = {};
  }

  // --- Tool use contextual indicator ---
  var _toolNames = {
    'web_search': '🔍 Recherche sur le web',
    'search': '🔍 Recherche sur le web',
    'google_search': '🔍 Recherche sur le web',
    'read_file': '📄 Lecture du fichier',
    'read': '📄 Lecture du document',
    'write': '✏️ Écriture fichier',
    'edit': '✏️ Modification fichier',
    'exec': '⚡ Exécution de commande',
    'execute': '⚡ Exécution de commande',
    'bash': '⚡ Exécution terminal',
    'python': '🐍 Exécution Python',
    'send_email': '📧 Envoi d\'email',
    'gmail': '📧 Accès Gmail',
    'notion': '📋 Accès Notion',
    'qonto': '🏦 Accès Qonto',
    'whatsapp': '💬 Envoi WhatsApp',
    'telegram': '💬 Envoi Telegram',
    'legifrance': '⚖️ Recherche Légifrance',
    'judilibre': '⚖️ Recherche Judilibre',
    'eur_lex': '🇪🇺 Recherche EUR-Lex',
    'crm': '👥 Accès CRM',
    'generate': '🔨 Génération en cours',
    'analyze': '🔬 Analyse en cours',
    'calculate': '🧮 Calcul en cours'
  };

  function extractToolHint(msg) {
    if (!msg) return null;
    var content = msg.content || msg;
    if (!Array.isArray(content)) return null;
    for (var i = 0; i < content.length; i++) {
      if (content[i].type === 'tool_use' && content[i].name) {
        var name = content[i].name.toLowerCase();
        for (var key in _toolNames) {
          if (name.indexOf(key) !== -1) return _toolNames[key];
        }
        return 'Utilisation d\'outil : ' + content[i].name;
      }
    }
    return null;
  }

  var _toolIndicatorEl = null;
  var _toolStepsEl = null;
  var _toolStepCount = 0;
  var _agentWorkingTimer = null;
  var _agentWorkingSteps = 0;

  function showToolIndicator(hint) {
    // Update streaming activity label
    var actLabel = document.getElementById('streaming-activity-label');
    if (actLabel) actLabel.textContent = hint;

    // Create steps container if needed
    if (!_toolStepsEl) {
      _toolStepsEl = document.createElement('div');
      _toolStepsEl.className = 'tool-steps';
      _toolStepCount = 0;
    }

    // Add new step (avoid duplicating the same hint)
    var lastStep = _toolStepsEl.lastElementChild;
    var lastText = lastStep ? lastStep.querySelector('.tool-step-text') : null;
    if (lastText && lastText.textContent === hint) {
      // Same tool — just pulse the dot
      return;
    }

    // Mark previous step as done
    if (lastStep) {
      lastStep.classList.add('done');
      var dot = lastStep.querySelector('.tool-step-dot');
      if (dot) dot.innerHTML = '✓';
    }

    _toolStepCount++;
    var step = document.createElement('div');
    step.className = 'tool-step';
    step.innerHTML = '<span class="tool-step-dot"></span><span class="tool-step-text">' + hint + '</span>';
    _toolStepsEl.appendChild(step);

    // Insert into DOM
    if (!_toolStepsEl.parentNode) {
      var ref = $streaming.parentNode === $messages ? $streaming : null;
      if (ref) $messages.insertBefore(_toolStepsEl, ref);
      else $messages.appendChild(_toolStepsEl);
    }
    scrollToBottom(false);

    // Legacy single indicator (keep for compatibility)
    if (!_toolIndicatorEl) {
      _toolIndicatorEl = document.createElement('div');
      _toolIndicatorEl.className = 'tool-indicator';
      _toolIndicatorEl.innerHTML = '<span class="tool-indicator-dot"></span><span class="tool-indicator-text"></span>';
    }
    _toolIndicatorEl.querySelector('.tool-indicator-text').textContent = hint;
  }

  function hideToolIndicator() {
    // Clear agent working timer
    clearInterval(_agentWorkingTimer);
    _agentWorkingSteps = 0;
    // Mark last step as done
    if (_toolStepsEl) {
      var lastStep = _toolStepsEl.lastElementChild;
      if (lastStep) {
        lastStep.classList.add('done');
        var dot = lastStep.querySelector('.tool-step-dot');
        if (dot) dot.innerHTML = '✓';
      }
      // Fade out steps after a moment
      setTimeout(function() {
        if (_toolStepsEl && _toolStepsEl.parentNode) {
          _toolStepsEl.classList.add('fade-out');
          setTimeout(function() {
            if (_toolStepsEl && _toolStepsEl.parentNode) {
              _toolStepsEl.parentNode.removeChild(_toolStepsEl);
            }
            _toolStepsEl = null;
            _toolStepCount = 0;
          }, 400);
        }
      }, 800);
    }
    if (_toolIndicatorEl && _toolIndicatorEl.parentNode) {
      _toolIndicatorEl.parentNode.removeChild(_toolIndicatorEl);
    }
  }

  // --- Chat event handler (streaming) ---
  function handleChatEvent(payload) {
    if (!payload) return;

    // Check if event is for a different session -> track unread
    var eventKey = payload.sessionKey || '';
    var isCurrentSession = !eventKey || eventKey === SESSION_KEY ||
      eventKey.indexOf(':' + SESSION_KEY + ':') !== -1 ||
      eventKey.indexOf(':' + SESSION_KEY) !== -1 ||
      SESSION_KEY.indexOf(':' + eventKey) !== -1;

    if (!isCurrentSession) {
      // Track unread for other sessions (only on final messages)
      if (payload.state === 'final') {
        // Use both full key and simple key for matching
        var parts = eventKey.split(':');
        var simpleKey = parts[parts.length - 1] || eventKey;
        unreadCounts[eventKey] = (unreadCounts[eventKey] || 0) + 1;
        unreadCounts[simpleKey] = (unreadCounts[simpleKey] || 0) + 1;
        updateUnreadBadges();
      }
      return;
    }

    if (payload.state === 'delta') {
      var text = cleanText(extractText(payload.message));
      // Detect tool use for contextual indicator + typing label
      var toolHint = extractToolHint(payload.message);
      if (toolHint) {
        showToolIndicator(toolHint);
        // Sprint 13: update typing label with tool name
        var _toolRaw = null;
        var _content = payload.message && (payload.message.content || payload.message);
        if (Array.isArray(_content)) {
          for (var _ti = 0; _ti < _content.length; _ti++) {
            if (_content[_ti].type === 'tool_use' && _content[_ti].name) { _toolRaw = _content[_ti].name; break; }
          }
        }
        updateTypingLabel(_toolRaw);
      }
      if (text && text.length > 0) {
        // Clear agent working timer as soon as real text arrives
        clearInterval(_agentWorkingTimer);
        streamText = text;
        hideTyping();
        showStreaming(streamText);
        showSidebarTyping(text);
        setGenerating(true);
      }
    } else if (payload.state === 'final') {
      hideToolIndicator();
      hideTyping();
      updateTypingLabel(null);
      clearAllSourcePulses();
      hideStreaming();
      hideSidebarTyping();
      setGenerating(false);
      chatRunId = null;
      // Use final message directly - no need to reload entire history
      var finalText = cleanText(extractText(payload.message));
      if (finalText) {
        var finalImages = extractImages(payload.message);
        addMessage('assistant', finalText, payload.message ? payload.message.timestamp : Date.now(), finalImages);
        // Track received message usage
        trackUsage('received', finalText.length);
      }
      streamText = '';
      // Smart sidebar update: just update the active item's timestamp + preview
      updateSidebarActiveItem(finalText);
    } else if (payload.state === 'aborted') {
      hideTyping();
      hideSidebarTyping();
      hideToolIndicator();
      updateTypingLabel(null);
      clearAllSourcePulses();
      if (streamText) {
        addMessage('assistant', streamText);
      }
      hideStreaming();
      setGenerating(false);
      chatRunId = null;
      streamText = '';
    } else if (payload.state === 'error') {
      hideTyping();
      hideStreaming();
      hideSidebarTyping();
      hideToolIndicator();
      updateTypingLabel(null);
      clearAllSourcePulses();
      setGenerating(false);
      chatRunId = null;
      streamText = '';
      var errMsg = payload.errorMessage || 'Erreur lors de la génération';
      addMessage('assistant', '⚠ ' + errMsg);
    }
  }

  // --- Load history ---
  var HISTORY_INITIAL_COUNT = 50;
  var _pendingOlderMessages = []; // messages not yet rendered (older ones)

  function loadHistory() {
    if (!connected) return;

    request('chat.history', { sessionKey: SESSION_KEY, limit: 200 }).then(function(result) {
      var messages = result && result.messages ? result.messages : [];
      if (messages.length === 0) { showDashboard(); return; }

      // Clear current messages
      while ($messages.firstChild) $messages.removeChild($messages.firstChild);

      // Pre-process all messages
      var processed = [];
      var hasWaMessages = false;
      messages.forEach(function(msg) {
        var role = msg.role || 'assistant';
        if (role !== 'user' && role !== 'assistant') return;
        var rawText = extractText(msg);
        if (!rawText) return;
        var text = (role === 'user') ? rawText : cleanText(rawText);
        if (!text.trim()) return;
        var msgImages = extractImages(msg);
        processed.push({ role: role, text: text, timestamp: msg.timestamp, images: msgImages });
        if (role === 'user' && rawText.indexOf('untrusted metadata') !== -1) hasWaMessages = true;
      });

      // Split: render only last N, keep older ones for lazy load
      if (processed.length > HISTORY_INITIAL_COUNT) {
        _pendingOlderMessages = processed.slice(0, processed.length - HISTORY_INITIAL_COUNT);
        processed = processed.slice(processed.length - HISTORY_INITIAL_COUNT);
      } else {
        _pendingOlderMessages = [];
      }

      // Render "load more" button if there are older messages
      if (_pendingOlderMessages.length > 0) {
        var loadMoreBtn = document.createElement('div');
        loadMoreBtn.className = 'load-more-history';
        loadMoreBtn.id = 'load-more-history';
        loadMoreBtn.innerHTML = '<button class="load-more-btn">' + _pendingOlderMessages.length + ' messages precedents</button>';
        loadMoreBtn.querySelector('button').addEventListener('click', function() { loadOlderMessages(); });
        $messages.appendChild(loadMoreBtn);
      }

      // Batch render recent messages
      _batchFragment = document.createDocumentFragment();
      processed.forEach(function(m) {
        addMessage(m.role, m.text, m.timestamp, m.images);
      });
      $messages.appendChild(_batchFragment);
      _batchFragment = null;

      // SelfChat banner
      var simpleSession = SESSION_KEY.split(':').pop();
      if ((simpleSession === 'main' || SESSION_KEY === 'main') && hasWaMessages) {
        showSelfChatBanner();
      }

      scrollToBottom(false);
    }).catch(function() {
      // Silent fail for history
    });
  }

  function loadOlderMessages() {
    if (_pendingOlderMessages.length === 0) return;
    var btn = document.getElementById('load-more-history');
    var scrollRef = $messages.children[btn ? 1 : 0]; // first real message
    var scrollTopBefore = $messages.scrollTop;

    // Batch render all pending older messages
    _batchFragment = document.createDocumentFragment();
    _pendingOlderMessages.forEach(function(m) {
      addMessage(m.role, m.text, m.timestamp, m.images);
    });

    // Insert before the first real message (after load-more button position)
    if (btn) {
      btn.remove();
    }
    $messages.insertBefore(_batchFragment, $messages.firstChild);
    _batchFragment = null;
    _pendingOlderMessages = [];

    // Preserve scroll position so user doesn't jump
    if (scrollRef) {
      $messages.scrollTop = scrollRef.offsetTop - 20;
    }
  }

  // --- SelfChat mode info banner ---
  function showSelfChatBanner() {
    var existing = document.getElementById('selfchat-banner');
    if (existing) return; // Already shown
    var banner = document.createElement('div');
    banner.id = 'selfchat-banner';
    banner.className = 'selfchat-banner';
    banner.innerHTML = '<svg viewBox="0 0 24 24" width="16" height="16" fill="none" stroke="currentColor" stroke-width="2"><path d="M12 2C6.48 2 2 6.48 2 12s4.48 10 10 10 10-4.48 10-10S17.52 2 12 2z"/><path d="M12 16v-4"/><circle cx="12" cy="8" r="0.5" fill="currentColor"/></svg>' +
      '<span>Les messages WhatsApp envoyés directement à Léa arrivent dans cette session (mode selfChat)</span>' +
      '<button class="selfchat-close" title="Fermer">&times;</button>';
    banner.querySelector('.selfchat-close').addEventListener('click', function() {
      banner.remove();
    });
    $messages.insertBefore(banner, $messages.firstChild);
  }

  // --- Load agent identity ---
  function loadAgentIdentity() {
    if (!connected) return;

    // If we have admin config (from agents.json via config.php), it takes priority
    // Don't let OpenClaw gateway identity override our branding
    if (_agentConfig && _agentConfig.displayName) {
      // Already configured from admin config — skip gateway identity
      return;
    }

    request('agent.identity.get', { sessionKey: SESSION_KEY }).then(function(result) {
      if (!result) return;
      var name = result.name || '';
      var avatar = result.avatar || '';

      // Only override if no admin config set
      if (!AGENT_NAME && name) {
        $headerName.textContent = name;
        $welcomeTitle.textContent = 'Bienvenue';
      }
      if (avatar && !(_agentConfig && _agentConfig.avatar)) {
        var img = document.createElement('img');
        img.src = avatar;
        img.alt = name || '';
        img.onerror = function() { this.remove(); };
        $headerAvatar.textContent = '';
        $headerAvatar.appendChild(img);
      }
    }).catch(function() {
      // Silent fail
    });
  }


  // --- Auto-generate conversation title from first message ---
  var _titleGenerated = {};
  var STOP_WORDS_FR = ['le','la','les','un','une','des','du','de','d','l','je','tu','il','elle','on','nous','vous','ils','elles','me','te','se','mon','ma','mes','ton','ta','tes','son','sa','ses','ce','cette','ces','et','ou','mais','donc','car','ni','que','qui','dont','est','sont','a','ai','as','au','aux','en','y','ne','pas','pour','par','sur','avec','dans','plus','très','bien','faire','fait','fais','peut','peux','être','avoir','aussi','comme','tout','tous','ça','cela','ceci','votre','notre','leur','quoi','quel','quelle','quels','quelles','comment','pourquoi','combien','quand','où'];

  function extractSmartTitle(text) {
    // Flatten to single line, collapse whitespace
    var flat = text.replace(/\n/g, ' ').replace(/\s+/g, ' ').trim();
    // If short enough already, capitalize and return
    if (flat.length <= 40) {
      return flat.charAt(0).toUpperCase() + flat.slice(1);
    }
    // Remove URLs
    flat = flat.replace(/https?:\/\/\S+/g, '').trim();
    // Split into words, remove stop words and tiny words
    var stopSet = {};
    STOP_WORDS_FR.forEach(function(w) { stopSet[w] = true; });
    var words = flat.split(/\s+/);
    var keywords = [];
    for (var i = 0; i < words.length; i++) {
      var w = words[i].replace(/^[^\wÀ-ÿ]+|[^\wÀ-ÿ]+$/g, ''); // trim punctuation
      if (!w || w.length < 2) continue;
      if (stopSet[w.toLowerCase()]) continue;
      // Capitalize first keyword
      if (keywords.length === 0) {
        keywords.push(w.charAt(0).toUpperCase() + w.slice(1));
      } else {
        keywords.push(w);
      }
      // Check length
      var candidate = keywords.join(' ');
      if (candidate.length >= 35) break;
    }
    var title = keywords.join(' ');
    if (!title) {
      // Fallback: first 37 chars of original
      title = flat.substring(0, 37) + '...';
    }
    if (title.length > 40) {
      title = title.substring(0, 37) + '...';
    }
    return title;
  }

  function autoGenerateTitle(sessionKey, messageText) {
    if (!messageText || _titleGenerated[sessionKey]) return;
    // Only for auto-created sessions (chat-XXXXXXXX-XXXXXX pattern)
    var simpleKey = sessionKey.split(':').pop();
    if (!/^chat-\d{8}-\d{6}$/.test(simpleKey)) return;
    // Don't overwrite a custom title set by user via inline rename
    var renames = getSessionRenames();
    if (renames[simpleKey] && renames[simpleKey] !== 'Nouvelle conversation') return;
    _titleGenerated[sessionKey] = true;
    var title = extractSmartTitle(messageText);
    if (!title) return;
    // Save as local rename
    renames[simpleKey] = title;
    saveSessionRenames(renames);
    // Server-side persistence
    if (connected) {
      request('sessions.update', { sessionKey: sessionKey, title: title }).catch(function() {});
    }
    refreshSessionsList();
  }

  // --- Send message ---
  function sendMessage() {
    var text = $input.value.trim();
    var hasAttachments = pendingAttachments.length > 0;
    if ((!text && !hasAttachments) || !connected) return;

    // Block send if any document is still uploading
    var stillUploading = pendingAttachments.some(function(a) { return a.uploading; });
    if (stillUploading) {
      showError('Un fichier est encore en cours d\'upload...');
      setTimeout(hideError, 2000);
      return;
    }

    $input.value = '';
    $input.style.height = 'auto';

    // Show user message with image previews if any
    if (hasAttachments) {
      pendingAttachments.forEach(function(att) {
        if (att.type === 'document') {
          addMessage('user', '\ud83d\udcce ' + att.fileName);
        } else {
          addImageMessage('user', att.dataUrl, att.fileName);
        }
      });
    }
    if (text) {
      addMessage('user', text);
      // Auto-generate title for new conversations
      autoGenerateTitle(SESSION_KEY, text);
    }

    showTyping();
    setGenerating(true);

    lastUserMessage = text || '';
    streamText = '';
    var idempKey = uuid();
    chatRunId = idempKey;

    var sendParams = {
      sessionKey: SESSION_KEY,
      message: text || '(image jointe)',
      deliver: false,
      idempotencyKey: idempKey
    };

    // Add attachments if any
    if (hasAttachments) {
      var imageAtts = pendingAttachments.filter(function(a) { return a.type !== 'document'; });
      var docAtts = pendingAttachments.filter(function(a) { return a.type === 'document' && a.filePath; });
      if (imageAtts.length > 0) {
        sendParams.attachments = imageAtts.map(function(att) {
          return {
            type: 'image',
            mimeType: att.mimeType,
            fileName: att.fileName,
            content: att.base64
          };
        });
      }
      if (docAtts.length > 0) {
        var docRefs = docAtts.map(function(att) {
          var sizeKo = att.fileSize ? Math.round(att.fileSize / 1024) + ' Ko' : '?';
          return '[📎 Fichier joint: ' + att.fileName + ' (' + sizeKo + ') | Chemin serveur: ' + att.filePath + ' | Pour le lire, utilise: exec python3 -c "open(\'' + att.filePath + '\',\'rb\').read()" ou exec cat ' + att.filePath + ']';
        }).join('\n');
        var baseMsg = sendParams.message === '(image jointe)' ? 'Analyse ce document' : sendParams.message;
        sendParams.message = (baseMsg ? baseMsg + '\n\n' : '') + docRefs;
      }
    }

    // Clear attachments after sending
    pendingAttachments = [];
    renderAttachPreviews();

    // Track sent message usage
    trackUsage('sent', (text || '').length);

    request('chat.send', sendParams).catch(function(err) {
      hideTyping();
      setGenerating(false);
      chatRunId = null;
      addMessage('assistant', '⚠ Erreur : ' + err.message);
    });
  }

  // --- Abort ---
  function abortChat() {
    if (!connected) return;
    var abortParams = { sessionKey: SESSION_KEY };
    if (chatRunId) abortParams.runId = chatRunId;

    request('chat.abort', abortParams).catch(function() {});

    hideTyping();
    if (streamText) {
      addMessage('assistant', streamText);
    }
    hideStreaming();
    setGenerating(false);
    chatRunId = null;
    streamText = '';
  }

  // --- Event listeners ---
  $btnSend.addEventListener('click', sendMessage);
  $btnStop.addEventListener('click', abortChat);

  // Escape key stops generation
  document.addEventListener('keydown', function(e) {
    if (e.key === 'Escape' && _isGenerating) {
      e.preventDefault();
      abortChat();
    }
  });

  $input.addEventListener('keydown', function(e) {
    if (e.key === 'Enter' && !e.shiftKey) {
      e.preventDefault();
      sendMessage();
    }
  });


  // --- Sidebar ---
  var $sidebar = document.getElementById('sidebar');
  var $sidebarSessions = document.getElementById('sidebar-sessions');
  var $sidebarEmpty = document.getElementById('sidebar-empty');
  var $btnNewChat = document.getElementById('btn-new-chat');
  var $btnBurger = document.getElementById('btn-burger');
  var $sidebarOverlay = document.getElementById('sidebar-overlay');
  var sessionsList = [];

  // Toggle sidebar on mobile
  if ($btnBurger) {
    $btnBurger.addEventListener('click', function() {
      $sidebar.classList.toggle('open');
      $sidebarOverlay.classList.toggle('visible');
    });
  }
  if ($sidebarOverlay) {
    $sidebarOverlay.addEventListener('click', function() {
      $sidebar.classList.remove('open');
      $sidebarOverlay.classList.remove('visible');
    });
  }

  // Load sessions list
  var waContacts = {};
  // Load WhatsApp contact names
  fetch('/wa-contacts.json').then(function(r) { return r.json(); }).then(function(data) {
    waContacts = data || {};
  }).catch(function() {});

  function escapeHtml(str) {
    var div = document.createElement('div');
    div.textContent = str;
    return div.innerHTML;
  }

  function resolveSessionName(key) {
    if (waContacts[key]) return waContacts[key].name;
    if (key.indexOf('@g.us') > -1) return key.split('@')[0];
    if (key.indexOf('@s.whatsapp.net') > -1) return '+' + key.split('@')[0];
    return null;
  }

  function getSessionIcon(key) {
    if (waContacts[key] || key.indexOf('@g.us') > -1 || key.indexOf('@s.whatsapp.net') > -1) {
      return '<svg class="session-wa-icon" viewBox="0 0 24 24" fill="#25D366" width="14" height="14"><path d="M17.472 14.382c-.297-.149-1.758-.867-2.03-.967-.273-.099-.471-.148-.67.15-.197.297-.767.966-.94 1.164-.173.199-.347.223-.644.075-.297-.15-1.255-.463-2.39-1.475-.883-.788-1.48-1.761-1.653-2.059-.173-.297-.018-.458.13-.606.134-.133.298-.347.446-.52.149-.174.198-.298.298-.497.099-.198.05-.371-.025-.52-.075-.149-.669-1.612-.916-2.207-.242-.579-.487-.5-.669-.51-.173-.008-.371-.01-.57-.01-.198 0-.52.074-.792.372-.272.297-1.04 1.016-1.04 2.479 0 1.462 1.065 2.875 1.213 3.074.149.198 2.096 3.2 5.077 4.487.709.306 1.262.489 1.694.625.712.227 1.36.195 1.871.118.571-.085 1.758-.719 2.006-1.413.248-.694.248-1.289.173-1.413-.074-.124-.272-.198-.57-.347m-5.421 7.403h-.004a9.87 9.87 0 01-5.031-1.378l-.361-.214-3.741.982.998-3.648-.235-.374a9.86 9.86 0 01-1.51-5.26c.001-5.45 4.436-9.884 9.888-9.884 2.64 0 5.122 1.03 6.988 2.898a9.825 9.825 0 012.893 6.994c-.003 5.45-4.437 9.884-9.885 9.884m8.413-18.297A11.815 11.815 0 0012.05 0C5.495 0 .16 5.335.157 11.892c0 2.096.547 4.142 1.588 5.945L.057 24l6.305-1.654a11.882 11.882 0 005.683 1.448h.005c6.554 0 11.89-5.335 11.893-11.893a11.821 11.821 0 00-3.48-8.413Z"/></svg>';
    }
    return '';
  }

  function loadSessions() {
    if (!connected) return;
    request('sessions.list', {
      limit: 200,
      includeDerivedTitles: true,
      includeLastMessage: true
    }).then(function(result) {
      sessionsList = (result && result.sessions) ? result.sessions : [];
      renderSessions();
    }).catch(function() {
      $sidebarEmpty.textContent = 'Erreur chargement';
    });
  }

  function isWhatsAppSession(key) {
    return key.indexOf('@s.whatsapp.net') !== -1 || key.indexOf('@g.us') !== -1;
  }

  // Smart sidebar update: update only active conversation's preview + time
  function updateSidebarActiveItem(latestText) {
    var activeItem = $sidebarSessions.querySelector('.session-item.active');
    if (!activeItem) return;
    // Update preview text
    var preview = activeItem.querySelector('.session-preview');
    if (preview && latestText) {
      var short = latestText.replace(/\n/g, ' ').trim();
      if (short.length > 60) short = short.substring(0, 57) + '...';
      preview.textContent = short;
    }
    // Update relative time
    var timeEl = activeItem.querySelector('.session-time');
    if (timeEl) {
      timeEl.textContent = relativeTime(Date.now());
    }
    // Move active item to top of its section (most recent)
    var parent = activeItem.parentNode;
    if (parent) {
      var firstItem = parent.querySelector('.session-item');
      if (firstItem && firstItem !== activeItem) {
        parent.insertBefore(activeItem, firstItem);
      }
    }
  }

  // --- Sidebar typing indicator ---
  function showSidebarTyping(previewText) {
    var activeItem = $sidebarSessions.querySelector('.session-item.active');
    if (!activeItem) return;
    if (!activeItem.classList.contains('typing-active')) {
      activeItem.classList.add('typing-active');
    }
    var preview = activeItem.querySelector('.session-preview');
    if (preview && previewText) {
      var short = previewText.replace(/\n/g, ' ').trim();
      if (short.length > 50) short = short.substring(0, 47) + '...';
      preview.textContent = short;
    }
  }

  function hideSidebarTyping() {
    var items = $sidebarSessions.querySelectorAll('.session-item.typing-active');
    items.forEach(function(el) { el.classList.remove('typing-active'); });
  }

  // === PINNED SESSIONS ===
  function getPinnedSessions() {
    try { return JSON.parse(localStorage.getItem('mybotia-pinned') || '[]'); } catch(e) { return []; }
  }
  function savePinnedSessions(arr) {
    localStorage.setItem('mybotia-pinned', JSON.stringify(arr));
    syncPrefToServer('pinned', JSON.stringify(arr));
  }
  function togglePinSession(simpleKey) {
    var pinned = getPinnedSessions();
    var idx = pinned.indexOf(simpleKey);
    if (idx >= 0) {
      pinned.splice(idx, 1);
    } else {
      if (pinned.length >= 10) return false;
      pinned.push(simpleKey);
    }
    savePinnedSessions(pinned);
    refreshSessionsList();
    return true;
  }

  function renderSessions() {
    $sidebarSessions.innerHTML = '';

    // Filter hidden (deleted) sessions
    var hiddenSessions = getHiddenSessions();
    var filtered = sessionsList.filter(function(s) {
      var key = s.key || s.sessionKey || '';
      var parts = key.split(':');
      var simpleKey = parts[parts.length - 1] || key;
      return hiddenSessions.indexOf(simpleKey) === -1;
    });

    // Sort by most recent first (using updatedAt or key)
    var sorted = filtered.slice().sort(function(a, b) {
      var ta = a.updatedAt || a.createdAt || 0;
      var tb = b.updatedAt || b.createdAt || 0;
      return tb - ta;
    });

    // Check if current session is in the list (match by simpleKey OR full key)
    var currentFound = false;
    var currentSimple = SESSION_KEY.split(':').pop();
    sorted.forEach(function(session) {
      var key = session.key || session.sessionKey || '';
      var parts = key.split(':');
      var simpleKey = parts[parts.length - 1] || key;
      if (simpleKey === currentSimple || key === SESSION_KEY || simpleKey === SESSION_KEY) currentFound = true;
    });

    // If current session not in list, add it at the top
    if (!currentFound) {
      var displayKey = currentSimple;
      var displayTitle = displayKey;
      if (/^chat-\d{8}-\d{6}$/.test(displayKey)) {
        displayTitle = 'Nouvelle conversation';
      } else if (displayKey === 'main') {
        displayTitle = 'Principal';
      }
      sorted.unshift({
        key: SESSION_KEY,
        title: displayTitle,
        updatedAt: Date.now(),
        _isCurrent: true
      });
    }

    // === FOLDER SYSTEM ===
    var folders = JSON.parse(localStorage.getItem('mybotia-folders') || '[]');

    // Build lookup: sessionKey -> folderId (normalized to simpleKey)
    var sessionFolderMap = {};
    folders.forEach(function(f) {
      (f.sessions || []).forEach(function(sk) {
        var normalized = sk.split(':').pop() || sk;
        sessionFolderMap[normalized] = f.id;
        sessionFolderMap[sk] = f.id; // also keep original for direct match
      });
    });

    // Split sessions: in folders vs. unfiled, separate WhatsApp
    var unfiledSessions = [];
    var whatsappSessions = [];
    var folderSessions = {};
    folders.forEach(function(f) { folderSessions[f.id] = []; });

    sorted.forEach(function(session) {
      var key = session.key || session.sessionKey || '';
      var parts = key.split(':');
      var simpleKey = parts[parts.length - 1] || key;
      session._simpleKey = simpleKey;

      if (sessionFolderMap[simpleKey]) {
        folderSessions[sessionFolderMap[simpleKey]].push(session);
      } else if (isWhatsAppSession(simpleKey)) {
        whatsappSessions.push(session);
      } else {
        unfiledSessions.push(session);
      }
    });

    if (sorted.length === 0 && folders.length === 0) {
      var empty = document.createElement('div');
      empty.className = 'sidebar-empty';
      empty.textContent = 'Aucune conversation';
      $sidebarSessions.appendChild(empty);
      return;
    }

    // === PINNED SESSIONS ===
    var pinnedKeys = getPinnedSessions();
    if (pinnedKeys.length > 0) {
      var pinnedTitle = document.createElement('div');
      pinnedTitle.className = 'sessions-section-title pinned-section-title';
      pinnedTitle.innerHTML = '<svg class="pin-icon-header" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M12 17v5"/><path d="M9 11V4a1 1 0 0 1 1-1h4a1 1 0 0 1 1 1v7"/><path d="M5 11h14l-1.5 6h-11z"/></svg> Épinglées';
      $sidebarSessions.appendChild(pinnedTitle);

      pinnedKeys.forEach(function(pk) {
        var session = null;
        for (var i = 0; i < sorted.length; i++) {
          var sk = sorted[i]._simpleKey || (sorted[i].key || '').split(':').pop();
          if (sk === pk) { session = sorted[i]; break; }
        }
        if (!session) return;
        if (!session._simpleKey) session._simpleKey = pk;
        var item = createSessionItem(session);
        item.classList.add('pinned');
        $sidebarSessions.appendChild(item);
      });
    }

    // Folders header — collapsible section
    var foldersCollapsed = localStorage.getItem('mybotia-folders-collapsed') === '1';
    var foldersHeaderDiv = document.createElement('div');
    foldersHeaderDiv.className = 'sidebar-folders-header';
    foldersHeaderDiv.innerHTML = '<svg class="folders-section-chevron' + (foldersCollapsed ? ' collapsed' : '') + '" viewBox="0 0 24 24" width="12" height="12" fill="none" stroke="currentColor" stroke-width="2"><polyline points="6 9 12 15 18 9"/></svg>' +
      '<span class="sidebar-folders-title">Dossiers</span>' +
      '<span class="sidebar-folders-count">' + folders.length + '</span>' +
      '<button class="btn-add-folder" id="btn-add-folder" title="Nouveau dossier">+</button>';
    foldersHeaderDiv.style.cursor = 'pointer';
    foldersHeaderDiv.addEventListener('click', function(e) {
      if (e.target.closest('.btn-add-folder')) return;
      var wrap = document.getElementById('folders-collapsible-wrap');
      var chevron = foldersHeaderDiv.querySelector('.folders-section-chevron');
      if (wrap.style.display === 'none') {
        wrap.style.display = '';
        chevron.classList.remove('collapsed');
        localStorage.setItem('mybotia-folders-collapsed', '0');
      } else {
        wrap.style.display = 'none';
        chevron.classList.add('collapsed');
        localStorage.setItem('mybotia-folders-collapsed', '1');
      }
    });
    $sidebarSessions.appendChild(foldersHeaderDiv);

    // Collapsible wrapper for folders content
    var foldersWrap = document.createElement('div');
    foldersWrap.id = 'folders-collapsible-wrap';
    if (foldersCollapsed) foldersWrap.style.display = 'none';
    $sidebarSessions.appendChild(foldersWrap);

    // Folder create dialog container (inserted inside wrapper)
    var folderDialogContainer = document.createElement('div');
    folderDialogContainer.id = 'folder-create-container';
    foldersWrap.appendChild(folderDialogContainer);

    // Sort folders alphabetically
    folders.sort(function(a, b) {
      return (a.name || '').localeCompare(b.name || '', 'fr', { sensitivity: 'base' });
    });

    // Render each folder
    folders.forEach(function(folder) {
      var fDiv = document.createElement('div');
      fDiv.className = 'folder-item' + (folder.collapsed ? ' collapsed' : '');
      fDiv.dataset.folderId = folder.id;

      // Determine icon SVG based on folder type
      var folderType = folder.type || 'general';
      var folderIcon;
      switch (folderType) {
        case 'projet':
          folderIcon = '<svg class="folder-type-icon" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><rect x="2" y="7" width="20" height="14" rx="2" ry="2"/><path d="M16 21V5a2 2 0 0 0-2-2h-4a2 2 0 0 0-2 2v16"/></svg>';
          break;
        case 'client':
          folderIcon = '<svg class="folder-type-icon" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M20 21v-2a4 4 0 0 0-4-4H8a4 4 0 0 0-4 4v2"/><circle cx="12" cy="7" r="4"/></svg>';
          break;
        default:
          folderIcon = '<svg class="folder-type-icon" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M22 19a2 2 0 0 1-2 2H4a2 2 0 0 1-2-2V5a2 2 0 0 1 2-2h5l2 3h9a2 2 0 0 1 2 2z"/></svg>';
      }

      // Color dot
      var colorDot = folder.color ? '<span class="folder-color-dot" style="background:' + folder.color + '"></span>' : '';

      var fHeader = document.createElement('div');
      fHeader.className = 'folder-header';
      fHeader.innerHTML = '<svg class="folder-chevron" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><polyline points="6 9 12 15 18 9"/></svg>' +
        folderIcon + colorDot +
        '<span class="folder-name">' + (folder.name || 'Sans nom') + '</span>' +
        '<span class="folder-count">' + (folderSessions[folder.id] || []).length + '</span>' +
        '<span class="folder-actions">' +
          '<button class="folder-action-btn" data-action="rename" title="Renommer">&#9998;</button>' +
          '<button class="folder-action-btn" data-action="delete" title="Supprimer">&#10005;</button>' +
        '</span>';

      fHeader.addEventListener('click', function(e) {
        if (e.target.closest('.folder-action-btn')) return;
        fDiv.classList.toggle('collapsed');
        saveFolderCollapsed(folder.id, fDiv.classList.contains('collapsed'));
      });

      // Folder actions
      fHeader.querySelectorAll('.folder-action-btn').forEach(function(btn) {
        btn.addEventListener('click', function(e) {
          e.stopPropagation();
          if (btn.dataset.action === 'rename') renameFolder(folder.id);
          if (btn.dataset.action === 'delete') deleteFolder(folder.id);
        });
      });

      fDiv.appendChild(fHeader);

      // Folder sessions
      var fSessions = document.createElement('div');
      fSessions.className = 'folder-sessions';
      (folderSessions[folder.id] || []).forEach(function(session) {
        fSessions.appendChild(createSessionItem(session));
      });
      if (!folder.collapsed) {
        fSessions.style.maxHeight = ((folderSessions[folder.id] || []).length * 80) + 'px';
      }
      fDiv.appendChild(fSessions);

      foldersWrap.appendChild(fDiv);
    });

    // Unfiled sessions section - grouped by date
    if (unfiledSessions.length > 0) {
      var _now = new Date();
      var _todayStart = new Date(_now.getFullYear(), _now.getMonth(), _now.getDate()).getTime();
      var _yesterdayStart = _todayStart - 86400000;
      var _weekStart = _todayStart - 7 * 86400000;
      var _monthStart = _todayStart - 30 * 86400000;

      var dateGroups = [
        { label: "Aujourd'hui", sessions: [] },
        { label: 'Hier', sessions: [] },
        { label: '7 derniers jours', sessions: [] },
        { label: '30 derniers jours', sessions: [] },
        { label: 'Plus ancien', sessions: [] }
      ];

      unfiledSessions.forEach(function(session) {
        var t = session.updatedAt || session.createdAt || 0;
        if (t >= _todayStart) dateGroups[0].sessions.push(session);
        else if (t >= _yesterdayStart) dateGroups[1].sessions.push(session);
        else if (t >= _weekStart) dateGroups[2].sessions.push(session);
        else if (t >= _monthStart) dateGroups[3].sessions.push(session);
        else dateGroups[4].sessions.push(session);
      });

      dateGroups.forEach(function(group) {
        if (group.sessions.length === 0) return;
        var dtTitle = document.createElement('div');
        dtTitle.className = 'sessions-section-title';
        dtTitle.textContent = group.label;
        $sidebarSessions.appendChild(dtTitle);
        group.sessions.forEach(function(session) {
          $sidebarSessions.appendChild(createSessionItem(session));
        });
      });
    }

    // WhatsApp section (collapsible, separate from web conversations)
    if (whatsappSessions.length > 0) {
      var waSection = document.createElement('div');
      waSection.className = 'wa-section';
      var waCollapsed = localStorage.getItem('mybotia-wa-collapsed') === '1';
      // Force open if active session is in WhatsApp section
      var _currentSimpleWa = SESSION_KEY.split(':').pop();
      for (var _wi = 0; _wi < whatsappSessions.length; _wi++) {
        if (whatsappSessions[_wi]._simpleKey === _currentSimpleWa) { waCollapsed = false; break; }
      }

      var waHeader = document.createElement('div');
      waHeader.className = 'sessions-section-title wa-section-header';
      waHeader.innerHTML = '<svg class="wa-section-chevron' + (waCollapsed ? ' collapsed' : '') + '" viewBox="0 0 24 24" width="12" height="12" fill="none" stroke="currentColor" stroke-width="2"><polyline points="6 9 12 15 18 9"/></svg>' +
        '<svg viewBox="0 0 24 24" width="12" height="12" fill="#25D366"><path d="M17.472 14.382c-.297-.149-1.758-.867-2.03-.967-.273-.099-.471-.148-.67.15-.197.297-.767.966-.94 1.164-.173.199-.347.223-.644.075-.297-.15-1.255-.463-2.39-1.475-.883-.788-1.48-1.761-1.653-2.059-.173-.297-.018-.458.13-.606.134-.133.298-.347.446-.52.149-.174.198-.298.298-.497.099-.198.05-.371-.025-.52-.075-.149-.669-1.612-.916-2.207-.242-.579-.487-.5-.669-.51-.173-.008-.371-.01-.57-.01-.198 0-.52.074-.792.372-.272.297-1.04 1.016-1.04 2.479 0 1.462 1.065 2.875 1.213 3.074.149.198 2.096 3.2 5.077 4.487.709.306 1.262.489 1.694.625.712.227 1.36.195 1.871.118.571-.085 1.758-.719 2.006-1.413.248-.694.248-1.289.173-1.413-.074-.124-.272-.198-.57-.347m-5.421 7.403h-.004a9.87 9.87 0 01-5.031-1.378l-.361-.214-3.741.982.998-3.648-.235-.374a9.86 9.86 0 01-1.51-5.26c.001-5.45 4.436-9.884 9.888-9.884 2.64 0 5.122 1.03 6.988 2.898a9.825 9.825 0 012.893 6.994c-.003 5.45-4.437 9.884-9.885 9.884m8.413-18.297A11.815 11.815 0 0012.05 0C5.495 0 .16 5.335.157 11.892c0 2.096.547 4.142 1.588 5.945L.057 24l6.305-1.654a11.882 11.882 0 005.683 1.448h.005c6.554 0 11.89-5.335 11.893-11.893a11.821 11.821 0 00-3.48-8.413Z"/></svg>' +
        ' WhatsApp <span class="wa-section-count">' + whatsappSessions.length + '</span>';
      waHeader.style.cursor = 'pointer';
      waHeader.addEventListener('click', function() {
        var list = waSection.querySelector('.wa-session-list');
        var chevron = waHeader.querySelector('.wa-section-chevron');
        if (list.style.display === 'none') {
          list.style.display = '';
          chevron.classList.remove('collapsed');
          localStorage.setItem('mybotia-wa-collapsed', '0');
        } else {
          list.style.display = 'none';
          chevron.classList.add('collapsed');
          localStorage.setItem('mybotia-wa-collapsed', '1');
        }
      });
      waSection.appendChild(waHeader);

      var waList = document.createElement('div');
      waList.className = 'wa-session-list';
      if (waCollapsed) waList.style.display = 'none';
      whatsappSessions.forEach(function(session) {
        waList.appendChild(createSessionItem(session));
      });
      waSection.appendChild(waList);
      $sidebarSessions.appendChild(waSection);
    }

    // Apply unread badges
    updateUnreadBadges();

    // Scroll active session into view — auto-expand parent sections if needed
    requestAnimationFrame(function() {
      var activeItem = $sidebarSessions.querySelector('.session-item.active');
      if (activeItem) {
        // Expand parent folder if collapsed
        var parentFolder = activeItem.closest('.folder-item.collapsed');
        if (parentFolder) {
          parentFolder.classList.remove('collapsed');
          var fSessions = parentFolder.querySelector('.folder-sessions');
          if (fSessions) fSessions.style.maxHeight = (fSessions.scrollHeight + 100) + 'px';
        }
        // Expand folders section if collapsed
        var foldersWrap = document.getElementById('folders-collapsible-wrap');
        if (foldersWrap && foldersWrap.style.display === 'none' && activeItem.closest('#folders-collapsible-wrap')) {
          foldersWrap.style.display = '';
          var chevron = document.querySelector('.folders-section-chevron');
          if (chevron) chevron.classList.remove('collapsed');
          localStorage.setItem('mybotia-folders-collapsed', '0');
        }
        // Expand WhatsApp section if collapsed
        var waWrap = activeItem.closest('.wa-section');
        if (waWrap) {
          var waContent = waWrap.querySelector('.wa-section-content');
          if (waContent && waContent.style.display === 'none') {
            waContent.style.display = '';
            var waChevron = waWrap.querySelector('.wa-section-chevron');
            if (waChevron) waChevron.classList.remove('collapsed');
            localStorage.setItem('mybotia-wa-collapsed', '0');
          }
        }
        activeItem.scrollIntoView({ block: 'nearest', behavior: 'smooth' });
      }
    });
  }


  // --- Relative time formatting ---
  function relativeTime(ts) {
    if (!ts) return '';
    var now = Date.now();
    var diff = now - ts;
    var seconds = Math.floor(diff / 1000);
    var minutes = Math.floor(seconds / 60);
    var hours = Math.floor(minutes / 60);
    var days = Math.floor(hours / 24);
    if (seconds < 60) return "A l'instant";
    if (minutes < 60) return 'Il y a ' + minutes + ' min';
    if (hours < 24) return 'Il y a ' + hours + 'h';
    if (days === 1) return 'Hier';
    if (days < 7) return 'Il y a ' + days + 'j';
    if (days < 30) return 'Il y a ' + Math.floor(days / 7) + ' sem.';
    var d = new Date(ts);
    return d.toLocaleDateString('fr-FR', { day: '2-digit', month: 'short' });
  }

  function createSessionItem(session) {
    var simpleKey = session._simpleKey;
    var item = document.createElement('div');
    item.className = 'session-item';
    item.dataset.sessionKey = simpleKey;
    var _currentSimple = SESSION_KEY.split(':').pop();
    if (simpleKey === SESSION_KEY || simpleKey === _currentSimple ||
        (session.key || session.sessionKey || '') === SESSION_KEY) {
      item.classList.add('active');
    }

    var title = document.createElement('div');
    title.className = 'session-title';
    var resolvedName = resolveSessionName(simpleKey);
    var icon = getSessionIcon(simpleKey);
    // Check local renames
    var localRenames = getSessionRenames();
    var displayTitle = localRenames[simpleKey] || session.title || resolvedName || session.label || simpleKey;
    if (icon) {
      title.innerHTML = icon + ' ' + escapeHtml(displayTitle);
    } else {
      title.textContent = displayTitle;
    }
    item.appendChild(title);

    if (session.lastMessage) {
      var preview = document.createElement('div');
      preview.className = 'session-preview';
      var previewText = typeof session.lastMessage === 'string' ? session.lastMessage : extractText(session.lastMessage);
      previewText = cleanText(previewText);
      if (previewText.length > 60) previewText = previewText.substring(0, 60) + '...';
      preview.textContent = previewText;
      item.appendChild(preview);
    }

    if (session.updatedAt) {
      var timeDiv = document.createElement('div');
      timeDiv.className = 'session-time';
      timeDiv.textContent = relativeTime(session.updatedAt);
      item.appendChild(timeDiv);
    }

    var fullKey = session.key || session.sessionKey || simpleKey;
    item.addEventListener('click', function() {
      switchSession(fullKey);
    });

    // Double-click to rename inline
    title.addEventListener('dblclick', function(e) {
      e.stopPropagation();
      startInlineRename(simpleKey, fullKey);
    });

    // Three-dot actions button (visible on hover)
    var actionsBtn = document.createElement('button');
    actionsBtn.className = 'session-actions-btn';
    actionsBtn.innerHTML = '&#x2026;';
    actionsBtn.title = 'Actions';
    actionsBtn.addEventListener('click', function(e) {
      e.stopPropagation();
      e.preventDefault();
      showSessionContextMenu(e, simpleKey, fullKey, session.title || session.label || simpleKey);
    });
    item.appendChild(actionsBtn);

    // Right-click context menu
    item.addEventListener('contextmenu', function(e) {
      e.preventDefault();
      showSessionContextMenu(e, simpleKey, fullKey, session.title || session.label || simpleKey);
    });

    return item;
  }

  // === FOLDER CRUD ===
  function generateFolderId() {
    return 'f_' + Date.now().toString(36) + Math.random().toString(36).substr(2, 4);
  }

  function getFolders() {
    return JSON.parse(localStorage.getItem('mybotia-folders') || '[]');
  }

  function saveFolders(folders) {
    localStorage.setItem('mybotia-folders', JSON.stringify(folders));
    syncPrefToServer('folders', JSON.stringify(folders));
  }

  // --- Server preferences sync (Sprint 3.1) ---
  var prefsSyncEnabled = true;
  var prefsBaseUrl = window.location.origin + '/api/preferences.php';

  function syncPrefToServer(key, value, _retries) {
    if (!prefsSyncEnabled || !TOKEN) return;
    _retries = _retries || 0;
    var url = prefsBaseUrl + '?t=' + encodeURIComponent(TOKEN);
    var body = {};
    body[key] = (typeof value === 'string') ? value : JSON.stringify(value);
    try {
      fetch(url, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(body)
      }).then(function(res) {
        if (!res.ok && _retries < 2) {
          console.warn('[prefs] sync HTTP ' + res.status + ' for ' + key + ', retrying...');
          setTimeout(function() { syncPrefToServer(key, value, _retries + 1); }, 2000);
        }
      }).catch(function(err) {
        console.warn('[prefs] sync failed for ' + key + ':', err.message);
        if (_retries < 2) {
          setTimeout(function() { syncPrefToServer(key, value, _retries + 1); }, 3000);
        }
      });
    } catch(e) {
      console.warn('[prefs] sync error:', e.message);
    }
  }

  function loadPrefsFromServer() {
    if (!TOKEN) return Promise.resolve(null);
    var url = prefsBaseUrl + '?t=' + encodeURIComponent(TOKEN);
    return fetch(url).then(function(res) {
      if (!res.ok) throw new Error('HTTP ' + res.status);
      return res.json();
    }).then(function(data) {
      if (!data.ok || !data.preferences) return null;
      var prefs = data.preferences;

      // Sync folders: server wins if present
      if (prefs.folders) {
        try {
          var serverFolders = (typeof prefs.folders === 'string') ? JSON.parse(prefs.folders) : prefs.folders;
          if (Array.isArray(serverFolders) && serverFolders.length > 0) {
            localStorage.setItem('mybotia-folders', JSON.stringify(serverFolders));
            console.log('[prefs] Loaded ' + serverFolders.length + ' folders from server');
          }
        } catch(e) { console.warn('[prefs] Invalid folders JSON from server'); }
      }

      // Sync theme: server wins if present
      if (prefs.theme) {
        var currentTheme = localStorage.getItem('mybotia-theme') || 'dark';
        if (prefs.theme !== currentTheme) {
          localStorage.setItem('mybotia-theme', prefs.theme);
          applyTheme(prefs.theme === 'dark');
          console.log('[prefs] Applied theme from server: ' + prefs.theme);
        }
      }

      // First load: push localStorage to server if server has nothing
      if (!prefs.folders) {
        var localFolders = localStorage.getItem('mybotia-folders');
        if (localFolders) {
          syncPrefToServer('folders', localFolders);
          console.log('[prefs] Migrated local folders to server');
        }
      }
      if (!prefs.theme) {
        var localTheme = localStorage.getItem('mybotia-theme');
        if (localTheme) {
          syncPrefToServer('theme', localTheme);
          console.log('[prefs] Migrated local theme to server');
        }
      }

      return prefs;
    }).catch(function(err) {
      console.warn('[prefs] Failed to load from server, using localStorage fallback:', err.message);
      prefsSyncEnabled = false;
      return null;
    });
  }


  function saveFolderCollapsed(folderId, collapsed) {
    var folders = getFolders();
    folders.forEach(function(f) { if (f.id === folderId) f.collapsed = collapsed; });
    saveFolders(folders);
  }

  // Predefined colors for folder creation
  var FOLDER_COLORS = [
    { name: 'Violet', hex: '#a78bfa' },
    { name: 'Bleu', hex: '#3b82f6' },
    { name: 'Vert', hex: '#22c55e' },
    { name: 'Orange', hex: '#f59e0b' },
    { name: 'Rouge', hex: '#ef4444' },
    { name: 'Gris', hex: '#94a3b8' }
  ];

  function addFolder(name, type, color) {
    var folders = getFolders();
    folders.push({
      id: generateFolderId(),
      name: name || 'Nouveau dossier',
      type: type || 'general',
      color: color || '',
      collapsed: false,
      sessions: []
    });
    saveFolders(folders);
    refreshSessionsList();
  }

  function showFolderCreateDialog() {
    var container = document.getElementById('folder-create-container');
    if (!container) return;
    // Don't show if already open
    if (container.querySelector('.folder-create-dialog')) return;

    var dialog = document.createElement('div');
    dialog.className = 'folder-create-dialog';
    dialog.innerHTML =
      '<input type="text" class="folder-create-name" placeholder="Nom du dossier..." autofocus>' +
      '<div class="folder-create-row">' +
        '<select class="folder-create-type">' +
          '<option value="general">General</option>' +
          '<option value="projet">Projet</option>' +
          '<option value="client">Client</option>' +
        '</select>' +
        '<div class="folder-create-colors">' +
          FOLDER_COLORS.map(function(c) {
            return '<button class="folder-color-btn" data-color="' + c.hex + '" title="' + c.name + '" style="background:' + c.hex + '"></button>';
          }).join('') +
        '</div>' +
      '</div>' +
      '<div class="folder-create-actions">' +
        '<button class="folder-create-ok">Creer</button>' +
        '<button class="folder-create-cancel">Annuler</button>' +
      '</div>';

    container.appendChild(dialog);

    var nameInput = dialog.querySelector('.folder-create-name');
    var typeSelect = dialog.querySelector('.folder-create-type');
    var selectedColor = '';
    var colorBtns = dialog.querySelectorAll('.folder-color-btn');

    // Focus name input
    setTimeout(function() { nameInput.focus(); }, 50);

    // Color selection
    colorBtns.forEach(function(btn) {
      btn.addEventListener('click', function(e) {
        e.preventDefault();
        colorBtns.forEach(function(b) { b.classList.remove('selected'); });
        btn.classList.add('selected');
        selectedColor = btn.dataset.color;
      });
    });

    function create() {
      var name = nameInput.value.trim();
      if (!name) { nameInput.focus(); return; }
      addFolder(name, typeSelect.value, selectedColor);
      dialog.remove();
    }

    function cancel() {
      dialog.remove();
    }

    dialog.querySelector('.folder-create-ok').addEventListener('click', create);
    dialog.querySelector('.folder-create-cancel').addEventListener('click', cancel);
    nameInput.addEventListener('keydown', function(e) {
      if (e.key === 'Enter') { e.preventDefault(); create(); }
      if (e.key === 'Escape') { cancel(); }
    });
  }

  function renameFolder(folderId) {
    var el = document.querySelector('[data-folder-id="' + folderId + '"] .folder-name');
    if (!el) return;
    var oldName = el.textContent;
    var input = document.createElement('input');
    input.className = 'folder-name-input';
    input.value = oldName;
    el.replaceWith(input);
    input.focus();
    input.select();

    function save() {
      var newName = input.value.trim() || oldName;
      var folders = getFolders();
      folders.forEach(function(f) { if (f.id === folderId) f.name = newName; });
      saveFolders(folders);
      refreshSessionsList();
    }
    input.addEventListener('blur', save);
    input.addEventListener('keydown', function(e) {
      if (e.key === 'Enter') { e.preventDefault(); save(); }
      if (e.key === 'Escape') { refreshSessionsList(); }
    });
  }

  function deleteFolder(folderId) {
    mybotiaConfirm('Supprimer le dossier', 'Les conversations seront conserv\u00e9es.').then(function(ok) {
      if (!ok) return;
      var folders = getFolders();
      folders = folders.filter(function(f) { return f.id !== folderId; });
      saveFolders(folders);
      refreshSessionsList();
    });
  }

  function moveSessionToFolder(sessionKey, folderId) {
    // Always normalize to simpleKey for consistent folder storage
    var normalizedKey = sessionKey.split(':').pop() || sessionKey;
    var folders = getFolders();
    // Remove from any existing folder (check both forms)
    folders.forEach(function(f) {
      f.sessions = f.sessions.filter(function(s) {
        var sSimple = s.split(':').pop() || s;
        return sSimple !== normalizedKey;
      });
    });
    // Add to target folder (null = unfiled)
    if (folderId) {
      folders.forEach(function(f) {
        if (f.id === folderId) f.sessions.push(normalizedKey);
      });
    }
    saveFolders(folders);
    refreshSessionsList();
  }

  // --- Update unread badges in sidebar ---
  function updateUnreadBadges() {
    var items = document.querySelectorAll('.session-item');
    items.forEach(function(item) {
      var sk = item.dataset.sessionKey;
      var count = unreadCounts[sk] || 0;
      var badge = item.querySelector('.unread-badge');
      if (count > 0) {
        if (!badge) {
          badge = document.createElement('span');
          badge.className = 'unread-badge';
          item.appendChild(badge);
        }
        badge.textContent = count > 99 ? '99+' : count;
        item.classList.add('has-unread');
      } else {
        if (badge) badge.remove();
        item.classList.remove('has-unread');
      }
    });

    // Also update folder badges
    var folders = document.querySelectorAll('.folder-item');
    folders.forEach(function(fDiv) {
      var total = 0;
      fDiv.querySelectorAll('.session-item').forEach(function(item) {
        var sk = item.dataset.sessionKey;
        total += unreadCounts[sk] || 0;
      });
      var fBadge = fDiv.querySelector('.folder-unread-badge');
      if (total > 0) {
        if (!fBadge) {
          fBadge = document.createElement('span');
          fBadge.className = 'folder-unread-badge';
          fDiv.querySelector('.folder-header').appendChild(fBadge);
        }
        fBadge.textContent = total > 99 ? '99+' : total;
      } else {
        if (fBadge) fBadge.remove();
      }
    });
  }

  var _refreshTimer = null;
  function refreshSessionsList(immediate) {
    if (immediate) {
      clearTimeout(_refreshTimer);
      _refreshTimer = null;
      renderSessions();
      return;
    }
    if (_refreshTimer) return; // already scheduled
    _refreshTimer = setTimeout(function() {
      _refreshTimer = null;
      renderSessions();
    }, 100);
  }

  // === EDIT USER MESSAGE ===
  function startEditMessage(msgDiv) {
    if (msgDiv.classList.contains('editing')) return;
    var originalText = msgDiv.dataset.originalText || '';
    var bubble = msgDiv.querySelector('.msg-bubble');
    if (!bubble) return;
    msgDiv.classList.add('editing');
    var savedHTML = bubble.innerHTML;
    bubble.innerHTML = '';
    var ta = document.createElement('textarea');
    ta.className = 'msg-edit-textarea';
    ta.value = originalText;
    ta.rows = Math.min(Math.max(originalText.split('\n').length, 2), 8);
    bubble.appendChild(ta);
    var actions = document.createElement('div');
    actions.className = 'msg-edit-actions';
    var cancelBtn = document.createElement('button');
    cancelBtn.className = 'msg-edit-cancel';
    cancelBtn.textContent = 'Annuler';
    cancelBtn.addEventListener('click', function() {
      msgDiv.classList.remove('editing');
      bubble.innerHTML = savedHTML;
    });
    var sendBtn = document.createElement('button');
    sendBtn.className = 'msg-edit-send';
    sendBtn.textContent = 'Envoyer';
    sendBtn.addEventListener('click', function() {
      var newText = ta.value.trim();
      if (!newText || !connected) return;
      msgDiv.classList.remove('editing');
      bubble.innerHTML = '';
      var textDiv = document.createElement('div');
      textDiv.className = 'msg-text';
      textDiv.textContent = newText;
      bubble.appendChild(textDiv);
      msgDiv.dataset.originalText = newText;
      // Send as new message
      $input.value = newText;
      sendMessage();
    });
    actions.appendChild(cancelBtn);
    actions.appendChild(sendBtn);
    bubble.appendChild(actions);
    ta.focus();
    ta.setSelectionRange(ta.value.length, ta.value.length);
  }

  // === EXPORT CONVERSATION ===
  function exportConversation(sessionKey, title) {
    // Collect all messages from DOM
    var msgs = $messages.querySelectorAll('.msg');
    var lines = ['# ' + (title || 'Conversation') + '\n'];
    var date = new Date().toLocaleDateString('fr-FR', { year: 'numeric', month: 'long', day: 'numeric' });
    lines.push('*Exporté le ' + date + '*\n\n---\n');
    msgs.forEach(function(msg) {
      var isUser = msg.classList.contains('user');
      var bubble = msg.querySelector('.msg-bubble');
      if (!bubble) return;
      var timeEl = msg.querySelector('.msg-time');
      var time = timeEl ? timeEl.textContent : '';
      var text = bubble.textContent || '';
      if (!text.trim()) return;
      lines.push('### ' + (isUser ? 'Vous' : 'Collaborateur') + (time ? ' — ' + time : '') + '\n');
      lines.push(text.trim() + '\n');
      lines.push('');
    });
    var md = lines.join('\n');
    var blob = new Blob([md], { type: 'text/markdown;charset=utf-8' });
    var url = URL.createObjectURL(blob);
    var a = document.createElement('a');
    a.href = url;
    a.download = (title || 'conversation').replace(/[^a-zA-Z0-9àâéèêëïîôùûüÿçæœ\s\-]/gi, '').trim().replace(/\s+/g, '-').substring(0, 60) + '.md';
    document.body.appendChild(a);
    a.click();
    document.body.removeChild(a);
    URL.revokeObjectURL(url);
  }

  // === CONTEXT MENU ===
  function showSessionContextMenu(e, sessionKey, fullKey, sessionTitle) {
    closeContextMenu();
    var folders = getFolders();

    var menu = document.createElement('div');
    menu.className = 'ctx-menu';
    menu.id = 'ctx-menu';

    // Move to folder submenu
    if (folders.length > 0) {
      folders.forEach(function(f) {
        var item = document.createElement('div');
        item.className = 'ctx-menu-item';
        item.innerHTML = '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M22 19a2 2 0 0 1-2 2H4a2 2 0 0 1-2-2V5a2 2 0 0 1 2-2h5l2 3h9a2 2 0 0 1 2 2z"/></svg> ' + f.name;
        item.addEventListener('click', function() {
          moveSessionToFolder(sessionKey, f.id);
          closeContextMenu();
        });
        menu.appendChild(item);
      });

      // Option to remove from folder
      var currentFolder = null;
      folders.forEach(function(f) {
        if (f.sessions.indexOf(sessionKey) >= 0) currentFolder = f;
      });
      if (currentFolder) {
        var sep = document.createElement('div');
        sep.className = 'ctx-menu-sep';
        menu.appendChild(sep);
        var removeItem = document.createElement('div');
        removeItem.className = 'ctx-menu-item';
        removeItem.innerHTML = '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><line x1="18" y1="6" x2="6" y2="18"/><line x1="6" y1="6" x2="18" y2="18"/></svg> Retirer du dossier';
        removeItem.addEventListener('click', function() {
          moveSessionToFolder(sessionKey, null);
          closeContextMenu();
        });
        menu.appendChild(removeItem);
      }
    }

    // Create new folder with this session
    if (folders.length > 0) {
      var sep2 = document.createElement('div');
      sep2.className = 'ctx-menu-sep';
      menu.appendChild(sep2);
    }
    var newFolderItem = document.createElement('div');
    newFolderItem.className = 'ctx-menu-item';
    newFolderItem.innerHTML = '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M22 19a2 2 0 0 1-2 2H4a2 2 0 0 1-2-2V5a2 2 0 0 1 2-2h5l2 3h9a2 2 0 0 1 2 2z"/><line x1="12" y1="11" x2="12" y2="17"/><line x1="9" y1="14" x2="15" y2="14"/></svg> Nouveau dossier...';
    newFolderItem.addEventListener('click', function() {
      closeContextMenu();
      mybotiaPrompt('Nom du dossier', '').then(function(name) {
        if (name && name.trim()) {
          var folders2 = getFolders();
          var newId = generateFolderId();
          folders2.push({ id: newId, name: name.trim(), collapsed: false, sessions: [sessionKey] });
          saveFolders(folders2);
          refreshSessionsList();
        }
      });
    });
    menu.appendChild(newFolderItem);

    // --- Separator ---
    var sep3 = document.createElement('div');
    sep3.className = 'ctx-menu-sep';
    menu.appendChild(sep3);

    // Pin / Unpin
    var pinned = getPinnedSessions();
    var isPinned = pinned.indexOf(sessionKey) >= 0;
    var pinItem = document.createElement('div');
    pinItem.className = 'ctx-menu-item';
    pinItem.innerHTML = isPinned
      ? '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><line x1="18" y1="6" x2="6" y2="18"/><line x1="6" y1="6" x2="18" y2="18"/></svg> Désépingler'
      : '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M12 17v5"/><path d="M9 11V4a1 1 0 0 1 1-1h4a1 1 0 0 1 1 1v7"/><path d="M5 11h14l-1.5 6h-11z"/></svg> Épingler';
    pinItem.addEventListener('click', function() {
      closeContextMenu();
      var ok = togglePinSession(sessionKey);
      if (!ok) {
        mybotiaAlert('Limite atteinte', 'Maximum 10 sessions épinglées.');
      }
    });
    menu.appendChild(pinItem);

    // Rename
    var renameItem = document.createElement('div');
    renameItem.className = 'ctx-menu-item';
    renameItem.innerHTML = '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M17 3a2.828 2.828 0 1 1 4 4L7.5 20.5 2 22l1.5-5.5L17 3z"/></svg> Renommer';
    renameItem.addEventListener('click', function() {
      closeContextMenu();
      startInlineRename(sessionKey, fullKey);
    });
    menu.appendChild(renameItem);

    // Export Markdown
    var exportItem = document.createElement('div');
    exportItem.className = 'ctx-menu-item';
    exportItem.innerHTML = '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M21 15v4a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2v-4"/><polyline points="7 10 12 15 17 10"/><line x1="12" y1="15" x2="12" y2="3"/></svg> Exporter (.md)';
    exportItem.addEventListener('click', function() {
      closeContextMenu();
      exportConversation(sessionKey, sessionTitle);
    });
    menu.appendChild(exportItem);

    // Delete
    var deleteItem = document.createElement('div');
    deleteItem.className = 'ctx-menu-item danger';
    deleteItem.innerHTML = '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><polyline points="3 6 5 6 21 6"/><path d="M19 6v14a2 2 0 0 1-2 2H7a2 2 0 0 1-2-2V6m3 0V4a2 2 0 0 1 2-2h4a2 2 0 0 1 2 2v2"/></svg> Supprimer';
    deleteItem.addEventListener('click', function() {
      closeContextMenu();
      mybotiaConfirm('Supprimer la conversation', sessionTitle).then(function(ok) {
        if (ok) deleteSession(sessionKey);
      });
    });
    menu.appendChild(deleteItem);

    // Position
    menu.style.left = Math.min(e.clientX, window.innerWidth - 200) + 'px';
    menu.style.top = Math.min(e.clientY, window.innerHeight - 250) + 'px';

    document.body.appendChild(menu);

    setTimeout(function() {
      document.addEventListener('click', closeContextMenu, { once: true });
    }, 10);
  }

  function closeContextMenu() {
    var existing = document.getElementById('ctx-menu');
    if (existing) existing.remove();
  }

  // --- Session rename (local storage fallback) ---
  function getSessionRenames() {
    try { return JSON.parse(localStorage.getItem('mybotia-session-renames') || '{}'); } catch(e) { return {}; }
  }
  function saveSessionRenames(map) {
    localStorage.setItem('mybotia-session-renames', JSON.stringify(map));
  }

  function renameSession(simpleKey, fullKey, newName) {
    // Always save to localStorage with simpleKey (display reads it this way)
    var renames = getSessionRenames();
    renames[simpleKey] = newName;
    saveSessionRenames(renames);
    // API with fullKey (agent:xxx:slug) for server-side persistence
    if (connected && fullKey) {
      request('sessions.update', { sessionKey: fullKey, title: newName }).catch(function() {});
    }
    refreshSessionsList(true);
  }

  // --- Inline rename (double-click or context menu) ---
  function startInlineRename(simpleKey, fullKey, onDone) {
    var item = document.querySelector('.session-item[data-session-key="' + simpleKey + '"]');
    if (!item) return;
    var titleEl = item.querySelector('.session-title');
    if (!titleEl || titleEl.classList.contains('editing')) return;

    var currentText = titleEl.textContent.trim();
    titleEl.classList.add('editing');

    var input = document.createElement('input');
    input.type = 'text';
    input.className = 'session-title-input';
    input.value = currentText;
    input.maxLength = 60;

    // Replace title content with input
    titleEl.textContent = '';
    titleEl.appendChild(input);
    input.focus();
    input.select();

    var saved = false;
    function save() {
      if (saved) return;
      saved = true;
      var newName = input.value.trim();
      titleEl.classList.remove('editing');

      if (newName && newName !== currentText) {
        titleEl.textContent = newName;
        renameSession(simpleKey, fullKey, newName);
        // Visual feedback
        item.classList.add('rename-success');
        setTimeout(function() { item.classList.remove('rename-success'); }, 1200);
      } else {
        titleEl.textContent = currentText;
      }
      if (onDone) onDone(newName || currentText);
    }

    function cancel() {
      if (saved) return;
      saved = true;
      titleEl.classList.remove('editing');
      titleEl.textContent = currentText;
      if (onDone) onDone(null);
    }

    input.addEventListener('keydown', function(e) {
      if (e.key === 'Enter') { e.preventDefault(); save(); }
      if (e.key === 'Escape') { e.preventDefault(); cancel(); }
    });
    input.addEventListener('blur', function() {
      setTimeout(save, 100);
    });
    input.addEventListener('click', function(e) { e.stopPropagation(); });
  }

  // --- Session delete ---
  function getHiddenSessions() {
    try { return JSON.parse(localStorage.getItem('mybotia-session-hidden') || '[]'); } catch(e) { return []; }
  }
  function saveHiddenSessions(arr) {
    localStorage.setItem('mybotia-session-hidden', JSON.stringify(arr));
  }

  function deleteSession(sessionKey) {
    // Try OpenClaw API first
    if (connected) {
      request('sessions.delete', { sessionKey: sessionKey }).then(function() {
        // If we were viewing the deleted session, switch to a new one
        if (SESSION_KEY === sessionKey) {
          switchSession('main');
        }
        refreshSessionsList();
      }).catch(function() {
        // API not supported — hide locally
        var hidden = getHiddenSessions();
        if (hidden.indexOf(sessionKey) === -1) hidden.push(sessionKey);
        saveHiddenSessions(hidden);
        // Also remove from folders
        var folders = getFolders();
        folders.forEach(function(f) {
          var idx = f.sessions.indexOf(sessionKey);
          if (idx >= 0) f.sessions.splice(idx, 1);
        });
        saveFolders(folders);
        if (SESSION_KEY === sessionKey) {
          switchSession('main');
        }
        refreshSessionsList();
      });
    } else {
      var hidden = getHiddenSessions();
      if (hidden.indexOf(sessionKey) === -1) hidden.push(sessionKey);
      saveHiddenSessions(hidden);
      if (SESSION_KEY === sessionKey) {
        switchSession('main');
      }
      refreshSessionsList();
    }
  }

  function switchSession(newKey) {
    // Clear unread count for the session we're switching to
    var parts = newKey.split(':');
    var simpleKey = parts[parts.length - 1] || newKey;
    delete unreadCounts[newKey];
    delete unreadCounts[simpleKey];

    if (newKey === SESSION_KEY) {
      $sidebar.classList.remove('open');
      $sidebarOverlay.classList.remove('visible');
      return;
    }
    // Switch session WITHOUT page reload
    SESSION_KEY = newKey;
    localStorage.setItem('mybotia-session', newKey);

    // Update URL without reload
    var url = new URL(window.location.href);
    url.searchParams.set('session', newKey);
    window.history.replaceState(null, '', url.toString());

    // Clear chat area
    while ($messages.firstChild) $messages.removeChild($messages.firstChild);
    streamText = '';
    chatRunId = null;
    setGenerating(false);
    hideTyping();
    hideStreaming();

    // Show dashboard immediately (will be removed if history loads)
    showDashboard();

    // Load new session via WebSocket
    if (connected) {
      loadHistory();
      loadAgentIdentity();
    }

    // Update sidebar active state
    refreshSessionsList(true);

    // Close sidebar on mobile
    $sidebar.classList.remove('open');
    $sidebarOverlay.classList.remove('visible');
  }

  // Folder add button (event delegation since it's re-rendered)
  $sidebarSessions.addEventListener('click', function(e) {
    var addBtn = e.target.closest('#btn-add-folder');
    if (addBtn) {
      showFolderCreateDialog();
    }
  });

  // New chat button — instant creation with proper agent prefix
  $btnNewChat.addEventListener('click', function() {
    var now = new Date();
    var ts = now.getFullYear().toString() +
      String(now.getMonth() + 1).padStart(2, '0') +
      String(now.getDate()).padStart(2, '0') + '-' +
      String(now.getHours()).padStart(2, '0') +
      String(now.getMinutes()).padStart(2, '0') +
      String(now.getSeconds()).padStart(2, '0');
    var chatSlug = 'chat-' + ts;
    // Build proper prefixed key matching the agent namespace
    var currentParts = SESSION_KEY.split(':');
    var newKey;
    if (currentParts.length >= 2 && currentParts[0] === 'agent') {
      // Current key is agent:XXX:YYY — keep agent:XXX: prefix
      newKey = currentParts.slice(0, -1).join(':') + ':' + chatSlug;
    } else {
      newKey = chatSlug;
    }
    switchSession(newKey);
    // Open inline rename on the new session after DOM is rebuilt
    setTimeout(function() {
      startInlineRename(chatSlug, newKey);
    }, 50);
  });

  // Refresh sessions after connecting (hook into existing connect success)
  var _origLoadAgentIdentity = loadAgentIdentity;




  // --- Keyboard shortcuts ---
  document.addEventListener('keydown', function(e) {
    // Ctrl+Shift+N (or Cmd+Shift+N on Mac) = New conversation
    if ((e.ctrlKey || e.metaKey) && e.shiftKey && e.key === 'N') {
      e.preventDefault();
      e.stopPropagation();
      $btnNewChat.click();
    }
    // Escape = close sidebar on mobile
    if (e.key === 'Escape') {
      if ($sidebar.classList.contains('open')) {
        $sidebar.classList.remove('open');
        $sidebarOverlay.classList.remove('visible');
      }
    }
  });

  // --- Voice recognition (Web Speech API) ---
  var $btnMic = document.getElementById('btn-mic');
  var $recIndicator = document.getElementById('recording-indicator');
  var speechRecognition = null;
  var isRecording = false;

  // Check support
  var SpeechRecognition = window.SpeechRecognition || window.webkitSpeechRecognition;
  if (!SpeechRecognition) {
    $btnMic.classList.add('unsupported');
    $btnMic.title = 'Reconnaissance vocale non supportée par ce navigateur';
  } else {
    speechRecognition = new SpeechRecognition();
    speechRecognition.lang = 'fr-FR';
    speechRecognition.continuous = true;
    speechRecognition.interimResults = true;
    speechRecognition.maxAlternatives = 1;

    var finalTranscript = '';
    var interimTranscript = '';

    speechRecognition.onresult = function(event) {
      interimTranscript = '';
      for (var i = event.resultIndex; i < event.results.length; i++) {
        var transcript = event.results[i][0].transcript;
        if (event.results[i].isFinal) {
          finalTranscript += transcript + ' ';
        } else {
          interimTranscript += transcript;
        }
      }
      // Update input with final + interim
      $input.value = finalTranscript + interimTranscript;
      $input.style.height = 'auto';
      $input.style.height = Math.min($input.scrollHeight, 120) + 'px';
      // Keep focus on our page
      $input.focus();
    };

    speechRecognition.onerror = function(event) {
      if (event.error === 'no-speech') return; // Ignore silence
      if (event.error === 'aborted') return;
      stopRecording();
      if (event.error === 'not-allowed') {
        showError('Microphone non autorisé. Vérifiez les permissions du navigateur.');
      } else {
        showError('Erreur micro : ' + event.error);
      }
      setTimeout(hideError, 4000);
    };

    speechRecognition.onend = function() {
      // If still in recording mode, restart (continuous workaround)
      if (isRecording) {
        try { speechRecognition.start(); } catch(e) { stopRecording(); }
      }
    };

    $btnMic.addEventListener('click', function(e) {
      e.preventDefault();
      e.stopPropagation();
      if ($btnMic.classList.contains('unsupported')) return;
      // Keep focus on our input to prevent other apps from stealing it
      $input.focus();
      if (isRecording) {
        stopRecording();
      } else {
        startRecording();
      }
    });
  }

  function startRecording() {
    if (!speechRecognition) return;
    isRecording = true;
    finalTranscript = $input.value || '';
    interimTranscript = '';
    $btnMic.classList.add('recording');
    $recIndicator.classList.add('visible');
    $btnMic.title = 'Arrêter la dictée';
    // Focus input to keep this page active and prevent other apps from stealing focus
    $input.focus();
    window.focus();
    try {
      speechRecognition.start();
    } catch(e) {
      // Already started
    }
  }

  function stopRecording() {
    isRecording = false;
    $btnMic.classList.remove('recording');
    $recIndicator.classList.remove('visible');
    $btnMic.title = 'Dictée vocale';
    if (speechRecognition) {
      try { speechRecognition.stop(); } catch(e) {}
    }
    // Clean up: set final value
    if (finalTranscript.trim()) {
      $input.value = finalTranscript.trim();
      $input.style.height = 'auto';
      $input.style.height = Math.min($input.scrollHeight, 120) + 'px';
    }
  }

  // --- Sidebar toggle (desktop) ---
  var $btnSidebarToggle = document.getElementById('btn-sidebar-toggle');
  var $iconSidebarShow = document.getElementById('icon-sidebar-show');
  var $iconSidebarHide = document.getElementById('icon-sidebar-hide');

  function setSidebarVisible(visible) {
    if (visible) {
      $sidebar.classList.remove('collapsed');
      $iconSidebarShow.style.display = 'none';
      $iconSidebarHide.style.display = 'block';
      $btnSidebarToggle.title = 'Masquer la sidebar';
    } else {
      $sidebar.classList.add('collapsed');
      $iconSidebarShow.style.display = 'block';
      $iconSidebarHide.style.display = 'none';
      $btnSidebarToggle.title = 'Afficher la sidebar';
    }
    try { localStorage.setItem('mybotia-sidebar', visible ? '1' : '0'); } catch(e) {}
  }

  if ($btnSidebarToggle) {
    $btnSidebarToggle.addEventListener('click', function() {
      var isVisible = !$sidebar.classList.contains('collapsed');
      setSidebarVisible(!isVisible);
    });
    // Restore preference
    try {
      var saved = localStorage.getItem('mybotia-sidebar');
      if (saved === '0') setSidebarVisible(false);
    } catch(e) {}
  }

  // --- Theme toggle ---
  var $btnTheme = document.getElementById('btn-theme');
  var $iconMoon = document.getElementById('icon-moon');
  var $iconSun = document.getElementById('icon-sun');

  function applyTheme(dark) {
    if (dark) {
      document.body.classList.add('dark');
      $iconMoon.style.display = 'none';
      $iconSun.style.display = 'block';
      $btnTheme.title = 'Mode clair';
    } else {
      document.body.classList.remove('dark');
      $iconMoon.style.display = 'block';
      $iconSun.style.display = 'none';
      $btnTheme.title = 'Mode sombre';
    }
    try { localStorage.setItem('mybotia-theme', dark ? 'dark' : 'light'); } catch(e) {}
    syncPrefToServer('theme', dark ? 'dark' : 'light');
  }

  // Load saved preference
  var savedTheme = 'dark';
  try { savedTheme = localStorage.getItem('mybotia-theme') || 'dark'; } catch(e) {}
  applyTheme(savedTheme === 'dark');

  $btnTheme.addEventListener('click', function() {
    var isDark = document.body.classList.contains('dark');
    applyTheme(!isDark);
  });


  var $accountProfile = document.getElementById('account-profile');
  var $accountMenu = document.getElementById('account-menu');

  if ($accountProfile && $accountMenu) {
    $accountProfile.addEventListener('click', function(e) {
      e.stopPropagation();
      $accountMenu.classList.toggle('visible');
    });

    document.addEventListener('click', function() {
      $accountMenu.classList.remove('visible');
    });

    $accountMenu.addEventListener('click', function(e) {
      e.stopPropagation();
    });

    // Menu items
    document.getElementById('menu-profile').addEventListener('click', function() {
      $accountMenu.classList.remove('visible');
      if (_clientInfo && _authType === 'email') {
        openProfilePanel();
      } else {
        mybotiaAlert('Profil', 'Non disponible avec une connexion par token.');
      }
    });
    // === SPRINT 13: Usage panel ===
    var $usagePanel = document.getElementById('usage-panel');
    var $usageOverlay = document.getElementById('usage-overlay');
    var $usageClose = document.getElementById('usage-panel-close');

    function openUsagePanel() {
      if (!$usagePanel || !$usageOverlay) return;
      $usageOverlay.classList.add('visible');
      $usagePanel.classList.add('visible');
      loadUsagePanelData();
    }
    function closeUsagePanel() {
      if ($usagePanel) $usagePanel.classList.remove('visible');
      if ($usageOverlay) $usageOverlay.classList.remove('visible');
    }
    if ($usageClose) $usageClose.addEventListener('click', closeUsagePanel);
    if ($usageOverlay) $usageOverlay.addEventListener('click', closeUsagePanel);

    function loadUsagePanelData() {
      fetch('/api/usage.php', { method: 'GET', credentials: 'same-origin' })
        .then(function(r) { return r.json(); })
        .then(function(data) {
          if (!data.ok) return;
          var u = data.usage;
          var pct = parseFloat(u.percentage) || 0;
          var used = u.tokens_used || 0;
          var max = u.tokens_max || 1;

          // Percentage
          var $pct = document.getElementById('usage-pct');
          if ($pct) $pct.textContent = pct.toFixed(1) + ' %';

          // Bar color
          var $bar = document.getElementById('usage-bar-fill');
          if ($bar) {
            $bar.style.width = Math.min(pct, 100) + '%';
            $bar.className = 'usage-quota-bar-fill';
            var remaining = 100 - pct;
            if (remaining > 50) $bar.classList.add('green');
            else if (remaining > 20) $bar.classList.add('orange');
            else $bar.classList.add('red');
          }

          // Tokens detail
          var $used = document.getElementById('usage-tokens-used');
          var $max = document.getElementById('usage-tokens-max');
          if ($used) $used.textContent = formatNumber(used) + ' utilis\u00e9s';
          if ($max) $max.textContent = formatNumber(max) + ' total';

          // Estimate remaining messages
          var $est = document.getElementById('usage-estimate');
          if ($est) {
            var sent = parseInt(u.messages_sent) || 0;
            var received = parseInt(u.messages_received) || 0;
            var totalMsgs = sent + received;
            if (totalMsgs > 0 && used > 0) {
              var avgPerMsg = used / totalMsgs;
              var tokensLeft = max - used;
              var msgsLeft = Math.floor(tokensLeft / avgPerMsg);
              $est.textContent = '\u2248 ' + msgsLeft + ' messages restants (estimation)';
            } else {
              $est.textContent = '';
            }
          }

          // Period
          var $period = document.getElementById('usage-period');
          if ($period) {
            var now = new Date();
            var firstDay = new Date(now.getFullYear(), now.getMonth(), 1);
            var lastDay = new Date(now.getFullYear(), now.getMonth() + 1, 0);
            var mois = ['janvier','f\u00e9vrier','mars','avril','mai','juin','juillet','ao\u00fbt','septembre','octobre','novembre','d\u00e9cembre'];
            $period.textContent = 'P\u00e9riode : 1er ' + mois[now.getMonth()] + ' - ' + lastDay.getDate() + ' ' + mois[now.getMonth()] + ' ' + now.getFullYear();
          }

          // History bars (7 last days)
          var $histBars = document.getElementById('usage-history-bars');
          if ($histBars) {
            $histBars.innerHTML = '';
            var history = u.daily_history || null;
            var days = [];
            var jours = ['Dim','Lun','Mar','Mer','Jeu','Ven','Sam'];
            for (var d = 6; d >= 0; d--) {
              var dt = new Date();
              dt.setDate(dt.getDate() - d);
              var key = dt.toISOString().slice(0, 10);
              var val = (history && history[key]) ? history[key] : Math.round(used / 7 * (0.5 + Math.random()));
              days.push({ label: jours[dt.getDay()], value: val });
            }
            var maxVal = Math.max.apply(null, days.map(function(d) { return d.value; })) || 1;
            days.forEach(function(day) {
              var col = document.createElement('div');
              col.className = 'usage-history-bar-col';
              var bar = document.createElement('div');
              bar.className = 'usage-history-bar';
              bar.style.height = Math.max(2, (day.value / maxVal) * 60) + 'px';
              bar.title = formatNumber(day.value) + ' tokens';
              var label = document.createElement('div');
              label.className = 'usage-history-bar-label';
              label.textContent = day.label;
              col.appendChild(bar);
              col.appendChild(label);
              $histBars.appendChild(col);
            });
          }
        }).catch(function() { });
    }

    var $menuUsage = document.getElementById('menu-usage');
    if ($menuUsage) {
      $menuUsage.addEventListener('click', function() {
        $accountMenu.classList.remove('visible');
        if (_authType === 'email') {
          openUsagePanel();
        } else {
          mybotiaAlert('Usage', 'Non disponible avec une connexion par token.');
        }
      });
    }
    document.getElementById('menu-settings').addEventListener('click', function() {
      $accountMenu.classList.remove('visible');
      openSettingsPanel();
    });
    document.getElementById('btn-logout-visible').addEventListener('click', function() {
      doLogout();
    });
    document.getElementById('menu-logout').addEventListener('click', function() {
      $accountMenu.classList.remove('visible');
      mybotiaConfirm('D\u00e9connexion', 'Voulez-vous vous d\u00e9connecter ?').then(function(ok) {
        if (ok) doLogout();
      });
    });
  }

  // --- Client sidebar update ---
  // --- Agent-specific UI: hide/show sources and dashboard cards per agent ---
  // --- Dynamic cards from admin config ---
  var _cardIconMap = {
    calendar: '<svg viewBox="0 0 24 24" width="28" height="28" fill="none" stroke="currentColor" stroke-width="1.5"><rect x="3" y="4" width="18" height="18" rx="2"/><line x1="16" y1="2" x2="16" y2="6"/><line x1="8" y1="2" x2="8" y2="6"/><line x1="3" y1="10" x2="21" y2="10"/></svg>',
    briefcase: '<svg viewBox="0 0 24 24" width="28" height="28" fill="none" stroke="currentColor" stroke-width="1.5"><rect x="2" y="7" width="20" height="14" rx="2"/><path d="M16 7V5a2 2 0 0 0-2-2h-4a2 2 0 0 0-2 2v2"/></svg>',
    search: '<svg viewBox="0 0 24 24" width="28" height="28" fill="none" stroke="currentColor" stroke-width="1.5"><circle cx="11" cy="11" r="8"/><line x1="21" y1="21" x2="16.65" y2="16.65"/></svg>',
    mail: '<svg viewBox="0 0 24 24" width="28" height="28" fill="none" stroke="currentColor" stroke-width="1.5"><path d="M4 4h16c1.1 0 2 .9 2 2v12c0 1.1-.9 2-2 2H4c-1.1 0-2-.9-2-2V6c0-1.1.9-2 2-2z"/><polyline points="22,6 12,13 2,6"/></svg>',
    bank: '<svg viewBox="0 0 24 24" width="28" height="28" fill="none" stroke="currentColor" stroke-width="1.5"><path d="M3 21h18M3 10h18M5 6l7-3 7 3M4 10v11M20 10v11M8 14v3M12 14v3M16 14v3"/></svg>',
    edit: '<svg viewBox="0 0 24 24" width="28" height="28" fill="none" stroke="currentColor" stroke-width="1.5"><path d="M17 3a2.828 2.828 0 1 1 4 4L7.5 20.5 2 22l1.5-5.5L17 3z"/></svg>',
    doc: '<svg viewBox="0 0 24 24" width="28" height="28" fill="none" stroke="currentColor" stroke-width="1.5"><path d="M14 2H6a2 2 0 0 0-2 2v16a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2V8z"/><polyline points="14 2 14 8 20 8"/><line x1="16" y1="13" x2="8" y2="13"/><line x1="16" y1="17" x2="8" y2="17"/></svg>',
    gavel: '<svg viewBox="0 0 24 24" width="28" height="28" fill="none" stroke="currentColor" stroke-width="1.5"><path d="M14.5 2.5L18 6l-8 8-3.5-3.5 8-8z"/><path d="M2 22l4-4"/><path d="M22 2l-6 6"/><line x1="2" y1="22" x2="8" y2="22"/></svg>',
    folder: '<svg viewBox="0 0 24 24" width="28" height="28" fill="none" stroke="currentColor" stroke-width="1.5"><path d="M22 19a2 2 0 0 1-2 2H4a2 2 0 0 1-2-2V5a2 2 0 0 1 2-2h5l2 3h9a2 2 0 0 1 2 2z"/></svg>',
    chart: '<svg viewBox="0 0 24 24" width="28" height="28" fill="none" stroke="currentColor" stroke-width="1.5"><line x1="18" y1="20" x2="18" y2="10"/><line x1="12" y1="20" x2="12" y2="4"/><line x1="6" y1="20" x2="6" y2="14"/></svg>',
    users: '<svg viewBox="0 0 24 24" width="28" height="28" fill="none" stroke="currentColor" stroke-width="1.5"><path d="M17 21v-2a4 4 0 0 0-4-4H5a4 4 0 0 0-4 4v2"/><circle cx="9" cy="7" r="4"/><path d="M23 21v-2a4 4 0 0 0-3-3.87"/><path d="M16 3.13a4 4 0 0 1 0 7.75"/></svg>'
  };

  function renderDynamicCards(cards) {
    var container = document.getElementById('suggestions');
    if (!container) return;
    container.innerHTML = '';
    cards.forEach(function(card) {
      var el = document.createElement('div');
      el.className = 'dashboard-card';
      el.dataset.prompt = card.prompt || '';
      el.innerHTML = '<div class="dashboard-card-icon">' + (_cardIconMap[card.icon] || _cardIconMap.doc) + '</div>' +
        '<div class="dashboard-card-text"><div class="dashboard-card-title">' + (card.title || '') + '</div>' +
        '<div class="dashboard-card-desc">' + (card.desc || '') + '</div></div>';
      container.appendChild(el);
    });
    // Re-bind click events
    container.querySelectorAll('.dashboard-card').forEach(function(card) {
      card.addEventListener('click', function() {
        var p = card.dataset.prompt;
        if (p && connected) { $input.value = p; $input.focus(); }
      });
    });
  }

  function configureAgentUI(subdomain) {
    // Define allowed sources per agent (by source-name text)
    var agentSources = {
      max:     ['Légifrance', 'Judilibre', 'EUR-Lex', 'CEDH', 'Gmail', 'WhatsApp', 'Notion', 'Web', 'CRM'],
      eva:     ['Web'],
      nina:    ['Gmail', 'WhatsApp', 'Telegram', 'Notion', 'Web'],
      oscar:   ['Gmail', 'WhatsApp', 'Notion', 'Web', 'CRM'],
      julian:  ['Légifrance', 'Judilibre', 'EUR-Lex', 'CEDH', 'Gmail', 'Notion', 'Web']
    };
    // Define allowed cards per agent (by dashboard-card-title text)
    var agentCards = {
      max:  ['Recherche juridique', 'Analyse de document', 'Consultation juridique', 'Suivi de dossier'],
      eva:  ['Présentation commerciale', 'Analyse de marché', 'Email commercial', 'Stratégie commerciale']
    };

    var allowedSources = agentSources[subdomain];
    if (allowedSources) {
      var chips = document.querySelectorAll('.source-chip');
      for (var i = 0; i < chips.length; i++) {
        var nameEl = chips[i].querySelector('.source-name');
        if (nameEl && allowedSources.indexOf(nameEl.textContent) === -1) {
          chips[i].style.display = 'none';
        } else {
          chips[i].style.display = '';
        }
      }
    }

    var allowedCards = agentCards[subdomain];
    if (allowedCards) {
      var cards = document.querySelectorAll('.dashboard-card');
      for (var j = 0; j < cards.length; j++) {
        var titleEl = cards[j].querySelector('.dashboard-card-title');
        if (titleEl && allowedCards.indexOf(titleEl.textContent) === -1) {
          cards[j].style.display = 'none';
        } else {
          cards[j].style.display = '';
        }
      }
    }
  }

    function updateClientSidebar(data) {
    var $avatar = document.getElementById('account-avatar');
    var $name = document.getElementById('account-name');
    var $badge = document.getElementById('account-badge');
    var $creditsValue = document.getElementById('credits-value');
    var $creditsFill = document.getElementById('credits-fill');
    var $collabSelector = document.getElementById('collab-selector');
    var $collabSelect = document.getElementById('collab-select');

    if (data.client) {
      // Company name + initials
      var company = data.client.company_name || '';
      var contact = data.client.contact_name || '';
      if ($name) $name.textContent = company || contact || 'Client';
      if ($avatar) {
        if (data.client.photo_url) {
          $avatar.innerHTML = '<img src="' + data.client.photo_url + '" style="width:100%;height:100%;object-fit:cover;border-radius:50%;" alt="">';
        } else {
          var initials = company ? company.split(' ').map(function(w){return w[0]}).join('').substring(0,2).toUpperCase() : '?';
          $avatar.textContent = initials;
        }
      }
      if ($badge) {
        var plan = (data.client.plan || 'pro').toUpperCase();
        $badge.textContent = plan;
        $badge.className = 'plan-badge ' + (data.client.plan || 'pro');
      }
    }

    // Usage bar
    if (data.usage) {
      var pct = data.usage.percentage || 0;
      if ($creditsValue) $creditsValue.textContent = formatNumber(data.usage.tokens_used) + ' / ' + formatNumber(data.usage.tokens_max);
      if ($creditsFill) {
        $creditsFill.style.width = Math.min(pct, 100) + '%';
        // Color: green < 60%, orange 60-85%, red > 85%
        if (pct > 85) $creditsFill.style.background = 'linear-gradient(90deg, #ef4444, #dc2626)';
        else if (pct > 60) $creditsFill.style.background = 'linear-gradient(90deg, #f59e0b, #d97706)';
        else $creditsFill.style.background = 'linear-gradient(90deg, #a78bfa, #7c3aed)';
      }
    }

    // Collaborateur selector (only if multiple)
    if (data.collaborateurs && data.collaborateurs.length > 1 && $collabSelector && $collabSelect) {
      $collabSelector.style.display = 'block';
      $collabSelect.innerHTML = '';
      data.collaborateurs.forEach(function(c) {
        var opt = document.createElement('option');
        opt.value = c.subdomain;
        opt.textContent = c.name + (c.role ? ' — ' + c.role : '');
        if (c.subdomain === data.active_collaborateur) opt.selected = true;
        $collabSelect.appendChild(opt);
      });
    } else if ($collabSelector) {
      $collabSelector.style.display = 'none';
    }
  }

  // Collaborateur switch handler — redirect to proper subdomain for clean state
  var $collabSelect = document.getElementById('collab-select');
  if ($collabSelect) {
    $collabSelect.addEventListener('change', function() {
      var newSub = $collabSelect.value;
      if (!newSub || newSub === _activeCollab) return;
      // Update server-side active collaborateur
      fetch('/api/auth.php', {
        method: 'PATCH',
        headers: { 'Content-Type': 'application/json' },
        credentials: 'same-origin',
        body: JSON.stringify({ subdomain: newSub })
      }).then(function() {
        // Redirect to the collaborateur's own subdomain for clean UI
        var newUrl = window.location.protocol + '//' + newSub + '.mybotia.com';
        window.location.href = newUrl;
      }).catch(function(err) {
        console.error('[collab switch]', err);
        // Fallback: reload current page
        window.location.reload();
      });
    });
  }

  // Format number with spaces (French style)
  function formatNumber(n) {
    if (n === null || n === undefined) return '--';
    return n.toString().replace(/\B(?=(\d{3})+(?!\d))/g, ' ');
  }

  // --- Usage tracking ---
  function trackUsage(direction, charCount) {
    if (_authType !== 'email' || !_clientInfo) return;
    fetch('/api/usage.php', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      credentials: 'same-origin',
      body: JSON.stringify({
        collaborateur: _activeCollab,
        direction: direction,
        char_count: charCount
      })
    }).then(function(r) { return r.json(); }).then(function(data) {
      if (data.ok && data.usage) {
        // Update the credits bar in real-time
        var $creditsValue = document.getElementById('credits-value');
        var $creditsFill = document.getElementById('credits-fill');
        var pct = data.usage.percentage || 0;
        if ($creditsValue) $creditsValue.textContent = formatNumber(data.usage.tokens_used) + ' / ' + formatNumber(data.usage.tokens_max);
        if ($creditsFill) {
          $creditsFill.style.width = Math.min(pct, 100) + '%';
          if (pct > 85) $creditsFill.style.background = 'linear-gradient(90deg, #ef4444, #dc2626)';
          else if (pct > 60) $creditsFill.style.background = 'linear-gradient(90deg, #f59e0b, #d97706)';
          else $creditsFill.style.background = 'linear-gradient(90deg, #a78bfa, #7c3aed)';
        }
      }
    }).catch(function() {});
  }

  // --- Init ---
  // Auth is handled by initAuth() above


  // === PREMIUM V11 ===
  var SVG_COPY='<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><rect x="9" y="9" width="13" height="13" rx="2"/><path d="M5 15H4a2 2 0 0 1-2-2V4a2 2 0 0 1 2-2h9a2 2 0 0 1 2 2v1"/></svg>';
  var SVG_CHECK='<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><polyline points="20 6 9 17 4 12"/></svg>';
  var SVG_LIKE='<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M14 9V5a3 3 0 0 0-3-3l-4 9v11h11.28a2 2 0 0 0 2-1.7l1.38-9a2 2 0 0 0-2-2.3zM7 22H4a2 2 0 0 1-2-2v-7a2 2 0 0 1 2-2h3"/></svg>';
  var SVG_DISLIKE='<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M10 15v4a3 3 0 0 0 3 3l4-9V2H5.72a2 2 0 0 0-2 1.7l-1.38 9a2 2 0 0 0 2 2.3zm7-13h2.67A2.31 2.31 0 0 1 22 4v7a2.31 2.31 0 0 1-2.33 2H17"/></svg>';
  var SVG_REGEN='<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><polyline points="23 4 23 10 17 10"/><path d="M20.49 15a9 9 0 1 1-2.12-9.36L23 10"/></svg>';
  var lastUserMessage='';

  // --- Feedback persistence ---
  var _msgCounter = 0;
  function sendFeedback(rating, msgIndex, preview) {
    fetch('/api/feedback.php', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      credentials: 'same-origin',
      body: JSON.stringify({
        session_key: SESSION_KEY,
        message_index: msgIndex,
        rating: rating,
        message_preview: (preview || '').substring(0, 200)
      })
    }).catch(function() {});
  }

  function createActionBar(md){
    var msgIdx = ++_msgCounter;
    md.dataset.msgIndex = msgIdx;
    var b=document.createElement('div');b.className='msg-actions';
    var c=document.createElement('button');c.className='msg-action';c.title='Copier';c.innerHTML=SVG_COPY;
    c.onclick=function(e){e.stopPropagation();var t=md.querySelector('.msg-bubble');var tx=t?t.textContent:'';
      navigator.clipboard.writeText(tx).then(function(){c.innerHTML=SVG_CHECK;c.classList.add('flash');
      setTimeout(function(){c.innerHTML=SVG_COPY;c.classList.remove('flash')},1500)}).catch(function(){
      var ta=document.createElement('textarea');ta.value=tx;ta.style.cssText='position:fixed;opacity:0';
      document.body.appendChild(ta);ta.select();document.execCommand('copy');document.body.removeChild(ta);
      c.innerHTML=SVG_CHECK;c.classList.add('flash');setTimeout(function(){c.innerHTML=SVG_COPY;c.classList.remove('flash')},1500)})};
    b.appendChild(c);
    var lk=document.createElement('button');lk.className='msg-action';lk.title='Bonne r\u00e9ponse';lk.innerHTML=SVG_LIKE;
    var dk=document.createElement('button');dk.className='msg-action';dk.title='Mauvaise r\u00e9ponse';dk.innerHTML=SVG_DISLIKE;
    lk.onclick=function(e){e.stopPropagation();
      var wasLiked=lk.classList.contains('liked');
      lk.classList.toggle('liked');dk.classList.remove('disliked');
      lk.classList.add('flash');setTimeout(function(){lk.classList.remove('flash')},300);
      var preview=md.querySelector('.msg-bubble')?md.querySelector('.msg-bubble').textContent:'';
      sendFeedback(wasLiked?'none':'like',msgIdx,preview)};
    dk.onclick=function(e){e.stopPropagation();
      var wasDisliked=dk.classList.contains('disliked');
      dk.classList.toggle('disliked');lk.classList.remove('liked');
      dk.classList.add('flash');setTimeout(function(){dk.classList.remove('flash')},300);
      var preview=md.querySelector('.msg-bubble')?md.querySelector('.msg-bubble').textContent:'';
      sendFeedback(wasDisliked?'none':'dislike',msgIdx,preview)};
    b.appendChild(lk);b.appendChild(dk);
    var rg=document.createElement('button');rg.className='msg-action';rg.title='R\u00e9g\u00e9n\u00e9rer';rg.innerHTML=SVG_REGEN;
    rg.onclick=function(e){e.stopPropagation();var _msg=md.dataset.userText||lastUserMessage||'';if(_msg&&connected){rg.classList.add('flash');setTimeout(function(){rg.classList.remove('flash')},300);$input.value=_msg;sendMessage()}};
    b.appendChild(rg);return b}

  function addCopyButtons(bubble){
    if(bubble.dataset.copyDone)return;bubble.dataset.copyDone='1';
    var links=bubble.querySelectorAll('a[href]');
    for(var i=0;i<links.length;i++){var b=document.createElement('button');b.className='copy-btn';b.setAttribute('data-copy-url',links[i].href);b.title='Copier le lien';b.innerHTML=SVG_COPY;links[i].insertAdjacentElement('afterend',b)}
    var pres=bubble.querySelectorAll('pre');
    for(var j=0;j<pres.length;j++){var ce=pres[j].querySelector('code')||pres[j];var cb=document.createElement('button');cb.className='copy-btn pre-copy';cb.setAttribute('data-copy-code','1');cb.title='Copier le code';cb.innerHTML=SVG_COPY;pres[j].style.position='relative';pres[j].appendChild(cb)}
  }

  // --- Link previews ---
  var _previewCache = {};
  function addLinkPreviews(bubble) {
    var links = bubble.querySelectorAll('a[href^="http"]');
    if (!links.length) return;
    // Only preview first 3 external links
    var count = 0;
    for (var i = 0; i < links.length && count < 3; i++) {
      var href = links[i].href;
      // Skip internal links, images, action links
      if (href.indexOf('mybotia.com') !== -1 || href.match(/\.(png|jpg|gif|svg|pdf)$/i)) continue;
      count++;
      (function(link, url) {
        if (_previewCache[url]) { renderLinkPreview(bubble, _previewCache[url]); return; }
        fetch('/api/link-preview.php?url=' + encodeURIComponent(url))
          .then(function(r) { return r.json(); })
          .then(function(data) {
            if (data.title) {
              _previewCache[url] = data;
              renderLinkPreview(bubble, data);
            }
          }).catch(function() {});
      })(links[i], href);
    }
  }

  function renderLinkPreview(bubble, data) {
    var card = document.createElement('a');
    card.href = data.url;
    card.target = '_blank';
    card.rel = 'noopener';
    card.className = 'link-preview-card';
    var html = '';
    if (data.image) {
      html += '<img class="link-preview-img" src="' + data.image.replace(/"/g, '&quot;') + '" alt="" loading="lazy" onerror="this.style.display=\'none\'">';
    }
    html += '<div class="link-preview-body">';
    if (data.site_name) html += '<div class="link-preview-site">' + data.site_name + '</div>';
    html += '<div class="link-preview-title">' + (data.title || '').replace(/</g, '&lt;') + '</div>';
    if (data.description) html += '<div class="link-preview-desc">' + data.description.substring(0, 120).replace(/</g, '&lt;') + '</div>';
    html += '</div>';
    card.innerHTML = html;
    bubble.appendChild(card);
  }
  $messages.addEventListener('click',function(e){
    var btn=e.target.closest('.copy-btn');if(!btn)return;e.preventDefault();e.stopPropagation();
    var text='';
    if(btn.hasAttribute('data-copy-url'))text=btn.getAttribute('data-copy-url');
    else if(btn.hasAttribute('data-copy-code')){var pre=btn.closest('pre');var code=pre?(pre.querySelector('code')||pre):null;text=code?code.textContent:''}
    if(!text)return;
    navigator.clipboard.writeText(text).then(function(){btn.innerHTML=SVG_CHECK;btn.classList.add('ok');setTimeout(function(){btn.innerHTML=SVG_COPY;btn.classList.remove('ok')},1500)}).catch(function(){var ta=document.createElement('textarea');ta.value=text;ta.style.cssText='position:fixed;opacity:0';document.body.appendChild(ta);ta.select();document.execCommand('copy');document.body.removeChild(ta);btn.innerHTML=SVG_CHECK;btn.classList.add('ok');setTimeout(function(){btn.innerHTML=SVG_COPY;btn.classList.remove('ok')},1500)})});

  document.querySelectorAll('.dashboard-card').forEach(function(card){
    card.addEventListener('click',function(){
      var p=card.getAttribute('data-prompt');
      if(p&&connected){$input.value=p;sendMessage()}
    })});
  function updateTypingAvatar(){
    var ta=document.getElementById('typing-avatar');
    var tn=document.getElementById('typing-name');
    if(ta&&$headerAvatar){var img=$headerAvatar.querySelector('img');
      if(img){ta.innerHTML='';ta.appendChild(img.cloneNode(true))}
      else{ta.textContent=$headerAvatar.textContent||'M'}}
    if(tn&&$headerName){tn.textContent=$headerName.textContent||"Votre collaborateur"}}


  // === PROFILE PANEL ===
  var $profilePanel = document.getElementById('profile-panel');
  var $profileOverlay = document.getElementById('profile-overlay');
  var $profileClose = document.getElementById('profile-panel-close');
  var $profilePhotoInput = document.getElementById('profile-photo-input');
  var $btnUploadPhoto = document.getElementById('btn-upload-photo');
  var $btnSaveProfile = document.getElementById('btn-save-profile');
  var $profileSyncStatus = document.getElementById('profile-sync-status');

  function openProfilePanel() {
    if (!$profilePanel || !$profileOverlay) return;
    $profileOverlay.classList.add('visible');
    $profilePanel.classList.add('visible');
    loadProfileData();
  }

  function closeProfilePanel() {
    if ($profilePanel) $profilePanel.classList.remove('visible');
    if ($profileOverlay) $profileOverlay.classList.remove('visible');
    if ($profileSyncStatus) $profileSyncStatus.textContent = '';
  }

  if ($profileClose) $profileClose.addEventListener('click', closeProfilePanel);
  if ($profileOverlay) $profileOverlay.addEventListener('click', closeProfilePanel);

  function loadProfileData() {
    fetch('/api/profile.php', { method: 'GET', credentials: 'same-origin' })
      .then(function(r) { return r.json(); })
      .then(function(data) {
        if (!data.ok) return;
        var p = data.profile;
        var el;

        // Photo
        var img = document.getElementById('profile-photo-img');
        var placeholder = document.getElementById('profile-photo-placeholder');
        if (p.photo_url) {
          if (img) { img.src = p.photo_url + '?t=' + Date.now(); img.style.display = 'block'; }
          if (placeholder) placeholder.style.display = 'none';
        } else {
          if (img) img.style.display = 'none';
          if (placeholder) {
            var initials = p.company_name ? p.company_name.split(' ').map(function(w){return w[0]}).join('').substring(0,2).toUpperCase() : '?';
            placeholder.textContent = initials;
            placeholder.style.display = 'flex';
          }
        }

        // Fields
        el = document.getElementById('profile-contact-name');
        if (el) el.value = p.contact_name || '';
        el = document.getElementById('profile-company-name');
        if (el) el.value = p.company_name || '';
        el = document.getElementById('profile-email');
        if (el) el.value = p.email || '';
        el = document.getElementById('profile-plan');
        if (el) el.value = (p.plan || 'pro').toUpperCase();

        // Global instructions
        el = document.getElementById('profile-instructions-global');
        if (el) el.value = data.instructions['_global'] || '';

        // Per-collaborateur instructions
        renderCollabInstructions(data.collaborateurs, data.instructions);
      }).catch(function(err) {
        console.error('[profile] Load error:', err);
      });
  }

  function renderCollabInstructions(collaborateurs, instructions) {
    var container = document.getElementById('profile-collab-instructions');
    if (!container) return;
    container.innerHTML = '';

    if (!collaborateurs || collaborateurs.length === 0) {
      container.innerHTML = '<p style="color:#64748b;font-size:13px;">Aucun collaborateur configur\u00e9.</p>';
      return;
    }

    collaborateurs.forEach(function(c) {
      var block = document.createElement('div');
      block.className = 'profile-collab-block';
      block.innerHTML = '<div class="profile-collab-block-header">' +
        '<span class="profile-collab-name">' + (c.name || c.subdomain) + '</span>' +
        '<span class="profile-collab-role">' + (c.role || '') + '</span>' +
        '</div>' +
        '<textarea class="profile-collab-textarea" data-subdomain="' + c.subdomain + '" ' +
        'rows="3" maxlength="5000" placeholder="Instructions sp\u00e9cifiques pour ' + (c.name || c.subdomain) + '...">' +
        (instructions[c.subdomain] || '') + '</textarea>';
      container.appendChild(block);
    });
  }

  // Photo upload
  if ($btnUploadPhoto) {
    $btnUploadPhoto.addEventListener('click', function() {
      if ($profilePhotoInput) $profilePhotoInput.click();
    });
  }
  var $profilePhotoWrapper = document.getElementById('profile-photo-wrapper');
  if ($profilePhotoWrapper) {
    $profilePhotoWrapper.addEventListener('click', function() {
      if ($profilePhotoInput) $profilePhotoInput.click();
    });
  }

  if ($profilePhotoInput) {
    $profilePhotoInput.addEventListener('change', function() {
      var file = $profilePhotoInput.files[0];
      if (!file) return;
      if (file.size > 2 * 1024 * 1024) {
        mybotiaAlert('Photo', 'Trop volumineuse (max 2 Mo).');
        return;
      }
      if (!file.type.match(/^image\/(jpeg|png|webp)$/)) {
        mybotiaAlert('Format', 'Non support\u00e9. Utilisez JPEG, PNG ou WebP.');
        return;
      }

      $btnUploadPhoto.textContent = 'Upload...';
      $btnUploadPhoto.disabled = true;

      var formData = new FormData();
      formData.append('photo', file);

      fetch('/api/profile.php', {
        method: 'POST',
        credentials: 'same-origin',
        body: formData
      }).then(function(r) { return r.json(); })
        .then(function(data) {
          $btnUploadPhoto.textContent = 'Changer la photo';
          $btnUploadPhoto.disabled = false;
          if (data.ok && data.photo_url) {
            // Update panel photo
            var img = document.getElementById('profile-photo-img');
            var placeholder = document.getElementById('profile-photo-placeholder');
            if (img) { img.src = data.photo_url + '?t=' + Date.now(); img.style.display = 'block'; }
            if (placeholder) placeholder.style.display = 'none';
            // Update sidebar avatar
            updateSidebarAvatar(data.photo_url);
            if (_clientInfo) _clientInfo.photo_url = data.photo_url;
          } else {
            mybotiaAlert('Erreur', data.error || 'Erreur lors de l\u2019upload.');
          }
        }).catch(function(err) {
          $btnUploadPhoto.textContent = 'Changer la photo';
          $btnUploadPhoto.disabled = false;
          mybotiaAlert('Erreur', 'Erreur r\u00e9seau. V\u00e9rifiez votre connexion.');
        });

      $profilePhotoInput.value = '';
    });
  }

  function updateSidebarAvatar(photoUrl) {
    var $avatar = document.getElementById('account-avatar');
    if (!$avatar) return;
    if (photoUrl) {
      $avatar.innerHTML = '<img src="' + photoUrl + '?t=' + Date.now() + '" style="width:100%;height:100%;object-fit:cover;border-radius:50%;" alt="Photo">';
    }
  }

  // Save profile
  if ($btnSaveProfile) {
    $btnSaveProfile.addEventListener('click', function() {
      $btnSaveProfile.disabled = true;
      $btnSaveProfile.innerHTML = '<span class="login-spinner"></span>Synchronisation...';
      if ($profileSyncStatus) $profileSyncStatus.textContent = '';

      var contactName = document.getElementById('profile-contact-name');
      var globalInstr = document.getElementById('profile-instructions-global');

      var instructions = {};
      if (globalInstr) instructions['_global'] = globalInstr.value.trim();

      var collabTextareas = document.querySelectorAll('.profile-collab-textarea');
      for (var i = 0; i < collabTextareas.length; i++) {
        var sub = collabTextareas[i].getAttribute('data-subdomain');
        if (sub) instructions[sub] = collabTextareas[i].value.trim();
      }

      var body = { instructions: instructions };
      if (contactName) body.contact_name = contactName.value.trim();

      fetch('/api/profile.php', {
        method: 'PUT',
        headers: { 'Content-Type': 'application/json' },
        credentials: 'same-origin',
        body: JSON.stringify(body)
      }).then(function(r) { return r.json(); })
        .then(function(data) {
          $btnSaveProfile.disabled = false;
          $btnSaveProfile.innerHTML = '<svg viewBox="0 0 24 24" width="16" height="16" fill="none" stroke="currentColor" stroke-width="2"><path d="M19 21H5a2 2 0 0 1-2-2V5a2 2 0 0 1 2-2h11l5 5v11a2 2 0 0 1-2 2z"/><polyline points="17 21 17 13 7 13 7 21"/><polyline points="7 3 7 8 15 8"/></svg>Sauvegarder et synchroniser';
          if (data.ok) {
            var syncMsg = '';
            if (data.synced && data.synced.length > 0) {
              syncMsg = '\u2705 Synchronis\u00e9 avec ' + data.synced.join(', ');
            } else {
              syncMsg = '\u2705 Profil sauvegard\u00e9';
            }
            if ($profileSyncStatus) $profileSyncStatus.textContent = syncMsg;
            // Update sidebar name if changed
            if (contactName && _clientInfo) {
              _clientInfo.contact_name = contactName.value.trim();
            }
            // Auto-hide status after 5s
            setTimeout(function() {
              if ($profileSyncStatus) $profileSyncStatus.textContent = '';
            }, 5000);
          } else {
            if ($profileSyncStatus) {
              $profileSyncStatus.style.color = '#ef4444';
              $profileSyncStatus.textContent = '\u274c ' + (data.error || 'Erreur');
              setTimeout(function() {
                $profileSyncStatus.style.color = '#10b981';
                $profileSyncStatus.textContent = '';
              }, 5000);
            }
          }
        }).catch(function(err) {
          $btnSaveProfile.disabled = false;
          $btnSaveProfile.innerHTML = '<svg viewBox="0 0 24 24" width="16" height="16" fill="none" stroke="currentColor" stroke-width="2"><path d="M19 21H5a2 2 0 0 1-2-2V5a2 2 0 0 1 2-2h11l5 5v11a2 2 0 0 1-2 2z"/><polyline points="17 21 17 13 7 13 7 21"/><polyline points="7 3 7 8 15 8"/></svg>Sauvegarder et synchroniser';
          if ($profileSyncStatus) {
            $profileSyncStatus.style.color = '#ef4444';
            $profileSyncStatus.textContent = '\u274c Erreur r\u00e9seau';
          }
        });
    });
  }

  // ============================================================
  // SETTINGS PANEL — Parametres du collaborateur IA
  // ============================================================

  var $settingsPanel = document.getElementById('settings-panel');
  var $settingsOverlay = document.getElementById('settings-overlay');
  var $settingsClose = document.getElementById('settings-panel-close');
  var $settingsAvatarUrl = document.getElementById('settings-avatar-url');
  var $settingsAvatarImg = document.getElementById('settings-avatar-img');
  var $settingsAvatarPlaceholder = document.getElementById('settings-avatar-placeholder');
  var $settingsAvatarPreview = document.getElementById('settings-avatar-preview');
  var $settingsBtnApply = document.getElementById('settings-btn-apply-avatar');
  var $settingsBtnReset = document.getElementById('settings-btn-reset-avatar');
  var $settingsAgentName = document.getElementById('settings-agent-name');
  var $settingsAgentRole = document.getElementById('settings-agent-role');
  var $settingsAgentSubdomain = document.getElementById('settings-agent-subdomain');
  var $settingsHealth = document.getElementById('settings-health');
  var $settingsStatus = document.getElementById('settings-status');

  function openSettingsPanel() {
    if (!$settingsPanel) return;
    $settingsPanel.classList.add('open');
    if ($settingsOverlay) $settingsOverlay.classList.add('open');

    // Populate current agent info
    if (_agentConfig) {
      if ($settingsAgentName) $settingsAgentName.value = _agentConfig.displayName || _agentConfig.name || '';
      if ($settingsAgentRole) $settingsAgentRole.value = _agentConfig.role || '';
      if ($settingsAvatarUrl) $settingsAvatarUrl.value = _agentConfig.avatar || '';
      updateSettingsAvatarPreview(_agentConfig.avatar || '');
    } else {
      if ($settingsAgentName) $settingsAgentName.value = AGENT_NAME || '';
      if ($settingsAgentRole) $settingsAgentRole.value = $headerRole ? $headerRole.textContent : '';
    }
    if ($settingsAgentSubdomain) $settingsAgentSubdomain.value = _subdomain || '—';

    // Load health status
    loadSettingsHealth();
  }

  function closeSettingsPanel() {
    if ($settingsPanel) $settingsPanel.classList.remove('open');
    if ($settingsOverlay) $settingsOverlay.classList.remove('open');
  }

  function updateSettingsAvatarPreview(url) {
    if (!$settingsAvatarImg || !$settingsAvatarPlaceholder) return;
    if (url) {
      $settingsAvatarImg.src = url;
      $settingsAvatarImg.style.display = 'block';
      $settingsAvatarPlaceholder.style.display = 'none';
      $settingsAvatarImg.onerror = function() {
        $settingsAvatarImg.style.display = 'none';
        $settingsAvatarPlaceholder.style.display = 'flex';
        $settingsAvatarPlaceholder.textContent = '!';
      };
    } else {
      $settingsAvatarImg.style.display = 'none';
      $settingsAvatarPlaceholder.style.display = 'flex';
      var name = _agentConfig ? (_agentConfig.displayName || _agentConfig.name || '?') : '?';
      $settingsAvatarPlaceholder.textContent = name.charAt(0).toUpperCase();
    }
  }

  function applyAvatarUrl() {
    var url = $settingsAvatarUrl ? $settingsAvatarUrl.value.trim() : '';

    // Validation
    if (url && !isValidUrl(url)) {
      showSettingsStatus('URL invalide', 'error');
      return;
    }

    if (!_subdomain) {
      showSettingsStatus('Sous-domaine non detecte', 'error');
      return;
    }

    // Disable button
    if ($settingsBtnApply) {
      $settingsBtnApply.disabled = true;
      $settingsBtnApply.innerHTML = 'Enregistrement...';
    }

    // Call API to save avatar
    var body = { subdomain: _subdomain, avatar: url };
    if (TOKEN) body.admin_token = TOKEN;

    fetch('/api/agent-settings.php', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      credentials: 'same-origin',
      body: JSON.stringify(body)
    }).then(function(res) { return res.json(); }).then(function(data) {
      if (data.ok) {
        // Update local state
        if (_agentConfig) _agentConfig.avatar = url;

        // Update avatar preview in settings
        updateSettingsAvatarPreview(url);

        // Update header avatar
        var $ha = document.getElementById('header-avatar');
        if ($ha) {
          if (url) {
            $ha.textContent = '';
            var img = document.createElement('img');
            img.src = url;
            img.alt = AGENT_NAME;
            img.onerror = function() { this.remove(); $ha.textContent = (AGENT_NAME || 'M').charAt(0); };
            $ha.appendChild(img);
          } else {
            $ha.textContent = (AGENT_NAME || 'M').charAt(0);
          }
        }

        // Update dashboard avatar
        var $da = document.getElementById('dashboard-avatar');
        if ($da) {
          if (url) {
            $da.innerHTML = '<img src="' + url + '" alt="' + (AGENT_NAME || '') + '" style="width:100%;height:100%;object-fit:cover;border-radius:50%;">';
          } else {
            $da.innerHTML = '<img src="https://res.cloudinary.com/dniurvpzd/image/upload/v1772032713/Logo_Collaborateur_IA_coujhr.svg" alt="Collaborateur ia">';
          }
        }

        // Update typing avatar
        if (typeof updateTypingAvatar === 'function') updateTypingAvatar();

        showSettingsStatus('Avatar mis a jour avec succes', 'success');
      } else {
        showSettingsStatus(data.error || 'Erreur lors de la sauvegarde', 'error');
      }
    }).catch(function(err) {
      showSettingsStatus('Erreur reseau: ' + err.message, 'error');
    }).finally(function() {
      if ($settingsBtnApply) {
        $settingsBtnApply.disabled = false;
        $settingsBtnApply.innerHTML = '<svg viewBox="0 0 24 24" width="14" height="14" fill="none" stroke="currentColor" stroke-width="2"><polyline points="20 6 9 17 4 12"/></svg> Appliquer';
      }
    });
  }

  function resetAvatar() {
    if ($settingsAvatarUrl) $settingsAvatarUrl.value = '';
    applyAvatarUrl();
  }

  function isValidUrl(str) {
    try { new URL(str); return true; }
    catch(e) { return false; }
  }

  function showSettingsStatus(msg, type) {
    if (!$settingsStatus) return;
    $settingsStatus.textContent = msg;
    $settingsStatus.className = 'settings-status';
    if (type === 'success') $settingsStatus.style.color = '#22c55e';
    else if (type === 'error') $settingsStatus.style.color = '#ef4444';
    else $settingsStatus.style.color = '';
    // Auto-clear after 4s
    setTimeout(function() {
      if ($settingsStatus) $settingsStatus.textContent = '';
    }, 4000);
  }

  function loadSettingsHealth() {
    if (!$settingsHealth) return;
    $settingsHealth.innerHTML = '<div class="settings-health-loading">Chargement...</div>';
    fetch('/api/health.php')
      .then(function(r) { return r.json(); })
      .then(function(data) {
        var html = '';
        if (data.status) {
          html += '<div class="settings-health-item"><span>Gateway</span><span style="color:' + (data.status === 'ok' ? '#22c55e' : '#ef4444') + '">' + data.status + '</span></div>';
        }
        if (data.version) {
          html += '<div class="settings-health-item"><span>Version</span><span>' + data.version + '</span></div>';
        }
        if (data.uptime) {
          html += '<div class="settings-health-item"><span>Uptime</span><span>' + data.uptime + '</span></div>';
        }
        $settingsHealth.innerHTML = html || '<div class="settings-health-item"><span>Statut</span><span style="color:#22c55e">OK</span></div>';
      })
      .catch(function() {
        $settingsHealth.innerHTML = '<div class="settings-health-item"><span>Statut</span><span style="color:#f59e0b">Indisponible</span></div>';
      });
  }

  // Event listeners
  if ($settingsClose) $settingsClose.addEventListener('click', closeSettingsPanel);
  if ($settingsOverlay) $settingsOverlay.addEventListener('click', closeSettingsPanel);
  if ($settingsBtnApply) $settingsBtnApply.addEventListener('click', applyAvatarUrl);
  if ($settingsBtnReset) $settingsBtnReset.addEventListener('click', resetAvatar);

  // Live preview: update avatar preview as user types URL
  if ($settingsAvatarUrl) {
    var previewTimeout = null;
    $settingsAvatarUrl.addEventListener('input', function() {
      clearTimeout(previewTimeout);
      previewTimeout = setTimeout(function() {
        var url = $settingsAvatarUrl.value.trim();
        if (url && isValidUrl(url)) {
          updateSettingsAvatarPreview(url);
        }
      }, 500);
    });
  }


  // === SIDEBAR SEARCH ===
  var $sidebarSearch = document.getElementById('sidebar-search');
  var $sidebarSearchClear = document.getElementById('sidebar-search-clear');
  var $sidebarSearchResults = document.getElementById('sidebar-search-results');
  var searchDebounceTimer = null;

  function highlightText(el, query) {
    var text = el.textContent;
    var lower = text.toLowerCase();
    var idx = lower.indexOf(query);
    if (idx === -1) return;
    var before = text.substring(0, idx);
    var matched = text.substring(idx, idx + query.length);
    var after = text.substring(idx + query.length);
    el.innerHTML = escapeHtml(before) + '<mark>' + escapeHtml(matched) + '</mark>' + escapeHtml(after);
  }

  function handleSidebarSearch(query) {
    query = (query || '').trim().toLowerCase();

    // Clear state
    if ($sidebarSearchClear) {
      $sidebarSearchClear.style.display = query ? '' : 'none';
    }

    if (!query) {
      // Reset: show all folders and sessions
      if ($sidebarSearchResults) $sidebarSearchResults.style.display = 'none';
      if ($sidebarSearchResults) $sidebarSearchResults.innerHTML = '';
      var allFolders = document.querySelectorAll('.folder-item');
      allFolders.forEach(function(f) { f.style.display = ''; });
      var allSessions = document.querySelectorAll('.session-item');
      allSessions.forEach(function(s) {
        s.style.display = '';
        // Remove highlight marks
        s.querySelectorAll('mark').forEach(function(m) { m.replaceWith(m.textContent); });
      });
      var allTitles = document.querySelectorAll('.sessions-section-title, .sidebar-folders-header');
      allTitles.forEach(function(t) { t.style.display = ''; });
      return;
    }

    // Filter folders by name
    var allFolders = document.querySelectorAll('.folder-item');
    allFolders.forEach(function(f) {
      var name = (f.querySelector('.folder-name') || {}).textContent || '';
      f.style.display = name.toLowerCase().indexOf(query) !== -1 ? '' : 'none';
    });

    // Filter sessions by title AND preview text
    var allSessions = document.querySelectorAll('.session-item');
    allSessions.forEach(function(s) {
      var titleEl = s.querySelector('.session-title') || s.querySelector('.session-name');
      var title = (titleEl || s).textContent || '';
      var previewEl = s.querySelector('.session-preview');
      var previewText = previewEl ? previewEl.textContent : '';
      var match = title.toLowerCase().indexOf(query) !== -1 || previewText.toLowerCase().indexOf(query) !== -1;
      s.style.display = match ? '' : 'none';
      if (match) {
        if (titleEl) highlightText(titleEl, query);
        if (previewEl) highlightText(previewEl, query);
      }
    });

    // Hide empty date section titles when filtering
    var sectionTitles = document.querySelectorAll('.sessions-section-title');
    sectionTitles.forEach(function(titleEl) {
      var next = titleEl.nextElementSibling;
      var hasVisible = false;
      while (next && !next.classList.contains('sessions-section-title') && !next.classList.contains('sidebar-folders-header')) {
        if (next.classList.contains('session-item') && next.style.display !== 'none') hasVisible = true;
        next = next.nextElementSibling;
      }
      titleEl.style.display = hasVisible ? '' : 'none';
    });

    // Search clients via Notion API (debounced, only if 3+ chars)
    if (query.length >= 3) {
      clearTimeout(searchDebounceTimer);
      searchDebounceTimer = setTimeout(function() {
        searchClientsNotion(query);
      }, 300);
    } else {
      if ($sidebarSearchResults) {
        $sidebarSearchResults.style.display = 'none';
        $sidebarSearchResults.innerHTML = '';
      }
    }
  }

  function searchClientsNotion(query) {
    fetch('/api/notion-clients.php?q=' + encodeURIComponent(query))
      .then(function(r) { return r.json(); })
      .then(function(data) {
        if (!$sidebarSearchResults) return;
        if (!data.clients || data.clients.length === 0) {
          $sidebarSearchResults.style.display = 'none';
          $sidebarSearchResults.innerHTML = '';
          return;
        }
        var html = '<div class="search-results-title">Clients</div>';
        data.clients.forEach(function(c) {
          html += '<div class="search-result-client" data-client-id="' + c.id + '">' +
            '<div class="search-result-avatar">' + (c.nom || '?').charAt(0).toUpperCase() + '</div>' +
            '<div class="search-result-info">' +
              '<span class="search-result-name">' + (c.nom || 'Sans nom') + '</span>' +
              (c.societe ? '<span class="search-result-company">' + c.societe + '</span>' : '') +
            '</div>' +
            (c.type ? '<span class="search-result-type">' + c.type + '</span>' : '') +
          '</div>';
        });
        $sidebarSearchResults.innerHTML = html;
        $sidebarSearchResults.style.display = '';

        // Click handler for client results
        $sidebarSearchResults.querySelectorAll('.search-result-client').forEach(function(el) {
          el.addEventListener('click', function() {
            var id = el.dataset.clientId;
            if (id && typeof openClientCard === 'function') {
              openClientCard(id);
            }
          });
        });
      })
      .catch(function(err) {
        console.warn('[search] Client search error:', err);
      });
  }

  if ($sidebarSearch) {
    $sidebarSearch.addEventListener('input', function() {
      handleSidebarSearch(this.value);
    });
  }
  if ($sidebarSearchClear) {
    $sidebarSearchClear.addEventListener('click', function() {
      if ($sidebarSearch) $sidebarSearch.value = '';
      handleSidebarSearch('');
    });
  }


  // === CLIENT CARD PANEL ===
  var $clientPanel = document.getElementById('client-panel');
  var $clientOverlay = document.getElementById('client-overlay');
  var $clientClose = document.getElementById('client-panel-close');
  var $clientLoading = document.getElementById('client-loading');
  var $clientContent = document.getElementById('client-content');
  var $clientError = document.getElementById('client-error');
  var $clientBtnNotion = document.getElementById('client-btn-notion');

  function openClientCard(notionId) {
    if (!$clientPanel) return;
    // Show loading, hide content & error
    if ($clientLoading) $clientLoading.style.display = '';
    if ($clientContent) $clientContent.style.display = 'none';
    if ($clientError) $clientError.style.display = 'none';
    // Open panel
    $clientPanel.classList.add('open');
    if ($clientOverlay) $clientOverlay.classList.add('open');
    document.body.style.overflow = 'hidden';
    // Load data
    loadClientData(notionId);
  }

  function closeClientCard() {
    if (!$clientPanel) return;
    $clientPanel.classList.remove('open');
    if ($clientOverlay) $clientOverlay.classList.remove('open');
    document.body.style.overflow = '';
  }

  function loadClientData(notionId) {
    fetch('/api/notion-clients.php?id=' + encodeURIComponent(notionId))
      .then(function(r) {
        if (!r.ok) throw new Error('HTTP ' + r.status);
        return r.json();
      })
      .then(function(data) {
        if (data.error) throw new Error(data.error);
        var c = data.client;
        // Fill in the panel
        var $name = document.getElementById('client-panel-name');
        var $type = document.getElementById('client-panel-type');
        var $avatar = document.getElementById('client-avatar');

        if ($name) $name.textContent = c.nom || 'Sans nom';
        if ($type) {
          $type.textContent = c.status || c.abonnement || '';
          $type.className = 'client-panel-type client-type-' + (c.status || 'default').toLowerCase().replace(/[^a-z]/g, '');
        }
        if ($avatar) $avatar.textContent = (c.nom || '?').charAt(0).toUpperCase();

        // Fields
        var fields = {
          'client-societe': c.societe,
          'client-email': c.email,
          'client-telephone': c.telephone,
          'client-status': c.status,
          'client-agent-assigne': c.agentAssigne,
          'client-abonnement': c.abonnement,
          'client-canal': c.canal,
          'client-notes': c.notes
        };
        Object.keys(fields).forEach(function(id) {
          var el = document.getElementById(id);
          if (el) el.textContent = fields[id] || '-';
        });

        // Notion link
        if ($clientBtnNotion && c.url) {
          $clientBtnNotion.href = c.url;
          $clientBtnNotion.style.display = '';
        } else if ($clientBtnNotion) {
          $clientBtnNotion.style.display = 'none';
        }

        // Show content
        if ($clientLoading) $clientLoading.style.display = 'none';
        if ($clientContent) $clientContent.style.display = '';
        if ($clientError) $clientError.style.display = 'none';
      })
      .catch(function(err) {
        console.error('[client-card] Error loading client:', err);
        if ($clientLoading) $clientLoading.style.display = 'none';
        if ($clientContent) $clientContent.style.display = 'none';
        if ($clientError) $clientError.style.display = '';
      });
  }

  // Client panel event listeners
  if ($clientClose) $clientClose.addEventListener('click', closeClientCard);
  if ($clientOverlay) $clientOverlay.addEventListener('click', closeClientCard);

  // === DYNAMIC LINKS — Delegated click handler on messages ===
  if ($messages) {
    $messages.addEventListener('click', function(e) {
      // Handle action:// links
      var actionLink = e.target.closest('.action-link');
      if (actionLink) {
        e.preventDefault();
        e.stopPropagation();
        var action = actionLink.dataset.action;
        var id = actionLink.dataset.id;
        handleActionLink(action, id);
        return;
      }
      // Handle nav:// links
      var navLink = e.target.closest('.nav-link');
      if (navLink) {
        e.preventDefault();
        e.stopPropagation();
        var nav = navLink.dataset.nav;
        handleNavLink(nav);
        return;
      }
    });
  }

  /**
   * Route action:// links to the right handler
   * action://client/<notionId> → open client card
   * action://task/<notionId>   → open task detail (future)
   * action://search/<query>    → trigger search
   */
  function handleActionLink(action, id) {
    switch (action) {
      case 'client':
        if (typeof openClientCard === 'function') {
          openClientCard(id);
        } else {
          console.warn('[action-link] openClientCard not yet available, id:', id);
        }
        break;
      case 'task':
        // Future: open task detail
        console.log('[action-link] task action, id:', id);
        break;
      case 'search':
        // Trigger sidebar search
        var searchInput = document.getElementById('sidebar-search');
        if (searchInput) {
          searchInput.value = decodeURIComponent(id);
          searchInput.dispatchEvent(new Event('input'));
          // Open sidebar if closed on mobile
          var sidebar = document.getElementById('sidebar');
          if (sidebar && !sidebar.classList.contains('open')) {
            sidebar.classList.add('open');
          }
        }
        break;
      default:
        console.warn('[action-link] Unknown action:', action, id);
    }
  }

  /**
   * Route nav:// links to the right UI section
   * nav://folders    → scroll to folders in sidebar
   * nav://settings   → open settings panel
   * nav://profile    → open profile panel
   * nav://tools      → open tools panel
   * nav://dashboard  → show dashboard
   */
  function handleNavLink(target) {
    switch (target) {
      case 'folders':
        var foldersHeader = document.querySelector('.sidebar-folders-header');
        if (foldersHeader) {
          foldersHeader.scrollIntoView({ behavior: 'smooth', block: 'start' });
          // Open sidebar if closed on mobile
          var sidebar = document.getElementById('sidebar');
          if (sidebar && !sidebar.classList.contains('open')) {
            sidebar.classList.add('open');
          }
        }
        break;
      case 'settings':
        if (typeof openSettingsPanel === 'function') openSettingsPanel();
        break;
      case 'profile':
        if (typeof openProfilePanel === 'function') openProfilePanel();
        break;
      case 'tools':
        var toolsBtn = document.getElementById('btn-tools-toggle');
        if (toolsBtn) toolsBtn.click();
        break;
      case 'dashboard':
        var dashBtn = document.getElementById('nav-dashboard');
        if (dashBtn) dashBtn.click();
        break;
      default:
        console.warn('[nav-link] Unknown target:', target);
    }
  }

  // === Delegated event listeners (replacing inline onclick) ===
  document.addEventListener('click', function(e) {
    // Code copy button
    var copyBtn = e.target.closest('[data-action="copy-code"]');
    if (copyBtn) {
      var codeEl = copyBtn.closest('.code-wrapper').querySelector('code');
      if (codeEl) {
        navigator.clipboard.writeText(codeEl.textContent);
        copyBtn.textContent = 'Copié !';
        setTimeout(function() { copyBtn.textContent = 'Copier'; }, 1500);
      }
      return;
    }
    // Task table check button
    var taskBtn = e.target.closest('.task-table-check[data-task-title]');
    if (taskBtn && typeof window.completeTaskFromTable === 'function') {
      window.completeTaskFromTable(taskBtn);
      return;
    }
  });

  // === COMMAND PALETTE (Ctrl+K) ===
  var _cmdPaletteOpen = false;
  var _cmdPalette = null;

  var _cmdActions = [
    { id: 'new', icon: '➕', label: 'Nouvelle conversation', shortcut: 'Ctrl+Shift+N', action: function() { document.getElementById('btn-new-chat').click(); } },
    { id: 'search', icon: '🔍', label: 'Rechercher une conversation', action: function() {
      var sb = document.getElementById('sidebar');
      if (sb && !sb.classList.contains('open')) document.getElementById('btn-burger').click();
      setTimeout(function() { var si = document.getElementById('sidebar-search'); if (si) si.focus(); }, 200);
    }},
    { id: 'export', icon: '📥', label: 'Exporter la conversation (.md)', action: function() {
      var title = document.getElementById('header-name') ? document.getElementById('header-name').textContent : 'conversation';
      exportConversation(SESSION_KEY, title);
    }},
    { id: 'tools', icon: '🛠', label: 'Ouvrir/fermer le panneau outils', action: function() {
      var btn = document.getElementById('btn-tools-toggle');
      if (btn) btn.click();
    }},
    { id: 'dashboard', icon: '📊', label: 'Tableau de bord', action: function() {
      var btn = document.getElementById('nav-dashboard');
      if (btn) btn.click();
    }},
    { id: 'profile', icon: '👤', label: 'Mon profil', action: function() {
      if (typeof openProfilePanel === 'function') openProfilePanel();
    }},
    { id: 'settings', icon: '⚙', label: 'Paramètres', action: function() {
      document.getElementById('menu-settings').click();
    }},
    { id: 'theme', icon: '🌙', label: 'Changer le thème (clair/sombre)', action: function() {
      var btn = document.getElementById('theme-toggle') || document.getElementById('btn-theme');
      if (btn) btn.click();
    }},
    { id: 'logout', icon: '🚪', label: 'Déconnexion', action: function() {
      document.getElementById('menu-logout').click();
    }}
  ];

  function openCommandPalette() {
    if (_cmdPaletteOpen) { closeCommandPalette(); return; }
    _cmdPaletteOpen = true;
    var overlay = document.createElement('div');
    overlay.className = 'cmd-palette-overlay';
    overlay.addEventListener('click', closeCommandPalette);

    var panel = document.createElement('div');
    panel.className = 'cmd-palette';
    panel.innerHTML = '<input type="text" class="cmd-palette-input" placeholder="Rechercher une action..." autofocus>';
    var list = document.createElement('div');
    list.className = 'cmd-palette-list';
    panel.appendChild(list);
    overlay.appendChild(panel);
    document.body.appendChild(overlay);
    _cmdPalette = overlay;

    var input = panel.querySelector('.cmd-palette-input');
    var activeIdx = 0;

    function renderList(filter) {
      var filtered = _cmdActions.filter(function(a) {
        return !filter || a.label.toLowerCase().indexOf(filter.toLowerCase()) !== -1;
      });
      list.innerHTML = '';
      filtered.forEach(function(a, i) {
        var item = document.createElement('div');
        item.className = 'cmd-palette-item' + (i === activeIdx ? ' active' : '');
        item.innerHTML = '<span class="cmd-icon">' + a.icon + '</span><span class="cmd-label">' + a.label + '</span>' +
          (a.shortcut ? '<span class="cmd-shortcut">' + a.shortcut + '</span>' : '');
        item.addEventListener('click', function() { closeCommandPalette(); a.action(); });
        item.addEventListener('mouseenter', function() {
          activeIdx = i;
          list.querySelectorAll('.cmd-palette-item').forEach(function(el, j) {
            el.classList.toggle('active', j === i);
          });
        });
        list.appendChild(item);
      });
      return filtered;
    }

    var currentFiltered = renderList('');

    input.addEventListener('input', function() {
      activeIdx = 0;
      currentFiltered = renderList(input.value);
    });

    input.addEventListener('keydown', function(e) {
      var items = list.querySelectorAll('.cmd-palette-item');
      if (e.key === 'ArrowDown') { e.preventDefault(); activeIdx = Math.min(activeIdx + 1, items.length - 1); items.forEach(function(el, i) { el.classList.toggle('active', i === activeIdx); }); }
      else if (e.key === 'ArrowUp') { e.preventDefault(); activeIdx = Math.max(activeIdx - 1, 0); items.forEach(function(el, i) { el.classList.toggle('active', i === activeIdx); }); }
      else if (e.key === 'Enter') { e.preventDefault(); var active = list.querySelector('.cmd-palette-item.active'); if (active) active.click(); }
      else if (e.key === 'Escape') { closeCommandPalette(); }
    });

    requestAnimationFrame(function() { input.focus(); });
  }

  function closeCommandPalette() {
    if (_cmdPalette) {
      _cmdPalette.remove();
      _cmdPalette = null;
    }
    _cmdPaletteOpen = false;
  }

  document.addEventListener('keydown', function(e) {
    if ((e.ctrlKey || e.metaKey) && e.key === 'k') {
      e.preventDefault();
      openCommandPalette();
    }
  });

})();