
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



window.onload = () => {
  sendCodeAgain();

inputElements = [...document.querySelectorAll('input.code-input')]

inputElements.forEach((ele,index)=>{
  ele.addEventListener('keydown',(e)=>{
    if(e.keyCode === 8 && e.target.value==='') inputElements[Math.max(0,index-1)].focus()
  })
  ele.addEventListener('input',(e)=>{
    const [first,...rest] = e.target.value
    e.target.value = first ?? '' // first will be undefined when backspace was entered, so set the input to ""
    const lastInputBox = index===inputElements.length-1
    const didInsertContent = first!==undefined
    if(didInsertContent && !lastInputBox) {
      // continue to input the rest of the string
      inputElements[index+1].focus()
      inputElements[index+1].value = rest.join('')
      inputElements[index+1].dispatchEvent(new Event('input'))
    }
  })
})

}

const StageOneSubmit = async () => {
  const digits = ['one', 'two', 'three', 'four'].map((t) => document.getElementById(`digit-${t}`));
    digits.map((digit) => {
    if(digit.value.trim().length === 0) {
      digit.style.border = "1px red solid";
    } else {
      digit.style.border = "none";
    }
  });

  const code = `${digits[0].value.trim()}${digits[1].value.trim()}${digits[2].value.trim()}${digits[3].value.trim()}`;
  if (code.length !== 4) {
    digits.map((digit) => {
        digit.style.border = "1px red solid";
    });
    return;
  }

  const res = await fetch(`./confrimCode/?code=${code}`, {
    method: 'get'
  });

  if(res.status == 200) {
    const confirmCode = document.getElementById('confirm-email');
    const completeProfile = document.getElementById('complete-profile');
    confirmCode.style.display = "none";
    completeProfile.style.display = "flex";
    return;
  }

  digits.map((digit) => {
    digit.style.border = "1px red solid";
  });
}

const sendCodeAgain = async (toastContent, lang) => {
  const res = await fetch('../sendCodeAgain/', {
    method: 'get'
  });

  if (res.status === 200) {
    const digits = ['one', 'two', 'three', 'four'].map((t) => document.getElementById(`digit-${t}`));
    digits.map((digit) => {
      digit.value = "";
    });

    showToast({
      msg: toastContent[lang]["codeSentSuccessfully!"],
      borderColor: 'green',
      toastColor: 'green',
      lang: lang
    });
  }

}

const changeEmail = async () => {
  const res = await fetch('../changeEmail', {
    method: "get"
  })
  window.location.replace('./');
  window.open('../signup', '_self');
}

let currentCity;

const toggleCitiesDropdown = () => {
  document.getElementById(`cities-dropdown`).classList.toggle("show");
}

const filter = () => {
  var input, filter, ul, li, a, i;
  input = document.getElementById("city-search");
  filter = input.value.toUpperCase();
  div = document.getElementById("cities-dropdown");
  button = div.getElementsByTagName("button");
  for (i = 0; i < button.length; i++) {
    txtValue = button[i].textContent || button[i].innerText;
    if (txtValue.toUpperCase().indexOf(filter) > -1) {
      button[i].style.display = "";
    } else {
      button[i].style.display = "none";
    }
  }
}


const chooseCity = (cityText, city, lang) => {
  const btn = document.getElementById(`cities-dropbtn`);
  currentCity = city;
  btn.innerHTML = cityText;
  btn.innerText = cityText;
  btn.textContent = cityText;

  toggleCitiesDropdown();

}

let currentGender;

const toggleGendersDropdown = () => {
  document.getElementById(`genders-dropdown`).classList.toggle("show");
}

const gendersFilter = () => {
  var input, filter, ul, li, a, i;
  input = document.getElementById("gender-search");
  filter = input.value.toUpperCase();
  div = document.getElementById("genders-dropdown");
  button = div.getElementsByTagName("button");
  for (i = 0; i < button.length; i++) {
    txtValue = button[i].textContent || button[i].innerText;
    if (txtValue.toUpperCase().indexOf(filter) > -1) {
      button[i].style.display = "";
    } else {
      button[i].style.display = "none";
    }
  }
}


