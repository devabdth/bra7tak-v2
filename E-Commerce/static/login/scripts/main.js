
const showToast = (props) => {
	const toastDiv = document.getElementById("toast");
	const toastText = document.getElementById("toast-text");

	toastDiv.style.borderColor = props.borderColor;
	toastText.innerHTML = props.msg;
	toastText.style.color = props.toastColor;
	toastText.style.fontFamily = "Raleway";
	toastDiv.style.display = "flex";

	setTimeout(() => {
		toastDiv.style.display = "none";
	}, 5000)

}



const formValidation = async (toastContent, url, lang, customRecall) => {

	const username = document.getElementById("username");
	const password = document.getElementById("password");

	// Return all field to the nature form
	username.style.color = "#111";
	username.style.borderColor = "#111";
	password.style.color = "#111";
	password.style.borderColor = "#111";

	// Validate username to be email

	const emailRe =
		/^(([^<>()[\]\.,;:\s@\"]+(\.[^<>()[\]\.,;:\s@\"]+)*)|(\".+\"))@(([^<>()[\]\.,;:\s@\"]+\.)+[^<>()[\]\.,;:\s@\"]{2,})$/i;
	if (username.value.trim().length < 8) {
		username.style.borderColor = "red";
		username.style.color = "red";
		showToast({ msg: toastContent[lang]["notValidUsername"], borderColor: "red", toastColor: "red", lang: lang });
		return;

	}
	if (!(username.value.trim().match(emailRe))) {
		username.style.borderColor = "red";
		username.style.color = "red";
		showToast({ msg: toastContent[lang]["notValidEmail"], borderColor: "red", toastColor: "red", lang: lang });
		return;
	}
	username.style.borderColor = "#111";
	username.style.color = "#111";


	// validate password not less than 8 and not more than 32
	if ((password.value.trim().length < 8 || password.value.trim().length > 32)) {
		password.style.borderColor = "red";
		password.style.color = "red";
		showToast({ msg: toastContent[lang]["notValidPassword"], borderColor: "red", toastColor: "red", lang: lang });
		return;
	}
	password.style.borderColor = "#111";
	password.style.color = "#111";

	try {
		const payload = {
			username: username.value.trim().toLowerCase(),
			password: password.value.trim()
		}
		showToast({ msg: toastContent[lang]["loading"], borderColor: "#6b469c", toastColor: "#6b469c", lang: lang });
		const res = await fetch(`/users/login/`, {
			method: "PATCH",
			body: JSON.stringify(payload),
			mode: 'cors',
		    cache: 'no-cache',
		    credentials: 'same-origin' ,

			headers: { 
		        'Content-Type': 'application/json',
		        "Access-Control-Allow-Origin": "*",
       		},
		}
		);
		// if the status Code == 404; return user not found;
		if (res.status === 404) {
			showToast({ msg: toastContent[lang]["userNotFound"], borderColor: "red", toastColor: "red", lang: lang });
			username.style.borderColor = "red";
			username.style.color = "red";
			password.style.color = "red";
			password.style.borderColor = "red";
			return;
		}

		// if the status Code == 301; return password not matched;
		else if (res.status === 301) {
			showToast({ msg: toastContent[lang]["notValidPassword"], borderColor: "red", toastColor: "red", lang: lang });
			password.style.color = "red";
			password.style.borderColor = "red";
			return;
		}

		// if the status Code == 200; return to the home page;
		else if (res.status === 200) {
			if (!customRecall) {
				window.open(`${window.location.href.split("login")[0]}${window.location.href.split("login")[1]}`, '_self');
			} else {
				window.open(customRecall, '_self');

			}
		}
		else {
			showToast({ msg: toastContent[lang]["tryAgainLater"], borderColor: "red", toastColor: "red", lang: lang });
			return;
		}

	} catch (e) {
		console.log(`Error: ${e}`);
	}
}
