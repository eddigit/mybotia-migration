/* ── Voice V2 — Léa — Conversation continue ─────────────────────────────── */

const WS_URL = `wss://${location.host}/ws`;

// ── DOM ────────────────────────────────────────────────────────────────────
const micBtn       = document.getElementById('micBtn');
const micBtnText   = document.getElementById('micBtnText');
const avatarRing   = document.getElementById('avatarRing');
const micIcon      = document.getElementById('micIcon');
const stopIcon     = document.getElementById('stopIcon');
const spinner      = document.getElementById('spinner');
const statusLabel  = document.getElementById('statusLabel');
const statusDots   = document.getElementById('statusDots');
const transcriptArea = document.getElementById('transcriptArea');
const connDot      = document.getElementById('connDot');
const settingsBtn  = document.getElementById('settingsBtn');
const settingsOverlay = document.getElementById('settingsOverlay');
const settingsClose = document.getElementById('settingsClose');
const deviceBtns   = document.querySelectorAll('.device-btn');
const micSelect    = document.getElementById('micSelect');
const spkSelect    = document.getElementById('spkSelect');
const micTestBtn   = document.getElementById('micTestBtn');
const micLevel     = document.getElementById('micLevel');
const micLevelBar  = document.getElementById('micLevelBar');
const permStatus   = document.getElementById('permStatus');
const wakeWordHint = document.getElementById('wakeWordHint');
const voiceSpeed   = document.getElementById('voiceSpeed');
const speedValue   = document.getElementById('speedValue');
const meetingBar   = document.getElementById('meetingBar');
const meetingTimer = document.getElementById('meetingTimer');
const meetingCount = document.getElementById('meetingCount');
const meetingEndBtn  = document.getElementById('meetingEndBtn');
const meetingRecDot  = document.getElementById('meetingRecDot');
const meetingEmail   = document.getElementById('meetingEmail');
const meetingModal   = document.getElementById('meetingModal');
const meetingPauseBtn  = document.getElementById('meetingPauseBtn');
const meetingFinishBtn = document.getElementById('meetingFinishBtn');
const meetingCancelBtn = document.getElementById('meetingCancelBtn');
const modeBtns     = document.querySelectorAll('.mode-btn');

// ── State ──────────────────────────────────────────────────────────────────
let ws = null;
let myVad = null;
let isConnected = false;
let isConversationActive = false;
let audioContext = null;
let audioQueue = [];
let isPlayingAudio = false;
let currentSource = null;
let audioEndReceived = false;
let selectedMicId = localStorage.getItem('voice-mic-id') || '';
let selectedSpkId = localStorage.getItem('voice-spk-id') || '';
let micTestStream = null;
let micTestAnalyser = null;
let micTestRaf = null;
let permPollInterval = null;
let currentMode = localStorage.getItem('voice-mode') || 'on-call';
let meetingPaused = false;
let meetingStartTime = null;
let meetingTimerInterval = null;
let meetingSegments = 0;

// ── Deep Track ambient sound ──────────────────────────────────────────────
let thinkingAudio = null;
let thinkingAudioLoaded = false;

// Pre-load thinking ambient sound
(function preloadThinkingAudio() {
  thinkingAudio = new Audio('/thinking-ambient.mp3');
  thinkingAudio.loop = true;
  thinkingAudio.volume = 0.15;
  thinkingAudio.preload = 'auto';
  thinkingAudio.addEventListener('canplaythrough', () => { thinkingAudioLoaded = true; });
})();

function startThinkingSound() {
  if (thinkingAudio && thinkingAudioLoaded) {
    thinkingAudio.currentTime = 0;
    thinkingAudio.play().catch(() => {});
  }
}

function stopThinkingSound() {
  if (thinkingAudio) {
    // Fade out over 500ms
    const fadeOut = setInterval(() => {
      if (thinkingAudio.volume > 0.02) {
        thinkingAudio.volume = Math.max(0, thinkingAudio.volume - 0.02);
      } else {
        clearInterval(fadeOut);
        thinkingAudio.pause();
        thinkingAudio.volume = 0.15;
        thinkingAudio.currentTime = 0;
      }
    }, 50);
  }
}

