
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



const formValidation = async (toastContent, url, lang) => {

    const email = document.getElementById("email");
    const password = document.getElementById("password");
    const repassword = document.getElementById("repassword");

    // Return all field to the nature form
    email.style.color = "#111";
    email.style.borderColor = "#111";
    password.style.color = "#111";
    password.style.borderColor = "#111";
    repassword.style.color = "#111";
    repassword.style.borderColor = "#111";

    // Validate email to be email

    const emailRe =
        /^(([^<>()[\]\.,;:\s@\"]+(\.[^<>()[\]\.,;:\s@\"]+)*)|(\".+\"))@(([^<>()[\]\.,;:\s@\"]+\.)+[^<>()[\]\.,;:\s@\"]{2,})$/i;
    if (email.value.trim().length < 8) {
        email.style.borderColor = "red";
        email.style.color = "red";
        showToast({ msg: toastContent[lang]["notValidUsername"], borderColor: "red", toastColor: "red", lang: lang });
        return;

    }
    if (!(email.value.trim().match(emailRe))) {
        email.style.borderColor = "red";
        email.style.color = "red";
        showToast({ msg: toastContent[lang]["notValidEmail"], borderColor: "red", toastColor: "red", lang: lang });
        return;
    }
    email.style.borderColor = "#111";
    email.style.color = "#111";

    // validate password not less than 8 and not more than 32
    if ((password.value.trim().length < 8 || password.value.trim().length > 32)) {
        password.style.borderColor = "red";
        password.style.color = "red";
        showToast({ msg: toastContent[lang]["notValidPassword"], borderColor: "red", toastColor: "red", lang: lang });
        return;
    }
    password.style.borderColor = "#111";
    password.style.color = "#111";

    // validate repassword === password
    if (!(password.value.trim() === repassword.value.trim())) {
        repassword.style.borderColor = "red";
        repassword.style.color = "red";
        showToast({ msg: toastContent[lang]["repasswordNotMatched"], borderColor: "red", toastColor: "red", lang: lang });
        return;
    }
    repassword.style.borderColor = "#111";
    repassword.style.color = "#111";

    // Send get request to validate the login process
    try {
        const payload = {
            email: email.value.trim().toLowerCase(),
            password: password.value.trim()
        }
        showToast({ msg: toastContent[lang]["loading"], borderColor: "#6b469c", toastColor: "#6b469c", lang: lang });
        const res = await fetch(`/users/signup/`, {
            method: "POST",
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
        // if status code == 201: return the home page;
        if (res.status === 201) {
            window.open('../completeSignUp/', '_self');
            return;
        }
        
        // if status code == 203: return user email exists;
        else if (res.status === 203) {
            email.style.color = "red";
            email.style.borderColor = "red";
            showToast({
                msg: toastContent[lang]["userEmailExists"],
                borderColor: "red",
                toastColor: "red",
                lang: lang,
            });
            return;
        }

        // TODO: else: return server error;
        else {
            showToast({
                msg: toastContent[lang]["tryLater"],
                borderColor: "red",
                toastColor: "red",
                lang: lang,
            })
        }
    } catch (e) {
        console.log(`Error: ${e}`);
    }
}
