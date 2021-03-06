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
   const swRegistration = await registerServiceWorker();
   const permission = Notification.permission;
   
   if(permission !== 'granted'){
     
    Notification.requestPermission().then(async (permission_n) => {
       
      if(permission_n == "granted"){
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
            const subscription = await swRegistration.pushManager.subscribe(options)
            console.log(JSON.stringify(subscription))
            postSubscriptionToServer(subscription);
          })
        }
        catch (error){
          console.error(error);
        }

       }

     })

   }
   else{
     console.log("Permission already granted!");
   }

}


const main = async () => {
  check();
  const swRegistration = await registerServiceWorker();
}
main();