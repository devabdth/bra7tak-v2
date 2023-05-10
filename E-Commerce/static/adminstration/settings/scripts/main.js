const openDeleteAdminDialog= async(adminData)=>{
	document.getElementById('del-dialog-msg').innerHTML= `
		If you want to confirm deleting <span style="font-weight: 900;">${adminData['name']}</span>, Please enter the Meta Key!
	`;

	document.getElementById('overlay').style.display= 'flex';
	document.getElementById('delete-admin-dialog').style.display= 'flex';

	document.getElementById('delete-admin-confirmation').onclick= ()=> {
		const keyField= document.getElementById('key');
		const keyFieldContainer= document.getElementById('key-container');
		if(!keyField.value) {
			keyFieldContainer.style.border= "1px red solid";
		}
		keyFieldContainer.style.border= "none";

		try {
			fetch(
				`./?aid=${adminData['aid']}&key=${keyField.value.trim()}`, {
					method: 'DELETE'
				}
			).then( res=> {
				if (res.status == 200) {
					window.open('./', '_self');
					return
				}

				if (res.status == 405) {
					keyFieldContainer.style.border= "1px red solid";
					document.getElementById('delete-admin-confirmation').innerHTML= "Wrong Key";
					setTimeout(()=> {
						document.getElementById('delete-admin-confirmation').innerHTML= "Delete";
					}, 3000);
					return;
				}
				document.getElementById('delete-admin-confirmation').innerHTML= "Failed!";
				setTimeout(()=> {
					document.getElementById('delete-admin-confirmation').innerHTML= "Delete";
				}, 3000);
				
			});
		} catch (e) {
			console.log(e);
			document.getElementById('delete-admin-confirmation').innerHTML= "Failed!";
			setTimeout(()=> {
				document.getElementById('delete-admin-confirmation').innerHTML= "Delete";
			}, 3000);
			

		}
	}
}

const closeDeleteAdminDialog= ()=> {
	document.getElementById('overlay').style.display= "none";
	document.getElementById('delete-admin-dialog').style.display= "none";
}

const closeCreateAdminDialog= ()=> {
	document.getElementById('overlay').style.display= "none";
	document.getElementById('create-admin-dialog').style.display= "none";
}

const openCreateAdminDialog= ()=> {
	document.getElementById('overlay').style.display= "flex";
	document.getElementById('create-admin-dialog').style.display= "flex";
}

const createAdminConfirmation= async()=> {
	const nameField= document.getElementById('name-field');
	const nameFieldContainer= document.getElementById('name-field-container');

	const usernameField= document.getElementById('username-field');
	const usernameFieldContainer= document.getElementById('username-field-container');
	
	const accessKeyField= document.getElementById('access-key-field');
	const accessKeyFieldContainer= document.getElementById('access-key-field-container');
	
	const accessCheckbox= [];
	let activeAccesses= [];
	for(let i= 0; i!= 10; i++) {
		accessCheckbox.push(document.getElementById(`${i}-checkbox`));
	}

	if(!nameField.value){
		nameFieldContainer.style.border= "1px red solid";
		return;
	}
	nameFieldContainer.style.border= "none";

	if(!usernameField.value){
		usernameFieldContainer.style.border= "1px red solid";
		return;
	}
	usernameFieldContainer.style.border= "none";
	
	if(!accessKeyField.value){
		accessKeyFieldContainer.style.border= "1px red solid";
		return;
	}
	accessKeyFieldContainer.style.border= "none";

	for( let i in accessCheckbox ) {
		if(accessCheckbox[i].checked) activeAccesses.push(i);
	}

	if(activeAccesses.length === 0) {
		for( let i in accessCheckbox ) {
			accessCheckbox[i].style.color= 'red'
		}
		return;
	}

	for( let i in accessCheckbox ) {
			accessCheckbox[i].style.color= 'var(--secondary-color);'
		}


	const payload= {
		name: nameField.value.trim(),
		username: usernameField.value.trim(),
		accessKey: accessKeyField.value.trim(),
		activeAccesses: activeAccesses
	}

	try {
		const res= await fetch(
			'./', {
				method: 'POST',
				body: JSON.stringify(payload),
				headers: { 'Content-Type': 'application/json'}
			}
		);

		if (res.status === 201) {
			window.open('./', '_self');
			return;
		}
		document.getElementById('create-admin-confirmation').innerHTML= "Try Again Later!";
		document.getElementById('create-admin-confirmation').onclick= ()=> {};
		setTimeout(()=> {
			document.getElementById('create-admin-confirmation').innerHTML= "Create!";
			document.getElementById('create-admin-confirmation').onclick= createAdminConfirmation;
		}, 3000);

	} catch (e) {
		console.log(e);
		document.getElementById('create-admin-confirmation').innerHTML= "Failed!";
		document.getElementById('create-admin-confirmation').onclick= ()=> {};
		setTimeout(()=> {
			document.getElementById('create-admin-confirmation').innerHTML= "Create!";
			document.getElementById('create-admin-confirmation').onclick= createAdminConfirmation;
		}, 3000);

	}
}