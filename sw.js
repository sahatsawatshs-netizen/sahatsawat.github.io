const CACHE_NAME = 'expense-scanner-pwa-v1';

// ไฟล์ที่ต้องการแคชเก็บไว้ในเครื่อง
const urlsToCache = [
  './',
  './index.html',
  './manifest.json',
  'https://cdn.tailwindcss.com',
  'https://unpkg.com/lucide@latest',
  'https://cdn.jsdelivr.net/npm/jsqr@1.4.0/dist/jsQR.min.js',
  'https://cdn.jsdelivr.net/npm/tesseract.js@5.0.5/dist/tesseract.min.js'
];

self.addEventListener('install', event => {
  event.waitUntil(
    caches.open(CACHE_NAME)
      .then(cache => {
        return cache.addAll(urlsToCache);
      })
  );
});

self.addEventListener('fetch', event => {
  event.respondWith(
    caches.match(event.request)
      .then(response => {
        // หากมีไฟล์ในแคช ให้ใช้ของในเครื่อง (Offline Mode)
        if (response) {
          return response;
        }
        // ถ้าไม่มีให้ดึงผ่านอินเทอร์เน็ตปกติ
        return fetch(event.request);
      })
  );
});

// อัปเดตแคชใหม่เมื่อมีการเปลี่ยนเวอร์ชัน
self.addEventListener('activate', event => {
  const cacheWhitelist = [CACHE_NAME];
  event.waitUntil(
    caches.keys().then(cacheNames => {
      return Promise.all(
        cacheNames.map(cacheName => {
          if (cacheWhitelist.indexOf(cacheName) === -1) {
            return caches.delete(cacheName);
          }
        })
      );
    })
  );
});
