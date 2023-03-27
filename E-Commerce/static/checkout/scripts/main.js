let order = {}
let currentCity, currentUserId;

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


const initFormsSections = () => {
  document.getElementById('personal-information').style.display = "flex";
  document.getElementById('shipping-information').style.display = "none";
  document.getElementById('payment-information').style.display = "none";
  document.getElementById('complete-order').style.display = "none";
}

const initFormsFields = (userData, cities, genders, lang) => {
  currentUserId = userData['id'];
  document.getElementById('username').value = userData['name'];
  document.getElementById('email').value = userData['email'];
  document.getElementById('phone').value = userData['phone'];

  const genderBtn = document.getElementById(`genders-dropbtn`);
  currentGender = userData['gender'];
  genderBtn.innerHTML = genders[lang][userData.gender];
  genderBtn.innerText = genders[lang][userData.gender];
  genderBtn.textContent = genders[lang][userData.gender];


  document.getElementById('address-line-one').value = userData['addressLineOne'];
  document.getElementById('address-line-two').value = userData['addressLineTwo'];

  const cityBtn = document.getElementById(`cities-dropbtn`);
  currentCity = userData.cityCode;
  cityBtn.innerHTML = cities[lang][userData.cityCode];
  cityBtn.innerText = cities[lang][userData.cityCode];
  cityBtn.textContent = cities[lang][userData.cityCode];
}

const personalInformationConfirmation = () => {
  const username = document.getElementById('username');
  if (username.value.length < 8) {
    username.style.border = "1px red solid";
    return;
  }
  username.style.border = "none";
  const email = document.getElementById('email');
  if (email.value.length < 8) {
    email.style.border = "1px red solid";
    return;
  }
  email.style.border = "none";
  const phone = document.getElementById('phone');
  if (phone.value.length < 8) {
    phone.style.border = "1px red solid";
    return;
  }
  phone.style.border = "none";

  const genderBtn = document.getElementById(`genders-dropbtn`);
  if (currentGender === undefined) {
    genderBtn.style.border = "1px red solid";
    return;
  }
  genderBtn.style.border = "none";

  order.username = username.value.trim();
  order.email = email.value.trim();
  order.phone = phone.value.trim();
  order.gender = currentGender;

  document.getElementById('progress-bar').style.background = "linear-gradient(90deg, var(--main-color) 50%, var(--bg-color) 50%)";
  document.getElementById('shipping-information-icon').classList.add('active');
  document.getElementById('shipping-information').style.display = "flex";
  document.getElementById('personal-information').style.display = "none";
}

const shippingInformationConfirmation = () => {
  const commentsField = document.getElementById('comments');
  const addressLineOne = document.getElementById('address-line-one');
  if (addressLineOne.value.length < 8) {
    addressLineOne.style.border = "1px red solid";
    return;
  }
  addressLineOne.style.border = "none";

  const addressLineTwo = document.getElementById('address-line-two');
  const citiesBtn = document.getElementById(`cities-dropbtn`);
  if (currentCity === undefined) {
    citiesBtn.style.border = "1px red solid";
    return;
  }
  citiesBtn.style.border = "none";

  order.addressLineOne = addressLineOne.value.trim();
  order.addressLineTwo = addressLineOne.value.trim();
  order.comments = commentsField.value.trim();
  order.city = currentCity;

  document.getElementById('progress-bar').style.background = "linear-gradient(90deg, var(--main-color) 75%, var(--bg-color) 75%)";
  document.getElementById('payment-information-icon').classList.add('active');
  document.getElementById('shipping-information').style.display = "none";
  document.getElementById('payment-information').style.display = "flex";
}

const paymentInformationConfirmation = async (lang) => {
  let selectedCheckoutMethod;
  const supportedCheckoutMethodsCheckboxes = document.getElementsByClassName('supported-checkout-method');
  for (var cb in supportedCheckoutMethodsCheckboxes) {
    if (supportedCheckoutMethodsCheckboxes[cb].checked) {
      selectedCheckoutMethod = Number.parseInt(supportedCheckoutMethodsCheckboxes[cb].id.split('-')[0]);
      break;
    }
  }
  if (selectedCheckoutMethod === undefined) {
    document.getElementById('methods').style.border = "1px red solid";
    return;
  }
  document.getElementById('methods').style.border = "none";
  order.chechoutMethod = selectedCheckoutMethod;
  document.getElementById('order-confirmation').innerHTML = "Loading";
  document.getElementById('order-confirmation').onclick = () => { };
  try {
    order.uid = currentUserId;
    const res = await fetch(`./?${window.location.href.split('?')[1]}`, {
      method: 'POST',
      body: JSON.stringify({ order: order }),
      mode: 'cors',
      cache: 'no-cache',
      credentials: 'same-origin',

      headers: { 'Content-Type': 'application/json' }
    });

    if (res.status == 201) {
      document.getElementById('payment-information').style.display = "none";
      document.getElementById('complete-order').style.display = "flex";
      return;
    }
    document.getElementById('order-confirmation').innerHTML = "Failed";
    document.getElementById('order-confirmation').onclick = () => { };
    setTimeout(() => {
      document.getElementById('order-confirmation').innerHTML = lang == "en" ? "Submit" : "إكمال";
      document.getElementById('order-confirmation').onclick = () => {
        paymentInformationConfirmation(lang);
      };

    }, 3000);

  } catch (e) {
    document.getElementById('order-confirmation').innerHTML = "Failed";
    document.getElementById('order-confirmation').onclick = () => { };
    setTimeout(() => {
      document.getElementById('order-confirmation').innerHTML = lang == "en" ? "Submit" : "إكمال";
      document.getElementById('order-confirmation').onclick = () => {
        paymentInformationConfirmation(lang);
      };

    }, 3000);

  }

}