// ── Mode selector ─────────────────────────────────────────────────────────
function setMode(mode) {
  currentMode = mode;
  localStorage.setItem('voice-mode', mode);
  modeBtns.forEach(btn => btn.classList.toggle('active', btn.dataset.mode === mode));

  // Show/hide wake word hint
  if (wakeWordHint) {
    wakeWordHint.classList.toggle('hidden', mode !== 'on-call');
  }

  // Show/hide meeting bar
  if (meetingBar) {
    meetingBar.classList.toggle('hidden', mode !== 'meeting');
  }

  // If connected, notify server of mode change
  if (ws && ws.readyState === WebSocket.OPEN) {
    ws.send(JSON.stringify({ type: 'set_mode', mode }));
  }

  // If switching away from meeting, stop meeting timer
  if (mode !== 'meeting') {
    stopMeetingTimer();
  }
}

modeBtns.forEach(btn => {
  btn.addEventListener('click', () => setMode(btn.dataset.mode));
});

// Init mode from localStorage
setMode(currentMode);

// ── Voice speed slider ────────────────────────────────────────────────────
function updateSpeedLabel() {
  const val = parseInt(voiceSpeed.value, 10);
  const display = (1 + val / 100).toFixed(2) + 'x';
  speedValue.textContent = display;
}

voiceSpeed.addEventListener('input', () => {
  updateSpeedLabel();
});

voiceSpeed.addEventListener('change', () => {
  updateSpeedLabel();
  localStorage.setItem('voice-speed', voiceSpeed.value);
  // Notify server
  if (ws && ws.readyState === WebSocket.OPEN) {
    ws.send(JSON.stringify({ type: 'set_speed', rate: parseInt(voiceSpeed.value, 10) }));
  }
});

// Restore saved speed
const savedSpeed = localStorage.getItem('voice-speed');
if (savedSpeed !== null) {
  voiceSpeed.value = savedSpeed;
}
updateSpeedLabel();

// ── Meeting email ─────────────────────────────────────────────────────────
const savedMeetingEmail = localStorage.getItem('voice-meeting-email') || '';
if (meetingEmail) {
  meetingEmail.value = savedMeetingEmail;
  meetingEmail.addEventListener('change', () => {
    localStorage.setItem('voice-meeting-email', meetingEmail.value.trim());
  });
}

// ── Meeting timer ─────────────────────────────────────────────────────────
function startMeetingTimer() {
  meetingStartTime = Date.now();
  meetingSegments = 0;
  updateMeetingCount();
  meetingTimerInterval = setInterval(() => {
    const elapsed = Math.floor((Date.now() - meetingStartTime) / 1000);
    const mm = String(Math.floor(elapsed / 60)).padStart(2, '0');
    const ss = String(elapsed % 60).padStart(2, '0');
    meetingTimer.textContent = `${mm}:${ss}`;
  }, 1000);
}

function stopMeetingTimer() {
  if (meetingTimerInterval) {
    clearInterval(meetingTimerInterval);
    meetingTimerInterval = null;
  }
  meetingStartTime = null;
  meetingSegments = 0;
  meetingTimer.textContent = '00:00';
  updateMeetingCount();
  // Reset pause state
  meetingPaused = false;
  meetingBar.classList.remove('paused');
  meetingEndBtn.innerHTML = '<i class="ph-thin ph-stop-circle"></i> Arrêter';
}

function updateMeetingCount() {
  meetingCount.textContent = `${meetingSegments} segment(s)`;
}

// Meeting end → show modal with pause/finish choices
meetingEndBtn.addEventListener('click', () => {
  if (meetingPaused) {
    // Already paused → resume
    resumeMeeting();
  } else {
    // Show choice modal
    meetingModal.classList.remove('hidden');
  }
});

meetingPauseBtn.addEventListener('click', () => {
  meetingModal.classList.add('hidden');
  pauseMeeting();
});

meetingFinishBtn.addEventListener('click', () => {
  meetingModal.classList.add('hidden');
  finishMeeting();
});

meetingCancelBtn.addEventListener('click', () => {
  meetingModal.classList.add('hidden');
});

// Close modal on backdrop click
meetingModal.addEventListener('click', (e) => {
  if (e.target === meetingModal) meetingModal.classList.add('hidden');
});

function pauseMeeting() {
  meetingPaused = true;
  meetingBar.classList.add('paused');
  meetingEndBtn.innerHTML = '<i class="ph-thin ph-play-circle"></i> Reprendre';
  // Notify server
  if (ws && ws.readyState === WebSocket.OPEN) {
    ws.send(JSON.stringify({ type: 'meeting_pause' }));
  }
}

