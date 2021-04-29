function sendTestNotification(){
	fetch('/triggerTestPushNotification', {
		method : 'POST',
		headers : {
			'Content-Type' : 'application/json'
		},
		body : JSON.stringify({
			'title' : 'Test',
			'body' : 'Test Notification'
		})
	})
}


function disableTestPushButton(){
	var element = document.getElementById("testPushButtonStyle")
	element.disabled = true;
}

disableTestPushButton();