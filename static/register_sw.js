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
   Notification.requestPermission().then(async (permission) => {
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
      });
  };
  
    main();
  });
}


const main = async () => {
  check();
  const swRegistration = await registerServiceWorker();
  const permission = await Notification.requestPermission();
  document.addEventListener("DOMContentLoaded", function(event){
    if(permission !== "granted"){
    document.getElementById("testPushButtonStyle").disabled = true;
    document.getElementById("testPushButtonStyle").enabled = false;
    }
    if(permission === "granted"){
      document.getElementById("testPushButtonStyle").disabled = false;
      document.getElementById("testPushButtonStyle").enabled = true;

      let serverPublicKey;
      try {
          fetch('/get-public-key').then(response => response.text()).then(async data =>{
            console.log("server public key "+ data);
            serverPublicKey = urlB64ToUint8Array(data);
    
            console.info("server public key array", serverPublicKey);
            
            const options = {
              applicationServerKey : serverPublicKey,
              userVisibleOnly : true,
            };
            const swRegistration = await registerServiceWorker();
            console.log(JSON.stringify(swRegistration.pushManager.getSubscription()))
            const subscription = await swRegistration.pushManager.subscribe(options)
            console.log(JSON.stringify(subscription))
            postSubscriptionToServer(subscription);
          })
        }catch (error){
          console.error(error);
        }
    }
  });
}