function resumeMeeting() {
  meetingPaused = false;
  meetingBar.classList.remove('paused');
  meetingEndBtn.innerHTML = '<i class="ph-thin ph-stop-circle"></i> Arrêter';
  // Notify server
  if (ws && ws.readyState === WebSocket.OPEN) {
    ws.send(JSON.stringify({ type: 'meeting_resume' }));
  }
}

function finishMeeting() {
  meetingPaused = false;
  meetingBar.classList.remove('paused');
  meetingEndBtn.innerHTML = '<i class="ph-thin ph-stop-circle"></i> Arrêter';
  if (ws && ws.readyState === WebSocket.OPEN) {
    const email = localStorage.getItem('voice-meeting-email') || '';
    ws.send(JSON.stringify({ type: 'end_meeting', reportEmail: email || null }));
  }
  stopMeetingTimer();
}

// ── Settings overlay ──────────────────────────────────────────────────────
function openSettings() {
  settingsOverlay.classList.add('open');
  refreshDeviceList();
  checkPermission();
}

function closeSettings() {
  settingsOverlay.classList.remove('open');
  stopMicTest();
}

settingsBtn.addEventListener('click', openSettings);
settingsClose.addEventListener('click', closeSettings);

// Close on overlay backdrop click
settingsOverlay.addEventListener('click', (e) => {
  if (e.target === settingsOverlay) closeSettings();
});

// Close on Escape key
document.addEventListener('keydown', (e) => {
  if (e.key === 'Escape' && settingsOverlay.classList.contains('open')) closeSettings();
});

// ── Device mode (mobile / tablet) ────────────────────────────────────────
let currentDevice = localStorage.getItem('voice-device') || 'mobile';

function setDeviceMode(mode) {
  currentDevice = mode;
  localStorage.setItem('voice-device', mode);
  document.body.classList.toggle('tablet-mode', mode === 'tablet');
  deviceBtns.forEach(btn => btn.classList.toggle('active', btn.dataset.device === mode));
}

deviceBtns.forEach(btn => {
  btn.addEventListener('click', () => setDeviceMode(btn.dataset.device));
});

setDeviceMode(currentDevice);

micSelect.addEventListener('change', () => {
  selectedMicId = micSelect.value;
  localStorage.setItem('voice-mic-id', selectedMicId);
  stopMicTest();
});

spkSelect.addEventListener('change', () => {
  selectedSpkId = spkSelect.value;
  localStorage.setItem('voice-spk-id', selectedSpkId);
});

// [Correction 3] Mic test / permission request button handler
micTestBtn.addEventListener('click', async () => {
  // If button is in "request permission" mode, try to get permission
  if (micTestBtn.classList.contains('request-perm')) {
    try {
      const stream = await navigator.mediaDevices.getUserMedia({ audio: true });
      stream.getTracks().forEach(t => t.stop());
      updatePermStatus('granted');
      await refreshDeviceList();
      showToast('Micro autorisé ✓');
    } catch (err) {
      if (err.name === 'NotAllowedError') {
        // The page may have a stale permission cache — offer reload
        permStatus.innerHTML = '⚠️ Si vous avez déjà autorisé le micro dans les paramètres du navigateur, <a href="#" id="reloadLink" style="color:#f0a500;text-decoration:underline;cursor:pointer;">rechargez la page</a> pour appliquer le changement.';
        permStatus.className = 'perm-status denied';
        const reloadLink = document.getElementById('reloadLink');
        if (reloadLink) {
          reloadLink.addEventListener('click', (e) => {
            e.preventDefault();
            location.reload();
          });
        }
        startPermissionPolling();
        showToast('Permission bloquée — rechargez si vous avez changé les paramètres');
      } else {
        showToast('Erreur micro : ' + err.message);
      }
    }
    return;
  }
  // Normal test/stop toggle
  if (micTestStream) {
    stopMicTest();
  } else {
    startMicTest();
  }
});

async function checkPermission() {
  try {
    const result = await navigator.permissions.query({ name: 'microphone' });
    updatePermStatus(result.state);
    result.onchange = () => {
      console.log('[Permission] Changed to:', result.state);
      if (result.state === 'granted') {
        stopPermissionPolling();
        location.reload();
      }
      updatePermStatus(result.state);
    };
  } catch {
    // permissions API not supported (Firefox) — try getUserMedia
    updatePermStatus('unknown');
  }
}

