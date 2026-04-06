/**
 * VoiceClient — Module d'integration vocale pour le webchat MyBotIA
 * Panel lateral (right sidebar style) avec connexion au voice-server.
 * Lazy-loads ONNX + VAD uniquement au premier clic.
 */
(function () {
  'use strict';

  // ── State ─────────────────────────────────────────────────────────────
  var ws = null;
  var vad = null;
  var audioContext = null;
  var audioQueue = [];
  var isPlaying = false;
  var voiceState = 'idle'; // idle, connecting, listening, recording, processing, speaking
  var mode = 'free';
  var agentConfig = null;
  var sessionKey = null;
  var transcript = [];
  var meetingTimer = null;
  var meetingStart = 0;
  var vadLoaded = false;
  var selectedMicId = localStorage.getItem('voice-app:mic-id') || '';
  var ttsRate = parseInt(localStorage.getItem('voice-app:speed') || '-5', 10);

  // ── DOM refs ──────────────────────────────────────────────────────────
  var $ = function(id) { return document.getElementById(id); };

  // ── Public API ────────────────────────────────────────────────────────
  window.VoiceClient = {
    init: init,
    open: open,
    close: close,
    isOpen: function() { return $('voice-panel') && $('voice-panel').classList.contains('open'); },
    getTranscript: function() { return transcript; },
    setMode: setMode,
    getState: function() { return voiceState; },
    updateMic: function(id) { selectedMicId = id; localStorage.setItem('voice-app:mic-id', id); },
    updateRate: function(r) { ttsRate = r; localStorage.setItem('voice-app:speed', String(r)); }
  };

  // ── Init ──────────────────────────────────────────────────────────────
  function init(config) {
    agentConfig = config.agentConfig;
    sessionKey = config.sessionKey;

    // Populate hint with wake word
    var hintName = $('voice-hint-name');
    if (hintName) hintName.textContent = '\u00ab ' + (agentConfig.wakeWord || agentConfig.name) + ' \u00bb';

    // Mode buttons
    var modeBtns = document.querySelectorAll('.voice-mode-btn');
    modeBtns.forEach(function(btn) {
      btn.addEventListener('click', function() {
        modeBtns.forEach(function(b) { b.classList.remove('active'); });
        btn.classList.add('active');
        setMode(btn.dataset.mode);
      });
    });

    // Start/stop button
    var startBtn = $('voice-start-btn');
    if (startBtn) {
      startBtn.addEventListener('click', function() {
        if (voiceState === 'idle' || voiceState === 'connecting') {
          startVoice();
        } else {
          stopVoice();
        }
      });
    }

    // Back button (close)
    var backBtn = $('voice-back-btn');
    if (backBtn) backBtn.addEventListener('click', close);

    // Meeting stop — open modal instead of ending directly
    var meetingStop = $('voice-meeting-stop');
    if (meetingStop) meetingStop.addEventListener('click', function() {
      showMeetingStopModal();
    });

    console.log('[VoiceClient] Initialized for agent:', agentConfig.name, '| sessionKey:', sessionKey);
  }

  // ── Open voice panel ─────────────────────────────────────────────────
  function open() {
    var panel = $('voice-panel');
    if (!panel) { console.error('[VoiceClient] #voice-panel not found'); return; }

    // Close right sidebar (tools) if open to avoid overlap
    var rs = document.getElementById('right-sidebar');
    if (rs && rs.classList.contains('open')) {
      rs.classList.remove('open');
      var toolsBtn = document.getElementById('btn-tools-toggle');
      if (toolsBtn) toolsBtn.classList.remove('active');
    }

    panel.classList.add('open');
    var voiceBtn = $('btn-voice');
    if (voiceBtn) voiceBtn.classList.add('active');

    transcript = [];
    clearTranscriptUI();

    // Apply saved default mode
    var savedMode = localStorage.getItem('voice-app:default-mode');
    if (savedMode && savedMode !== mode) {
      var modeBtns = document.querySelectorAll('.voice-mode-btn');
      modeBtns.forEach(function(b) {
        b.classList.toggle('active', b.dataset.mode === savedMode);
      });
      setMode(savedMode);
    }
    // Re-read settings from localStorage
    ttsRate = parseInt(localStorage.getItem('voice-app:speed') || '-5', 10);
    selectedMicId = localStorage.getItem('voice-app:mic-id') || '';

    setState('idle');
    console.log('[VoiceClient] Panel opened | mode:', mode, '| ttsRate:', ttsRate);
  }

  // ── Close voice panel ─────────────────────────────────────────────────
  function close() {
    console.log('[VoiceClient] Closing panel | transcript entries:', transcript.length);
    stopVoice();
    var panel = $('voice-panel');
    if (panel) panel.classList.remove('open');
    var voiceBtn = $('btn-voice');
    if (voiceBtn) voiceBtn.classList.remove('active');

    // If there's transcript data, show save modal
    if (transcript.length > 0) {
      showSaveModal();
    } else {
      setState('idle');
      if (typeof window._onVoiceClosed === 'function') window._onVoiceClosed(null);
    }
  }

  // ── Start voice session ───────────────────────────────────────────────
  async function startVoice() {
    setState('connecting');
    console.log('[VoiceClient] Starting voice session...');
    console.log('[VoiceClient] Config:', JSON.stringify({
      agent: agentConfig ? agentConfig.name : 'none',
      mode: mode,
      ttsRate: ttsRate,
      mic: selectedMicId || 'default',
      sessionKey: sessionKey
    }));

    try {
      // Step 1: Lazy-load VAD + ONNX
      if (!vadLoaded) {
        console.log('[VoiceClient] Loading VAD scripts...');
        await loadVADScripts();
        vadLoaded = true;
        console.log('[VoiceClient] VAD scripts loaded OK');
      }

      // Step 2: Connect WebSocket
      var protocol = location.protocol === 'https:' ? 'wss:' : 'ws:';
      var wsUrl = protocol + '//' + location.host + '/voice-ws';
      console.log('[VoiceClient] Connecting WS to:', wsUrl);

      ws = new WebSocket(wsUrl);
      ws.binaryType = 'arraybuffer';

      ws.onopen = function() {
        console.log('[VoiceClient] WS connected OK');
        var connDot = $('voice-conn-dot');
        if (connDot) connDot.classList.add('connected');

        // Send start message with agent config + session key
        var startMsg = {
          type: 'start',
          mode: mode,
          rate: ttsRate,
          sessionKey: sessionKey,
          agentConfig: agentConfig ? {
            name: agentConfig.name,
            voice: agentConfig.voice,
            voiceRate: agentConfig.voiceRate,
            voicePitch: agentConfig.voicePitch,
            wakeWord: agentConfig.wakeWord,
            systemPrompt: agentConfig.systemPrompt,
            gatewayToken: agentConfig.gatewayToken,
            userName: agentConfig.userName
          } : undefined
        };
        console.log('[VoiceClient] Sending start:', JSON.stringify({ type: 'start', mode: mode, rate: ttsRate, hasConfig: !!agentConfig }));
        ws.send(JSON.stringify(startMsg));

        // Step 3: Start VAD AFTER WS is connected (like the working POC)
        console.log('[VoiceClient] Starting VAD...');
        startVAD().then(function() {
          console.log('[VoiceClient] VAD started OK - ready for speech');
        }).catch(function(vadErr) {
          console.error('[VoiceClient] VAD start failed:', vadErr.name, vadErr.message);
          if (vadErr.name === 'NotAllowedError') {
            console.error('[VoiceClient] MICROPHONE BLOCKED - Check browser permissions and Permissions-Policy header');
          }
          setState('idle');
        });
      };

      ws.onmessage = function(event) {
        if (event.data instanceof ArrayBuffer) {
          console.log('[VoiceClient] Audio chunk received:', event.data.byteLength, 'bytes');
          handleAudioChunk(event.data);
        } else {
          try {
            var msg = JSON.parse(event.data);
            console.log('[VoiceClient] Server msg:', msg.type, msg.text ? '| ' + msg.text.substring(0, 60) : '');
            handleMessage(msg);
          } catch (e) {
            console.error('[VoiceClient] Bad JSON message:', e);
          }
        }
      };

      ws.onclose = function(e) {
        console.log('[VoiceClient] WS closed | code:', e.code, '| reason:', e.reason || 'none');
        var connDot = $('voice-conn-dot');
        if (connDot) connDot.classList.remove('connected');
        if (e.code === 1006) {
          var label = $('voice-status-label');
          if (label) label.textContent = 'Connexion impossible au serveur vocal';
        }
        if (voiceState !== 'idle') setState('idle');
      };

      ws.onerror = function(e) {
        console.error('[VoiceClient] WS error:', e);
        console.error('[VoiceClient] Check: 1) voice-server running on :3100? 2) Apache proxy /voice-ws configured?');
        var label = $('voice-status-label');
        if (label) label.textContent = 'Serveur vocal indisponible';
        setState('idle');
      };

    } catch (err) {
      console.error('[VoiceClient] startVoice() error:', err.name, err.message);
      setState('idle');
    }
  }

  // ── Stop voice session ────────────────────────────────────────────────
  function stopVoice() {
    console.log('[VoiceClient] Stopping voice session');
    if (vad) {
      try { vad.destroy(); } catch(e) { console.warn('[VoiceClient] VAD destroy error:', e); }
      vad = null;
    }
    stopAudioPlayback();
    if (ws && ws.readyState === WebSocket.OPEN) {
      ws.send(JSON.stringify({ type: 'stop' }));
      ws.close();
    }
    ws = null;
    if (meetingTimer) { clearInterval(meetingTimer); meetingTimer = null; }
    setState('idle');
  }

  // ── Set mode ──────────────────────────────────────────────────────────
  function setMode(newMode) {
    mode = newMode;
    console.log('[VoiceClient] Mode changed to:', mode);
    if (ws && ws.readyState === WebSocket.OPEN) {
      ws.send(JSON.stringify({ type: 'set_mode', mode: mode }));
    }
    var hint = $('voice-hint');
    var meetingBar = $('voice-meeting-bar');
    if (hint) hint.classList.toggle('hidden', mode !== 'on-call');
    if (meetingBar) meetingBar.classList.toggle('hidden', mode !== 'meeting');
    if (mode === 'meeting') startMeetingTimer();
  }

  // ── Handle server messages ────────────────────────────────────────────
  function handleMessage(msg) {
    switch (msg.type) {
      case 'listening':
        setState('listening');
        break;
      case 'processing':
        setState('processing');
        break;
      case 'pipeline_stage':
        updatePipeline(msg.stage);
        break;
      case 'transcript':
        addTranscript(msg.role, msg.text);
        if (msg.role === 'user') {
          transcript.push({ role: 'user', text: msg.text, timestamp: new Date().toISOString() });
        }
        break;
      case 'response_text':
        addTranscript('assistant', msg.text);
        transcript.push({ role: 'assistant', text: msg.text, timestamp: new Date().toISOString() });
        break;
      case 'audio_end':
        setState('listening');
        break;
      case 'deep_thinking':
        if (msg.active) setState('processing');
        break;
      case 'no_wake_word':
        console.log('[VoiceClient] No wake word detected');
        break;
      case 'conversation_end':
      case 'conversation_timeout':
        setState('listening');
        break;
      case 'meeting_summary':
        addTranscript('system', msg.text);
        break;
      case 'meeting_report_sent':
        addTranscript('system', 'Compte-rendu envoye par email.');
        break;
      case 'meeting_report_error':
        addTranscript('system', 'Erreur envoi email : ' + (msg.message || 'inconnue'));
        break;
      case 'voice_transcript':
        if (msg.transcript) transcript = msg.transcript;
        break;
      case 'error':
        console.error('[VoiceClient] Server error:', msg.message);
        setState('listening');
        break;
      default:
        console.log('[VoiceClient] Unknown message type:', msg.type);
    }
  }

  // ── Audio playback ────────────────────────────────────────────────────
  function handleAudioChunk(data) {
    audioQueue.push(data);
    setState('speaking');
    playNextChunk();
  }

  async function playNextChunk() {
    if (isPlaying || audioQueue.length === 0) return;
    isPlaying = true;

    if (!audioContext) audioContext = new AudioContext();
    if (audioContext.state === 'suspended') await audioContext.resume();

    while (audioQueue.length > 0) {
      var chunk = audioQueue.shift();
      try {
        var buffer = await audioContext.decodeAudioData(chunk.slice(0));
        var source = audioContext.createBufferSource();
        source.buffer = buffer;
        source.connect(audioContext.destination);
        await new Promise(function(resolve) {
          source.onended = resolve;
          source.start(0);
        });
      } catch (e) {
        console.warn('[VoiceClient] Audio decode error:', e);
      }
    }
    isPlaying = false;
  }

  function stopAudioPlayback() {
    audioQueue = [];
    isPlaying = false;
    if (audioContext && audioContext.state === 'running') {
      audioContext.close().catch(function() {});
      audioContext = null;
    }
  }

  // ── VAD (lazy loaded) ─────────────────────────────────────────────────
  async function loadVADScripts() {
    if (window.vad) return;
    await loadScript('https://cdn.jsdelivr.net/npm/onnxruntime-web@1.19.0/dist/ort.min.js');
    await loadScript('https://cdn.jsdelivr.net/npm/@ricky0123/vad-web@0.0.19/dist/bundle.min.js');
  }

  function loadScript(src) {
    return new Promise(function(resolve, reject) {
      if (document.querySelector('script[src="' + src + '"]')) { resolve(); return; }
      var s = document.createElement('script');
      s.src = src;
      s.onload = resolve;
      s.onerror = function() { reject(new Error('Failed to load: ' + src)); };
      document.head.appendChild(s);
    });
  }

  async function startVAD() {
    var constraints = { audio: selectedMicId ? { deviceId: { exact: selectedMicId } } : true };
    console.log('[VoiceClient] Requesting mic access:', JSON.stringify(constraints));

    var stream = await navigator.mediaDevices.getUserMedia(constraints);
    console.log('[VoiceClient] Mic access granted, tracks:', stream.getAudioTracks().length);

    vad = await window.vad.MicVAD.new({
      stream: stream,
      positiveSpeechThreshold: 0.8,
      negativeSpeechThreshold: 0.4,
      minSpeechFrames: 5,
      preSpeechPadFrames: 10,
      redemptionFrames: 15,
      onSpeechStart: function() {
        console.log('[VoiceClient] Speech detected');
        if (isPlaying) {
          // Barge-in: stop playback
          stopAudioPlayback();
          audioContext = new AudioContext();
          if (ws && ws.readyState === WebSocket.OPEN) {
            ws.send(JSON.stringify({ type: 'barge_in' }));
          }
        }
        setState('recording');
      },
      onSpeechEnd: function(audio) {
        console.log('[VoiceClient] Speech ended, samples:', audio.length, '| sending WAV to server');
        var wav = float32ToWav(audio, 16000);
        if (ws && ws.readyState === WebSocket.OPEN) {
          ws.send(wav);
        } else {
          console.warn('[VoiceClient] WS not open, cannot send audio');
        }
        setState('processing');
      }
    });

    await vad.start();
    setState('listening');
    console.log('[VoiceClient] VAD active, listening for speech');
  }

  // ── WAV encoder ───────────────────────────────────────────────────────
  function float32ToWav(float32, sampleRate) {
    var numSamples = float32.length;
    var buffer = new ArrayBuffer(44 + numSamples * 2);
    var view = new DataView(buffer);
    var writeStr = function(offset, str) { for (var i = 0; i < str.length; i++) view.setUint8(offset + i, str.charCodeAt(i)); };
    writeStr(0, 'RIFF');
    view.setUint32(4, 36 + numSamples * 2, true);
    writeStr(8, 'WAVE');
    writeStr(12, 'fmt ');
    view.setUint32(16, 16, true);
    view.setUint16(20, 1, true);
    view.setUint16(22, 1, true);
    view.setUint32(24, sampleRate, true);
    view.setUint32(28, sampleRate * 2, true);
    view.setUint16(32, 2, true);
    view.setUint16(34, 16, true);
    writeStr(36, 'data');
    view.setUint32(40, numSamples * 2, true);
    for (var i = 0; i < numSamples; i++) {
      var s = Math.max(-1, Math.min(1, float32[i]));
      view.setInt16(44 + i * 2, s < 0 ? s * 0x8000 : s * 0x7FFF, true);
    }
    return buffer;
  }

  // ── State management ──────────────────────────────────────────────────
  function setState(newState) {
    voiceState = newState;
    var orb = $('voice-orb');
    var micIcon = $('voice-mic-icon');
    var spinner = $('voice-spinner');
    var label = $('voice-status-label');
    var startBtn = $('voice-start-btn');

    if (orb) orb.className = 'voice-orb voice-state-' + newState;

    switch (newState) {
      case 'idle':
        if (label) label.textContent = 'Cliquez pour demarrer';
        if (startBtn) startBtn.textContent = 'Demarrer';
        if (micIcon) micIcon.classList.remove('hidden');
        if (spinner) spinner.classList.add('hidden');
        break;
      case 'connecting':
        if (label) label.textContent = 'Connexion...';
        if (startBtn) startBtn.textContent = 'Connexion...';
        if (spinner) spinner.classList.remove('hidden');
        if (micIcon) micIcon.classList.add('hidden');
        break;
      case 'listening':
        if (label) label.textContent = mode === 'on-call' ? 'En attente du mot-cle...' : 'A l\'ecoute...';
        if (startBtn) startBtn.textContent = 'Arreter';
        if (micIcon) micIcon.classList.remove('hidden');
        if (spinner) spinner.classList.add('hidden');
        break;
      case 'recording':
        if (label) label.textContent = 'Parlez...';
        break;
      case 'processing':
        if (label) label.textContent = 'Traitement...';
        if (micIcon) micIcon.classList.add('hidden');
        if (spinner) spinner.classList.remove('hidden');
        break;
      case 'speaking':
        if (label) label.textContent = (agentConfig ? agentConfig.name : 'Agent') + ' repond...';
        if (micIcon) micIcon.classList.remove('hidden');
        if (spinner) spinner.classList.add('hidden');
        break;
    }

    document.dispatchEvent(new CustomEvent('voice:stateChange', { detail: { state: newState } }));
  }

  // ── Pipeline label ────────────────────────────────────────────────────
  var PIPELINE_LABELS = { stt: 'Transcription', thinking: 'Reflexion', tts: 'Synthese vocale', speaking: 'Reponse' };
  function updatePipeline(stage) {
    var el = $('voice-pipeline-label');
    if (el) el.textContent = PIPELINE_LABELS[stage] || '';
    if (stage === 'speaking') setState('speaking');
    else if (stage === 'thinking' || stage === 'stt' || stage === 'tts') setState('processing');
  }

  // ── Transcript UI ─────────────────────────────────────────────────────
  function addTranscript(role, text) {
    // Mobile preview: show in panel transcript area
    var area = $('voice-transcript');
    if (area) {
      var div = document.createElement('div');
      div.className = 'voice-transcript-item voice-role-' + role;
      var label = role === 'user' ? 'Vous' : role === 'system' ? 'Systeme' : (agentConfig ? agentConfig.name : 'Agent');
      div.innerHTML = '<span class="voice-transcript-role">' + label + '</span> ' + text;
      area.appendChild(div);
      area.scrollTop = area.scrollHeight;
    }

    // Real-time injection into main chat
    if (role !== 'system' && typeof window._onVoiceTranscriptEntry === 'function') {
      window._onVoiceTranscriptEntry({ role: role, text: text });
    }
  }

  function clearTranscriptUI() {
    var area = $('voice-transcript');
    if (area) area.innerHTML = '';
  }

  // ── Meeting timer ─────────────────────────────────────────────────────
  function startMeetingTimer() {
    meetingStart = Date.now();
    if (meetingTimer) clearInterval(meetingTimer);
    meetingTimer = setInterval(function() {
      var elapsed = Math.floor((Date.now() - meetingStart) / 1000);
      var m = String(Math.floor(elapsed / 60)).padStart(2, '0');
      var s = String(elapsed % 60).padStart(2, '0');
      var timerEl = $('voice-meeting-timer');
      if (timerEl) timerEl.textContent = m + ':' + s;
    }, 1000);
  }

  // ── Meeting stop modal ─────────────────────────────────────────────────
  function showMeetingStopModal() {
    var modal = $('voice-meeting-modal');
    if (!modal) return;

    var meta = $('voice-meeting-modal-meta');
    var timerEl = $('voice-meeting-timer');
    if (meta && timerEl) meta.textContent = 'Duree : ' + timerEl.textContent + ' \u00b7 ' + transcript.length + ' segment(s)';

    modal.classList.remove('hidden');

    var pauseBtn = $('voice-meeting-pause');
    var endEmailBtn = $('voice-meeting-end-email');
    var endNoEmailBtn = $('voice-meeting-end-no-email');

    var cleanup = function() {
      modal.classList.add('hidden');
      if (pauseBtn) pauseBtn.removeEventListener('click', onPause);
      if (endEmailBtn) endEmailBtn.removeEventListener('click', onEndEmail);
      if (endNoEmailBtn) endNoEmailBtn.removeEventListener('click', onEndNoEmail);
    };

    var onPause = function() {
      cleanup();
      if (ws && ws.readyState === WebSocket.OPEN) {
        ws.send(JSON.stringify({ type: 'meeting_pause' }));
      }
      var stopBtn = $('voice-meeting-stop');
      if (stopBtn) stopBtn.innerHTML = '<i class="ph-thin ph-play-circle"></i> Reprendre';
      // Switch stop button to resume
      if (stopBtn) {
        stopBtn.onclick = function() {
          if (ws && ws.readyState === WebSocket.OPEN) {
            ws.send(JSON.stringify({ type: 'meeting_resume' }));
          }
          stopBtn.innerHTML = '<i class="ph-thin ph-stop-circle"></i> Arreter';
          stopBtn.onclick = function() { showMeetingStopModal(); };
        };
      }
    };

    var onEndEmail = function() {
      cleanup();
      var reportEmail = localStorage.getItem('voice-app:report-email') || '';
      if (!reportEmail) {
        reportEmail = prompt('Adresse email pour le compte-rendu :');
        if (reportEmail) localStorage.setItem('voice-app:report-email', reportEmail);
      }
      if (ws && ws.readyState === WebSocket.OPEN) {
        ws.send(JSON.stringify({ type: 'end_meeting', reportEmail: reportEmail || '' }));
      }
    };

    var onEndNoEmail = function() {
      cleanup();
      if (ws && ws.readyState === WebSocket.OPEN) {
        ws.send(JSON.stringify({ type: 'end_meeting' }));
      }
    };

    if (pauseBtn) pauseBtn.addEventListener('click', onPause);
    if (endEmailBtn) endEmailBtn.addEventListener('click', onEndEmail);
    if (endNoEmailBtn) endNoEmailBtn.addEventListener('click', onEndNoEmail);
  }

  // ── Save modal ────────────────────────────────────────────────────────
  function showSaveModal() {
    var modal = $('voice-save-modal');
    var meta = $('voice-save-meta');
    if (!modal) return;

    var duration = transcript.length > 1
      ? Math.round((new Date(transcript[transcript.length - 1].timestamp) - new Date(transcript[0].timestamp)) / 60000)
      : 0;
    if (meta) meta.textContent = (duration || '< 1') + ' min \u00b7 ' + transcript.length + ' echanges';

    modal.classList.remove('hidden');

    var fullBtn = $('voice-save-full');
    var summaryBtn = $('voice-save-summary');
    var discardBtn = $('voice-save-discard');

    var cleanup = function() {
      modal.classList.add('hidden');
      if (fullBtn) fullBtn.removeEventListener('click', onKeep);
      if (summaryBtn) summaryBtn.removeEventListener('click', onSummary);
      if (discardBtn) discardBtn.removeEventListener('click', onDiscard);
    };

    var onKeep = function() { cleanup(); if (typeof window._onVoiceClosed === 'function') window._onVoiceClosed({ action: 'keep', transcript: transcript }); };
    var onSummary = function() { cleanup(); if (typeof window._onVoiceClosed === 'function') window._onVoiceClosed({ action: 'summary', transcript: transcript }); };
    var onDiscard = function() { cleanup(); if (typeof window._onVoiceClosed === 'function') window._onVoiceClosed(null); };

    if (fullBtn) fullBtn.addEventListener('click', onKeep);
    if (summaryBtn) summaryBtn.addEventListener('click', onSummary);
    if (discardBtn) discardBtn.addEventListener('click', onDiscard);
  }

})();
