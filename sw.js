// Service Worker — Cuadrante Personal 2026
const CACHE = 'cuadrante-v27';
const ASSETS = [
  '/Cuadrantepersonal/',
  '/Cuadrantepersonal/index.html',
  '/Cuadrantepersonal/catalogo_turnos_completo.js',
  '/Cuadrantepersonal/manifest.json',
  '/Cuadrantepersonal/icon-192.png',
  '/Cuadrantepersonal/icon-512.png'
];

self.addEventListener('install', e => {
  self.skipWaiting();
  e.waitUntil(
    caches.open(CACHE)
      .then(c => c.addAll(ASSETS))
      .catch(err => console.warn('SW cache addAll error:', err))
  );
});

self.addEventListener('activate', e => {
  e.waitUntil(
    caches.keys().then(keys =>
      Promise.all(keys.filter(k => k !== CACHE).map(k => caches.delete(k)))
    ).then(() => self.clients.claim())
  );
});

self.addEventListener('message', e => {
  if (e.data === 'skipWaiting') {
    self.skipWaiting();
  }
  if (e.data === 'clearCache') {
    caches.keys().then(keys => Promise.all(keys.map(k => caches.delete(k))));
  }
});

self.addEventListener('fetch', e => {
  // Peticiones a Supabase: siempre directo a la red (datos en tiempo real)
  if(e.request.url.includes('supabase.co')) return;

  // Para navegación y archivos HTML: SIEMPRE Network First para ver cambios al instante
  if(e.request.mode === 'navigate' || e.request.url.endsWith('.html') || e.request.url.endsWith('/') || e.request.url.includes('/Cuadrantepersonal/index.html')) {
    e.respondWith(
      fetch(e.request, { cache: 'no-cache' })
        .then(res => {
          if(res && res.status === 200) {
            const clone = res.clone();
            caches.open(CACHE).then(c => c.put(e.request, clone));
          }
          return res;
        })
        .catch(() => caches.match(e.request))
    );
    return;
  }

  // Resto de activos: Network first con fallback a caché
  e.respondWith(
    fetch(e.request)
      .then(res => {
        if(res && res.status === 200) {
          const clone = res.clone();
          caches.open(CACHE).then(c => c.put(e.request, clone));
        }
        return res;
      })
      .catch(() => caches.match(e.request))
  );
});