function updatePermStatus(state) {
  if (state === 'granted') {
    permStatus.textContent = 'Micro autorisé';
    permStatus.className = 'perm-status granted';
    micTestBtn.textContent = 'Tester le micro';
    micTestBtn.classList.remove('request-perm');
    stopPermissionPolling();
  } else if (state === 'denied') {
    permStatus.innerHTML = 'Micro bloqué — <strong>Étape 1:</strong> Cliquez sur le cadenas 🔒 → Microphone → Autoriser. <strong>Étape 2:</strong> Cliquez "Autoriser le micro" ci-dessous.';
    permStatus.className = 'perm-status denied';
    micTestBtn.textContent = 'Autoriser le micro';
    micTestBtn.classList.add('request-perm');
    startPermissionPolling();
  } else {
    permStatus.textContent = 'Cliquez "Tester" pour autoriser le micro';
    permStatus.className = 'perm-status pending';
    micTestBtn.textContent = 'Tester le micro';
    micTestBtn.classList.remove('request-perm');
    stopPermissionPolling();
  }
}

// ── Permission polling (fallback when onchange is unreliable) ─────────────
function startPermissionPolling() {
  if (permPollInterval) return;
  permPollInterval = setInterval(async () => {
    try {
      const stream = await navigator.mediaDevices.getUserMedia({ audio: true });
      stream.getTracks().forEach(t => t.stop());
      clearInterval(permPollInterval);
      permPollInterval = null;
      console.log('[Permission] Micro now available via polling — refreshing');
      updatePermStatus('granted');
      await refreshDeviceList();
      showToast('Micro autorisé ✓');
    } catch {
      // Still blocked — keep polling
    }
  }, 3000);
}

function stopPermissionPolling() {
  if (permPollInterval) {
    clearInterval(permPollInterval);
    permPollInterval = null;
  }
}

// [Correction 1] Populate <select> from a device list (with or without labels)
function populateDeviceSelects(devices) {
  const mics = devices.filter(d => d.kind === 'audioinput');
  const spks = devices.filter(d => d.kind === 'audiooutput');

  // Populate mic select
  micSelect.innerHTML = '';
  if (mics.length === 0) {
    const opt = document.createElement('option');
    opt.textContent = 'Aucun micro disponible';
    micSelect.appendChild(opt);
  } else {
    mics.forEach((d, i) => {
      const opt = document.createElement('option');
      opt.value = d.deviceId;
      opt.textContent = d.label || `Micro ${i + 1}`;
      if (d.deviceId === selectedMicId) opt.selected = true;
      micSelect.appendChild(opt);
    });
    if (!selectedMicId && mics.length) selectedMicId = mics[0].deviceId;
  }

  // Populate speaker select
  spkSelect.innerHTML = '';
  if (spks.length === 0) {
    const opt = document.createElement('option');
    opt.textContent = 'Défaut (non supporté)';
    spkSelect.appendChild(opt);
    spkSelect.disabled = true;
  } else {
    spkSelect.disabled = false;
    spks.forEach((d, i) => {
      const opt = document.createElement('option');
      opt.value = d.deviceId;
      opt.textContent = d.label || `Sortie ${i + 1}`;
      if (d.deviceId === selectedSpkId) opt.selected = true;
      spkSelect.appendChild(opt);
    });
    if (!selectedSpkId && spks.length) selectedSpkId = spks[0].deviceId;
  }
}

// [Correction 1] Fallback: enumerate devices without getUserMedia (labels may be empty)
async function fallbackEnumerateDevices() {
  try {
    const devices = await navigator.mediaDevices.enumerateDevices();
    populateDeviceSelects(devices);
  } catch (enumErr) {
    console.warn('[Settings] enumerateDevices fallback failed:', enumErr);
    // Last resort: show "unavailable" in both selects
    micSelect.innerHTML = '<option>Aucun périphérique disponible</option>';
    spkSelect.innerHTML = '<option>Aucun périphérique disponible</option>';
  }
}

async function refreshDeviceList() {
  try {
    // Request permission first to get device labels
    const tempStream = await navigator.mediaDevices.getUserMedia({ audio: true });
    tempStream.getTracks().forEach(t => t.stop());

    const devices = await navigator.mediaDevices.enumerateDevices();
    populateDeviceSelects(devices);

    updatePermStatus('granted');
  } catch (err) {
    console.error('[Settings] Device list error:', err);
    if (err.name === 'NotAllowedError') {
      updatePermStatus('denied');
    } else {
      updatePermStatus('unknown');
    }
    // [Correction 1] Fallback: try enumerateDevices without permission
    await fallbackEnumerateDevices();
  }
}

