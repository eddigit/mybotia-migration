const CACHE_NAME = 'mybotia-v35';
const PRECACHE_URLS = [
  '/mybotia/v11.html',
  '/mybotia/manifest.json',
  '/mybotia/icon-192x192.png',
  '/mybotia/icon-512x512.png',
  'https://fonts.googleapis.com/css2?family=Major+Mono+Display&display=swap'
];

self.addEventListener('install', e => {
  e.waitUntil(
    caches.open(CACHE_NAME).then(cache => cache.addAll(PRECACHE_URLS)).then(() => self.skipWaiting())
  );
});

self.addEventListener('activate', e => {
  e.waitUntil(
    caches.keys().then(keys => Promise.all(
      keys.filter(k => k !== CACHE_NAME).map(k => caches.delete(k))
    )).then(() => self.clients.claim())
  );
});

self.addEventListener('fetch', e => {
  const url = new URL(e.request.url);
  // Don't cache WebSocket or API requests
  if (url.protocol === 'wss:' || url.protocol === 'ws:' || url.pathname.startsWith('/ws')) return;
  
  e.respondWith(
    // Network first, fallback to cache (for a chat app, fresh content matters)
    fetch(e.request).then(response => {
      if (response && response.status === 200) {
        const responseClone = response.clone();
        caches.open(CACHE_NAME).then(cache => {
          cache.put(e.request, responseClone);
        });
      }
      return response;
    }).catch(() => caches.match(e.request))
  );
});
