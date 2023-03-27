const login= async ()=> {
	const usernameField= document.getElementById('username-field');
	const usernameFieldContainer= document.getElementById('username-field-container');
	const authKeyField= document.getElementById('auth-key-field');
	const authKeyFieldContainer= document.getElementById('auth-key-field-container');
	const status= document.getElementById('status');


	if(!usernameField.value) {
		usernameFieldContainer.style.border= "1px red solid";
		status.innerHTML= "Not a valid Username";
		return;
	}
	usernameFieldContainer.style.border= "none";
	status.innerHTML= "";

	if(!authKeyField.value) {
		authKeyFieldContainer.style.border= "1px red solid";
		status.innerHTML= "Not a valid Auth Key";
		return;
	}
	authKeyFieldContainer.style.border= "none";
	status.innerHTML= "";

	try {
		const res= await fetch('./', {
			method: 'PATCH',
			body: JSON.stringify({
				username: usernameField.value.trim(),
				accessKey: authKeyField.value.trim(),
			}),
			headers: { 'Content-Type': 'application/json' }
		});
		if (res.status === 200) {
			window.open('../settings/', '_self');
			return;
		}

		if (res.status === 404) {
			usernameFieldContainer.style.border= "1px red solid";
			status.innerHTML= "Username not found!"
			return;
		}

		if (res.status === 403) {
			authKeyFieldContainer.style.border= "1px red solid";
			status.innerHTML= "Auth key not correct!"
			return;
		}

		usernameFieldContainer.style.border= "1px red solid";
		authKeyFieldContainer.style.border= "1px red solid";
		status.innerHTML ="Please, Try again Later!";
	} catch (e) {
		console.log(e);
	}
}