async function startMicTest() {
  stopMicTest();
  try {
    const constraints = { audio: selectedMicId ? { deviceId: { exact: selectedMicId } } : true };
    micTestStream = await navigator.mediaDevices.getUserMedia(constraints);

    const ctx = new (window.AudioContext || window.webkitAudioContext)();
    const source = ctx.createMediaStreamSource(micTestStream);
    micTestAnalyser = ctx.createAnalyser();
    micTestAnalyser.fftSize = 256;
    source.connect(micTestAnalyser);

    micLevel.classList.remove('hidden');
    micTestBtn.textContent = 'Arrêter le test';
    updatePermStatus('granted');

    const dataArray = new Uint8Array(micTestAnalyser.frequencyBinCount);
    function draw() {
      micTestRaf = requestAnimationFrame(draw);
      micTestAnalyser.getByteFrequencyData(dataArray);
      const avg = dataArray.reduce((a, b) => a + b, 0) / dataArray.length;
      const pct = Math.min(100, (avg / 128) * 100);
      micLevelBar.style.width = pct + '%';
    }
    draw();
  } catch (err) {
    console.error('[MicTest]', err);
    if (err.name === 'NotAllowedError') {
      updatePermStatus('denied');
      showToast('Micro bloqué — autorisez dans les paramètres du navigateur');
    } else {
      showToast('Erreur micro : ' + err.message);
    }
  }
}

function stopMicTest() {
  if (micTestRaf) { cancelAnimationFrame(micTestRaf); micTestRaf = null; }
  if (micTestStream) { micTestStream.getTracks().forEach(t => t.stop()); micTestStream = null; }
  micTestAnalyser = null;
  micLevel.classList.add('hidden');
  micTestBtn.textContent = 'Tester le micro';
}

// ── State machine ──────────────────────────────────────────────────────────
function setState(state) {
  avatarRing.className = 'avatar-ring';
  micIcon.classList.add('hidden');
  stopIcon.classList.add('hidden');
  spinner.classList.add('hidden');
  statusDots.classList.add('hidden');
  // Stop thinking sound on any state change (will restart if needed)
  if (state !== 'processing' && state !== 'thinking_deep') stopThinkingSound();
  if (wakeWordHint) {
    wakeWordHint.classList.add('hidden');
    wakeWordHint.classList.remove('active');
  }

  switch (state) {
    case 'idle':
      micIcon.classList.remove('hidden');
      micBtn.disabled = false;
      micBtn.className = 'mic-btn';
      micBtnText.textContent = 'Démarrer';
      statusLabel.textContent = 'Cliquez pour démarrer la conversation';
      break;
    case 'connecting':
      spinner.classList.remove('hidden');
      micBtn.disabled = true;
      micBtn.className = 'mic-btn processing';
      micBtnText.textContent = 'Connexion...';
      statusLabel.textContent = 'Connexion en cours';
      statusDots.classList.remove('hidden');
      break;
    case 'listening':
      avatarRing.classList.add('recording');
      micIcon.classList.remove('hidden');
      micBtn.disabled = false;
      micBtn.className = 'mic-btn recording';
      micBtnText.textContent = 'Raccrocher';
      statusLabel.textContent = currentMode === 'meeting' ? 'Réunion en cours...' : 'En écoute...';
      if (wakeWordHint && currentMode === 'on-call') {
        wakeWordHint.classList.remove('hidden');
        wakeWordHint.classList.add('active');
      }
      break;
    case 'recording':
      avatarRing.classList.add('recording');
      stopIcon.classList.remove('hidden');
      micBtn.disabled = false;
      micBtn.className = 'mic-btn recording';
      micBtnText.textContent = 'Raccrocher';
      statusLabel.textContent = 'Vous parlez...';
      break;
    case 'processing':
      avatarRing.classList.add('processing');
      spinner.classList.remove('hidden');
      micBtn.disabled = false;
      micBtn.className = 'mic-btn recording';
      micBtnText.textContent = 'Raccrocher';
      statusLabel.textContent = 'Réflexion';
      statusDots.classList.remove('hidden');
      startThinkingSound();
      break;
    case 'thinking_deep':
      avatarRing.classList.add('thinking-deep');
      spinner.classList.remove('hidden');
      micBtn.disabled = false;
      micBtn.className = 'mic-btn recording';
      micBtnText.textContent = 'Raccrocher';
      statusLabel.textContent = 'Léa recherche...';
      statusDots.classList.remove('hidden');
      startThinkingSound();
      break;
    case 'speaking':
      avatarRing.classList.add('speaking');
      micIcon.classList.remove('hidden');
      micBtn.disabled = false;
      micBtn.className = 'mic-btn recording';
      micBtnText.textContent = 'Raccrocher';
      statusLabel.textContent = 'Léa répond...';
      stopThinkingSound();
      break;
  }
}

