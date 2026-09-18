// Service Worker — Cuadrante Personal 2026
const CACHE = 'cuadrante-v6';
const ASSETS = [
  '/Cuadrantepersonal/',
  '/Cuadrantepersonal/index.html',
  '/Cuadrantepersonal/catalogo_turnos_completo.js',
  '/Cuadrantepersonal/manifest.json',
  '/Cuadrantepersonal/icon-192.png',
  '/Cuadrantepersonal/icon-512.png'
];

self.addEventListener('install', e => {
  e.waitUntil(caches.open(CACHE).then(c => c.addAll(ASSETS)).catch(() => {}));
  self.skipWaiting();
});

self.addEventListener('activate', e => {
  e.waitUntil(
    caches.keys().then(keys =>
      Promise.all(keys.filter(k => k !== CACHE).map(k => caches.delete(k)))
    ).then(() => self.clients.claim())
  );
});

self.addEventListener('fetch', e => {
  // Para peticiones a Supabase, siempre red (datos en tiempo real)
  if(e.request.url.includes('supabase.co')) return;
  // Network first con fallback a cache para garantizar que siempre se vean las últimas actualizaciones
  if(e.request.mode === 'navigate' || e.request.url.endsWith('.html') || e.request.url.endsWith('/')) {
    e.respondWith(
      fetch(e.request, { cache: 'no-cache' })
        .then(res => {
          const clone = res.clone();
          caches.open(CACHE).then(c => c.put(e.request, clone));
          return res;
        })
        .catch(() => caches.match(e.request))
    );
    return;
  }
  e.respondWith(
    fetch(e.request).catch(() => caches.match(e.request))
  );
});