const chooseGender = (genderText, gender, lang) => {
  const btn = document.getElementById(`genders-dropbtn`);
  currentGender = gender;
  btn.innerHTML = genderText;
  btn.innerText = genderText;
  btn.textContent = genderText;

  toggleGendersDropdown();

}

const compleProfileSubmit = async (toastContent, lang, url, email) => {
  const nameField = document.getElementById('name');
  const phoneField = document.getElementById('phone');
  const addressOneField = document.getElementById('addressOne');
  const addressTwoField = document.getElementById('addressTwo');
  const citiesBtn = document.getElementById('cities-dropbtn');
  const gendersBtn = document.getElementById('genders-dropbtn');
  const birthField = document.getElementById('birth');

  if(nameField.value.trim() < 8 || nameField.value.trim() > 32) {
    showToast({
      msg: toastContent[lang]["notValidName"],
      toastColor: 'red',
      borderColor: 'red',
      lang
    });
    nameField.style.borderColor = 'red';
    nameField.style.color = 'red';
    return;
  }

  nameField.style.borderColor = '#888';
  nameField.style.color = '#6b469c';

  if(phoneField.value.trim() < 8) {
    showToast({
      msg: toastContent[lang]["notValidBio"],
      toastColor: 'red',
      borderColor: 'red',
      lang: lang,
    });
    phoneField.style.borderColor = 'red';
    phoneField.style.color = 'red';
    return;
  }
  
  phoneField.style.borderColor = '#888';
  phoneField.style.color = '#6b469c';

  if(addressOneField.value.trim() < 8) {
    showToast({
      msg: toastContent[lang]["notValidBio"],
      toastColor: 'red',
      borderColor: 'red',
      lang: lang,
    });
    addressOneField.style.borderColor = 'red';
    addressOneField.style.color = 'red';
    return;
  }
  
  addressOneField.style.borderColor = '#888';
  addressOneField.style.color = '#6b469c';

  if(birthField.value.trim() < 8) {
    showToast({
      msg: toastContent[lang]["notValidBio"],
      toastColor: 'red',
      borderColor: 'red',
      lang: lang,
    });
    birthField.style.borderColor = 'red';
    birthField.style.color = 'red';
    return;
  }
  
  birthField.style.borderColor = '#888';
  birthField.style.color = '#6b469c';

  if (currentCity === undefined) {
    citiesBtn.style.border = '2px red solid';
    showToast({
      msg: toastContent[lang]["notValidCity"],
      toastColor: 'red',
      borderColor: 'red',
      lang: lang,
    });
    return;
  }
  citiesBtn.style.border = 'none';

  if (currentGender === undefined) {
    gendersBtn.style.border = '2px red solid';
    showToast({
      msg: toastContent[lang]["notValidCity"],
      toastColor: 'red',
      borderColor: 'red',
      lang: lang,
    });
    return;
  }
  gendersBtn.style.border = 'none';


  const payload = {
    name: nameField.value.trim(),
    phone: phoneField.value.trim(),
    birth: birthField.value.trim(),
    addressLineOne: addressOneField.value.trim(),
    addressLineTwo: addressTwoField.value.trim(),
    gender: currentGender,
    city: currentCity,
  }

  console.log(payload)

  const res = await fetch(
    '../confirmSignUp/', {
      method: 'POST',
      body: JSON.stringify(payload),
      mode: 'cors',
      cache: 'no-cache',
      credentials: 'same-origin' ,

      headers: { 
        'Content-Type': 'application/json',
        "Access-Control-Allow-Origin": "*",
       }
  });

  if (res.status === 201) {
    window.open(`/login/?email=${email}`, '_self')
  }

}