// ── WebSocket ──────────────────────────────────────────────────────────────
function connect() {
  // Close settings if open
  closeSettings();

  setState('connecting');
  ws = new WebSocket(WS_URL);
  ws.binaryType = 'arraybuffer';

  ws.onopen = () => {
    isConnected = true;
    if (connDot) connDot.classList.add('connected');
    ws.send(JSON.stringify({
      type: 'start',
      mode: currentMode,
      rate: parseInt(voiceSpeed.value, 10)
    }));
    if (currentMode === 'meeting') startMeetingTimer();
    startVAD();
  };

  ws.onmessage = (event) => {
    if (event.data instanceof ArrayBuffer) {
      handleAudioChunk(event.data);
    } else {
      try {
        const msg = JSON.parse(event.data);
        handleServerMessage(msg);
      } catch (e) {}
    }
  };

  ws.onclose = () => {
    isConnected = false;
    isConversationActive = false;
    if (connDot) connDot.classList.remove('connected');
    stopVAD();
    stopAudioPlayback();
    setState('idle');
  };

  ws.onerror = () => {
    showToast('Erreur de connexion');
  };
}

function disconnect() {
  isConversationActive = false;
  stopVAD();
  stopAudioPlayback();
  stopThinkingSound();
  if (ws && ws.readyState === WebSocket.OPEN) {
    ws.send(JSON.stringify({ type: 'stop' }));
    ws.close();
  }
  ws = null;
  setState('idle');
}

// ── VAD (Silero via @ricky0123/vad-web) ───────────────────────────────────
async function startVAD() {
  if (myVad) return;

  try {
    // First request mic permission with selected device
    const constraints = { audio: selectedMicId ? { deviceId: { exact: selectedMicId } } : true };
    const stream = await navigator.mediaDevices.getUserMedia(constraints);

    myVad = await vad.MicVAD.new({
      stream: stream,
      positiveSpeechThreshold: 0.8,
      negativeSpeechThreshold: 0.4,
      minSpeechFrames: 5,
      preSpeechPadFrames: 10,
      redemptionFrames: 15,

      onSpeechStart: () => {
        if (!isConnected) return;
        if (isPlayingAudio) bargeIn();
        setState('recording');
      },

      onSpeechEnd: (audio) => {
        if (!isConnected || !isConversationActive) return;
        const wavBuffer = float32ToWav(audio, 16000);
        ws.send(wavBuffer);
        setState('processing');
      }
    });

    await myVad.start();
    isConversationActive = true;
    setState('listening');
    console.log('[VAD] Started with mic:', selectedMicId || 'default');
  } catch (err) {
    console.error('[VAD] Error:', err);
    if (err.name === 'NotAllowedError') {
      showToast('Micro bloqué — ouvrez les paramètres (roue) pour autoriser');
    } else if (err.name === 'NotFoundError') {
      showToast('Aucun micro trouvé — vérifiez les paramètres');
    } else {
      showToast('Erreur micro : ' + (err.message || 'inconnue'));
    }
    disconnect();
  }
}

function stopVAD() {
  if (myVad) {
    try { myVad.destroy(); } catch (e) {}
    myVad = null;
  }
}

// ── Barge-in ──────────────────────────────────────────────────────────────
function bargeIn() {
  stopAudioPlayback();
  stopThinkingSound();
  audioEndReceived = false;
  if (ws && ws.readyState === WebSocket.OPEN) {
    ws.send(JSON.stringify({ type: 'barge_in' }));
  }
}

// ── Audio playback (MP3 chunks via AudioContext) ──────────────────────────
function handleAudioChunk(arrayBuffer) {
  setState('speaking');
  audioQueue.push(arrayBuffer);
  if (!isPlayingAudio) playNextChunk();
}

