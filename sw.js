// Service Worker — Cuadrante Personal 2026
const CACHE = 'cuadrante-v1';
const ASSETS = [
  '/Cuadrantepersonal/',
  '/Cuadrantepersonal/index.html',
  '/Cuadrantepersonal/manifest.json',
  '/Cuadrantepersonal/icon-192.png',
  '/Cuadrantepersonal/icon-512.png'
];

self.addEventListener('install', e => {
  e.waitUntil(caches.open(CACHE).then(c => c.addAll(ASSETS)).catch(() => {}));
  self.skipWaiting();
});

self.addEventListener('activate', e => {
  e.waitUntil(caches.keys().then(keys =>
    Promise.all(keys.filter(k => k !== CACHE).map(k => caches.delete(k)))
  ));
  self.clients.claim();
});

self.addEventListener('fetch', e => {
  // Para peticiones a Supabase, siempre red (datos en tiempo real)
  if(e.request.url.includes('supabase.co')) return;
  e.respondWith(
    fetch(e.request).catch(() => caches.match(e.request))
  );
});
