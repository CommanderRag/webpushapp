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


function animateButtonTransition(){
	if(Notification.permission === "granted"){
	document.getElementById("testPushButtonStyle").style.animation="animate 3s";
	document.getElementById("testPushButtonStyle").disabled=false;
	document.getElementById("testPushButtonStyle").enabled=true;
	}
}

function triggerButtonTransition(){
	setTimeout(animateButtonTransition, 3000);
}

triggerButtonTransition();
