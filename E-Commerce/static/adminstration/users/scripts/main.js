const closeDeleteDialog= ()=> {
	document.getElementById('overlay').style.display= "none";
	document.getElementById('delete-dialog').style.display= "none";
}



const openDeleteDialog= (user, url)=> {
	document.getElementById('overlay').style.display= "flex";
	document.getElementById('overlay').onclick= ()=> {
		closeDeleteDialog();
	}

	document.getElementById('delete-dialog').style.display= "flex";
	document.getElementById('delete-dialog-confirmation-msg').innerHTML= `
		Are you sure you want to delete <span style="font-weight: 900;">(${user["name"]})</span> account?<br><br>
		<span style="font-weight: 900;">Notice:</span><br>
		- User Data will be deleted.<br>
		- All Orders the user have placed will be redirected to unregistered.<br>
		- E-Mail will be banned from the platform.<br>
		- This action will be a notification send to the board.

	`;

	document.getElementById('delete-cancelation').onclick= ()=> {
		closeDeleteDialog();
	}

	document.getElementById('delete-confirmation').onclick= ()=> {
		deleteUser(user["id"]);
	}
}


const deleteUser= async (uid)=> {
	try{
		document.getElementById('delete-dialog-status-msg').innerHTML= "Loading..."
		const res = await fetch(
			`./?uid=${uid}`, {
				method: "DELETE"
			}
		);

		if (res.status !== 200) {
			console.log(res.status);
			document.getElementById('delete-dialog-status-msg').innerHTML= "Failed!";
			return;
		}

		window.open('./', '_self');

	} catch(e) {
		console.log(e);
		document.getElementById('delete-dialog-status-msg').innerHTML= "Failed!"
	}

}

const usersFiltrationClear = ()=> {
	const nameField= document.getElementById('name-field');
	const emailField= document.getElementById('email-field');

	if(nameField.value.trim().length !== 0 || emailField.value.trim().length !== 0) {
		window.open(window.location.href.split('?')[0], '_self');
	}
}


const usersFiltrationSubmit = ()=> {
	const nameField= document.getElementById('name-field');
	const emailField= document.getElementById('email-field');
	const nameFieldContainer= document.getElementById('name-field-container');
	const emailFieldContainer= document.getElementById('email-field-container');

	if (nameField.value.trim().length === 0 && emailField.value.trim().length=== 0) {
		nameFieldContainer.style.border= "1px red solid";
		emailFieldContainer.style.border= "1px red solid";
		return;
	}
	nameFieldContainer.style.border= "none";
	emailFieldContainer.style.border= "none";
	window.open(`./?name=${nameField.value.trim()}&email=${emailField.value.trim()}`, '_self');
}

