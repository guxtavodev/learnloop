const cacheName = 'my-pwa-cache-v1';
const filesToCache = [
  '/',
  '/static/img/logo.png',
  '/static/icon.png',
  '/static/style.css',
  '/static/script.js'
];

self.addEventListener('install', function(e) {
  e.waitUntil(
    caches.open(cacheName).then(function(cache) {
      return cache.addAll(filesToCache);
    })
  );
});

self.addEventListener('fetch', function(e) {
  e.respondWith(
    caches.match(e.request).then(function(response) {
      return response || fetch(e.request);
    })
  );
});
