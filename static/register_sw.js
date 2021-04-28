const check = () => {
  if(('serviceworker' in navigator &&  'PushManager' in window))
  {
    console.info('ServiceWorker and Push Notifications supported');
  }
}

const registerServiceWorker = async () => {
  const swRegisteration = await navigator.serviceWorker.register('static/sw.js');
  return swRegisteration;
}

const requestNotificationPermission = async () => {
  const permission = await Notification.requestPermission();
  if(permission !== 'granted'){
    console.error('Permission not granted');
    document.addEventListener("DOMContentLoaded", function(event){
      document.getElementById("testPushButtonStyle").disabled = true;
    });
  }
  if(permission === 'denied'){
    document.addEventListener("DOMContentLoaded", function(event){
      document.getElementById("testPushButtonStyle").enabled = false;
      document.getElementById("testPushButtonStyle").disabled = true;
    });
  }
  if(permission === 'granted'){
    console.info('Permission already granted!');
    document.addEventListener("DOMContentLoaded", function(event){
      document.getElementById("testPushButtonStyle").disabled = false;
      document.getElementById("testPushButtonStyle").enabled = true;
      navigator.serviceWorker.getRegistrations().then(async (registrations) => {
        for(let registration of registrations){
          registration.unregister();
        }
        await registerServiceWorker();
      })

    });
    main();
  }
}

const main = async () => {
  check();
  const swRegistration = await registerServiceWorker();
  document.addEventListener("DOMContentLoaded", function(event){
    if(Notification.permission !== "granted"){
    document.getElementById("testPushButtonStyle").disabled = true;
    document.getElementById("testPushButtonStyle").enabled = false;
    }
    if(Notification.permission === "granted"){
      document.getElementById("testPushButtonStyle").disabled = false;
      document.getElementById("testPushButtonStyle").enabled = true;
      navigator.serviceWorker.startMessages()
    }
  });
}

main()