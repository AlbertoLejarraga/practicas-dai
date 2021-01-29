//https://github.com/nico-martin/notification-trigger-demo
// listen to the install event
self.addEventListener('install', event => console.log('ServiceWorker installed'));

self.addEventListener('notificationclick', event => {
  if (event.action === 'close') {
    event.notification.close();
  } else {
    self.clients.openWindow('/');
  }
});
// listen to the notification close
self.addEventListener('notificationclose', event => {
  event.waitUntil(self.clients.matchAll().then(clients => {
    if (clients.length) { // check if at least one tab is already open
      clients[0].postMessage('Push notification clicked!');
    }
  }));
});
