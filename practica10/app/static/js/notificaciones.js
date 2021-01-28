try {
  if (!('serviceWorker' in navigator) || !('showTrigger' in Notification.prototype)) {
    throw 'ServiceWorker or Notification Trigger API is not supported'
  }

  function pad(num, size = 2) {
    let s = num + '';
    while (s.length < size) s = '0' + s;
    return s;
  }

  // register the ServiceWorker
  navigator.serviceWorker.register('/static/js/service-worker.js').then(function(reg) {
    var botones = document.querySelectorAll('.botonNotif');
    for(var i=0;i<botones.length;i++){
      hora = botones[i].getAttribute('data-hour')
      nombre = botones[i].getAttribute('data-name')
      img = botones[i].getAttribute('data-img')
      botones[i].onclick= async () => {
        Notification.requestPermission().then(permission => {
          if (permission !== 'granted') {
            alert('you need to allow push notifications');
          } else {
            for (var i=0;i<7;i++){
              var timestamp = new Date()
              timestamp.setHours(parseInt(hora.split(":")[0]))
              timestamp.setMinutes(parseInt(hora.split(":")[1]))
              timestamp.setSeconds(0)
              timestamp.setDate(timestamp.getDate()+i)
              const scheduledTime = new Date(timestamp);
              reg.showNotification(
                'Salida de pokemon ' + nombre,
                {
                  tag: timestamp, // a unique ID
                  body: 'Son las ' + pad(scheduledTime.getHours()) + ':' + pad(scheduledTime.getMinutes()) + ", va a salir " + nombre, // content of the push notification
                  showTrigger: new TimestampTrigger(timestamp), // set the time for the push notification
                  data: {
                    url: "/practica4?nombre="+nombre, // pass the current url to the notification
                  },
                  icon: img,
                }
              );
            }
          }
          alert("Alerta configurada para " + nombre )
        })
    }
    };
  })


  // s


  // listen to the postMessage Event
  navigator.serviceWorker.addEventListener('message', event => console.log(event.data));

} catch (e) {
  alert(e)
}