async function playNextChunk() {
  if (audioQueue.length === 0) {
    isPlayingAudio = false;
    if (audioEndReceived) {
      audioEndReceived = false;
      if (isConversationActive) setState('listening');
    }
    return;
  }

  isPlayingAudio = true;

  if (!audioContext) {
    audioContext = new (window.AudioContext || window.webkitAudioContext)();
  }
  if (audioContext.state === 'suspended') {
    await audioContext.resume();
  }

  // [Correction 5] Set output device if supported; warn user if not
  if (selectedSpkId && audioContext.setSinkId) {
    try {
      await audioContext.setSinkId(selectedSpkId);
    } catch (e) {
      console.warn('[Audio] setSinkId failed — output device selection not supported:', e.message);
      showToast('Changement de sortie audio non supporté par ce navigateur');
    }
  }

  const buffer = audioQueue.shift();

  try {
    const audioBuffer = await audioContext.decodeAudioData(buffer.slice(0));
    const source = audioContext.createBufferSource();
    source.buffer = audioBuffer;
    source.connect(audioContext.destination);
    currentSource = source;

    source.onended = () => {
      currentSource = null;
      playNextChunk();
    };

    source.start();
  } catch (err) {
    console.error('[Audio] Decode error:', err);
    currentSource = null;
    playNextChunk();
  }
}

function stopAudioPlayback() {
  audioQueue = [];
  if (currentSource) {
    try { currentSource.stop(); } catch (e) {}
    currentSource = null;
  }
  isPlayingAudio = false;
}

// ── Pipeline stage indicator ──────────────────────────────────────────────
const PIPELINE_LABELS = {
  stt:      'Transcription',
  thinking: 'Réflexion',
  tts:      'Synthèse vocale',
  speaking: 'Léa répond...'
};

function updatePipelineStage(stage) {
  const label = PIPELINE_LABELS[stage];
  if (label && statusLabel) {
    statusLabel.textContent = label;
  }
  // When speaking starts, switch to speaking state
  if (stage === 'speaking') {
    setState('speaking');
  }
}

// ── Server messages ───────────────────────────────────────────────────────
function handleServerMessage(msg) {
  switch (msg.type) {
    case 'listening':
      if (isConversationActive) setState('listening');
      break;
    case 'processing':
      setState('processing');
      break;
    case 'pipeline_stage':
      updatePipelineStage(msg.stage);
      break;
    case 'transcript':
      addTranscript(msg.role || 'user', msg.text);
      // Conversation active — cacher le hint wake word
      if (wakeWordHint) wakeWordHint.classList.add('hidden');
      // Meeting segment count
      if (currentMode === 'meeting') {
        meetingSegments++;
        updateMeetingCount();
      }
      break;
    case 'response_text':
      addTranscript('lea', msg.text);
      break;
    case 'audio_end':
      audioEndReceived = true;
      if (!isPlayingAudio && isConversationActive) {
        audioEndReceived = false;
        setState('listening');
      }
      break;
    case 'barge_in_ack':
      setState('recording');
      break;
    case 'no_wake_word':
      console.log('[WakeWord] Ignored:', msg.text);
      if (wakeWordHint) {
        wakeWordHint.classList.remove('hidden');
        wakeWordHint.classList.add('active');
      }
      break;
    case 'conversation_end':
      console.log('[Conv] Conversation terminée');
      if (wakeWordHint) {
        wakeWordHint.classList.remove('hidden');
        wakeWordHint.classList.add('active');
      }
      addTranscript('lea', 'À bientôt !');
      break;
    case 'conversation_timeout':
      console.log('[Conv] Timeout — retour mode wake word');
      if (wakeWordHint) {
        wakeWordHint.classList.remove('hidden');
        wakeWordHint.classList.add('active');
      }
      break;
    case 'meeting_summary':
      addTranscript('lea', msg.text);
      stopMeetingTimer();
      showToast('Compte-rendu de réunion généré');
      break;
    case 'meeting_report_sent':
      showToast('Compte-rendu envoyé par email');
      break;
    case 'meeting_report_error':
      showToast('Erreur envoi email : ' + (msg.message || 'inconnue'));
      break;
    case 'deep_thinking':
      if (msg.active) {
        setState('thinking_deep');
        startThinkingSound();
      } else {
        stopThinkingSound();
      }
      break;
    case 'error':
      showToast(msg.message || 'Erreur');
      stopThinkingSound();
      break;
  }
}

