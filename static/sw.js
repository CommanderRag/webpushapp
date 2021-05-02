self.addEventListener('install', async () => {
  console.log('Service worker installing.');
})

self.addEventListener('activate', async () => {
  console.log('Service worker activating.');
}

)

self.addEventListener('push', async function received(event) {
  let data, title, body;  
  data = event.data.text();
  console.log("Push received event - " + data);

    try{
      data = JSON.parse(data);
      console.log(JSON.stringify(data));
      title = data.title;
      body = data.body;
    }catch(error){
      console.error(error);
      title = "Undefined";
      body = data;
    }

    event.waitUntil(showNotificationSW(title, body, self.registration));

}) 


const urlB64ToUint8Array = base64String => {
  const padding = '='.repeat((4 - (base64String.length % 4)) % 4)
  const base64 = (base64String + padding).replace(/\-/g, '+').replace(/_/g, '/')
  const rawData = atob(base64)
  const outputArray = new Uint8Array(rawData.length)
  for (let i = 0; i < rawData.length; ++i) {
    outputArray[i] = rawData.charCodeAt(i)
  }
  return outputArray
}


async function postSubscriptionToServer(subscription){
    fetch('/registerSubscriptions', {
      method : 'POST',
      headers : {
        'Content-Type' : 'application/json'
      },
      body : JSON.stringify(subscription)
    }).then(response => response.text).then(data => {

      json_obj = JSON.parse(data);
      console.log(JSON.stringify(data))
      if(json_obj.status == 200){
        $('.testPushButtonStyle').addClass('animated');
        setTimeout(function(){
          $('.testPushButtonStyle').attr("disabled", false);
          $('.testPushButtonStyle').attr("enabled", true);
          $(".testPushButtonStyle").removeClass("animated");
          }, 1500)     
      }
    })
}

async function showNotificationSW(title, body, swRegistration){
  const options = {
    title : title,
    body: body,
    icon : '/favicon.ico',
    badge : '/favicon.ico',
    tag : 'notification',
    renotify : true,
  }

  return swRegistration.showNotification(title, options);
}