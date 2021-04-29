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
	$('.testPushButtonStyle').addClass('animated');
	setTimeout(function(){
		document.getElementById("testPushButtonStyle").disabled=false;
		document.getElementById("testPushButtonStyle").enabled=true;
		$(".testPushButtonStyle").removeClass("animated");
		}, 600)
	}
}

function triggerButtonTransition(){
	setTimeout(animateButtonTransition, 3000);
}

triggerButtonTransition();