// ── Transcript ────────────────────────────────────────────────────────────
function addTranscript(role, text) {
  const block = document.createElement('div');
  block.className = `transcript-block ${role === 'lea' ? 'lea' : ''}`;

  const roleSpan = document.createElement('span');
  roleSpan.className = `transcript-role ${role === 'lea' ? 'lea' : ''}`;
  roleSpan.textContent = role === 'lea' ? 'Léa' : 'Vous';

  const textP = document.createElement('p');
  textP.className = 'transcript-text';
  textP.textContent = text;

  block.appendChild(roleSpan);
  block.appendChild(textP);
  transcriptArea.appendChild(block);
  transcriptArea.scrollTop = transcriptArea.scrollHeight;
}

// ── WAV encoder (Float32 16kHz → PCM 16-bit WAV) ─────────────────────────
function float32ToWav(float32, sampleRate) {
  const numSamples = float32.length;
  const buffer = new ArrayBuffer(44 + numSamples * 2);
  const view = new DataView(buffer);

  writeStr(view, 0, 'RIFF');
  view.setUint32(4, 36 + numSamples * 2, true);
  writeStr(view, 8, 'WAVE');
  writeStr(view, 12, 'fmt ');
  view.setUint32(16, 16, true);
  view.setUint16(20, 1, true);
  view.setUint16(22, 1, true);
  view.setUint32(24, sampleRate, true);
  view.setUint32(28, sampleRate * 2, true);
  view.setUint16(32, 2, true);
  view.setUint16(34, 16, true);
  writeStr(view, 36, 'data');
  view.setUint32(40, numSamples * 2, true);

  for (let i = 0; i < numSamples; i++) {
    const s = Math.max(-1, Math.min(1, float32[i]));
    view.setInt16(44 + i * 2, s < 0 ? s * 0x8000 : s * 0x7FFF, true);
  }
  return buffer;
}

function writeStr(view, offset, str) {
  for (let i = 0; i < str.length; i++) view.setUint8(offset + i, str.charCodeAt(i));
}

// ── Toast ─────────────────────────────────────────────────────────────────
function showToast(message) {
  document.querySelectorAll('.toast').forEach(t => t.remove());
  const toast = document.createElement('div');
  toast.className = 'toast';
  toast.textContent = message;
  document.body.appendChild(toast);
  setTimeout(() => { if (toast.parentNode) toast.remove(); }, 4200);
}

// ── Button handler ────────────────────────────────────────────────────────
micBtn.addEventListener('click', () => {
  if (isConversationActive) {
    disconnect();
  } else {
    connect();
  }
});

// ── Init ──────────────────────────────────────────────────────────────────

// [Correction 2] Pre-populate device lists at page load (without requiring settings panel open)
async function initDeviceList() {
  try {
    // Check permission status first
    let permState = 'unknown';
    try {
      const result = await navigator.permissions.query({ name: 'microphone' });
      permState = result.state;
      // Listen for permission changes at page level (auto-reload on grant)
      result.onchange = () => {
        console.log('[Permission] Changed to:', result.state);
        if (result.state === 'granted') {
          stopPermissionPolling();
          location.reload();
        }
        updatePermStatus(result.state);
      };
    } catch { /* permissions API not supported (Firefox) */ }

    if (permState === 'granted') {
      // Permission already granted — get full labels
      await refreshDeviceList();
    } else {
      // No permission yet — enumerate without labels (fallback)
      await fallbackEnumerateDevices();
    }

    // Restore saved selections from localStorage
    if (selectedMicId) micSelect.value = selectedMicId;
    if (selectedSpkId) spkSelect.value = selectedSpkId;
  } catch (err) {
    console.warn('[Init] Device list pre-fill failed:', err);
  }
}

// [Correction 4] Listen for device changes (plug/unplug mic or headset)
if (navigator.mediaDevices && navigator.mediaDevices.addEventListener) {
  navigator.mediaDevices.addEventListener('devicechange', async () => {
    console.log('[Devices] Change detected, refreshing list...');
    try {
      const result = await navigator.permissions.query({ name: 'microphone' });
      if (result.state === 'granted') {
        await refreshDeviceList();
      } else {
        await fallbackEnumerateDevices();
      }
    } catch {
      // permissions API not available — try fallback
      await fallbackEnumerateDevices();
    }
  });
}

// Run init
initDeviceList();
setState('idle');
