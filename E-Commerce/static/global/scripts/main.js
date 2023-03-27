
const changeLang = async (url, newLang) => {
    console.log("Clicked");
    await fetch(`/config/?lang=${newLang}`);
    location.reload();
}


const openDrawer = () => {
    const drawer = document.getElementById('drawer');
    const drawerOverlay = document.getElementById('drawer-overlay');
    drawer.style.left = '0%';
    drawer.style.boxShadow = '0px 0px 15px 1px #111';
    drawerOverlay.style.display = 'flex';

}


const closeDrawer = () => {
    const drawer = document.getElementById('drawer');
    const drawerOverlay = document.getElementById('drawer-overlay');
    drawer.style.left = '-70%';
    drawer.style.boxShadow = 'none';
    drawerOverlay.style.display = 'none';

}


const addToCart = async (url, productId, count, size, color) => {
    try {
        const res = await fetch(
            `/cart/add/`,
            {
                method: 'PATCH',
                body: JSON.stringify({
                    products: [
                        {
                            id: productId,
                            count: count,
                            size: size,
                            color: color
                        }
                    ]
                }),
                mode: 'cors',
                cache: 'no-cache',
                credentials: 'same-origin',

                headers: {
                    'Content-Type': 'application/json',
                    "Access-Control-Allow-Origin": "*",
                },

            }
        );

        if (res.status == 200) {
            window.open(`/cart/?freshProduct=${productId}`, '_self');
        }

        if (res.status == 405) {
            window.open(`/login/`, '_self');
        }
    } catch (e) {
        console.log(e);
    }
}

const addToFavourites = async (url, productId, toastContent, lang) => {
    try {
        const res = await fetch(
            `/favourites/add/`,
            {
                method: 'PATCH',
                body: JSON.stringify({
                    products: [
                        {
                            id: productId,
                        }
                    ]
                }),
                mode: 'cors',
                cache: 'no-cache',
                credentials: 'same-origin',

                headers: {
                    'Content-Type': 'application/json',
                    "Access-Control-Allow-Origin": "*",
                },

            }
        );

        if (res.status == 200) {
            window.open('.', '_self')
        }

        if (res.status == 405) {
            window.open(`/login/`, '_self');
        }
    } catch (e) {
        console.log(e);
    }
}

const removeFromFavourites = async (url, productId, toastContent, lang) => {
    try {
        const res = await fetch(
            `/favourites/remove/`,
            {
                method: 'PATCH',
                body: JSON.stringify({
                    products: [
                        {
                            id: productId,
                            count: count
                        }
                    ]
                }),
                mode: 'cors',
                cache: 'no-cache',
                credentials: 'same-origin',

                headers: {
                    'Content-Type': 'application/json',
                    "Access-Control-Allow-Origin": "*",
                },

            }
        );

        if (res.status == 200) {
            window.open('.', '_self');
        }

        if (res.status == 405) {
            window.open(`/login/`, '_self');
        }
    } catch (e) {
        console.log(e);
    }
}


const removeFromCart = async (url, productId, count) => {
    try {
        const res = await fetch(
            `/cart/remove/`,
            {
                method: 'PATCH',
                body: JSON.stringify({
                    products: [
                        {
                            id: productId,
                            count: count
                        }
                    ]
                }),
                mode: 'cors',
                cache: 'no-cache',
                credentials: 'same-origin',

                headers: {
                    'Content-Type': 'application/json',
                    "Access-Control-Allow-Origin": "*",
                },

            }
        );

        if (res.status == 200) {
            window.open(`/cart/`, '_self');
        }
    } catch (e) {
        console.log(e);
    }
}

const clearCart = async (url) => {
    try {
        const res = await fetch(
            `/cart/clear/`,
            {
                method: 'PATCH',
                mode: 'cors',
                cache: 'no-cache',
                credentials: 'same-origin',

                headers: {
                    'Content-Type': 'application/json',
                    "Access-Control-Allow-Origin": "*",
                },
            }
        );

        if (res.status == 200) {
            window.open(`/cart/`, '_self');
        }
    } catch (e) {
        console.log(e);
    }
}

const checkout = (url, prods) => {
    window.open(`/checkout/`, '_self');
}

const dryCheckout = (url, prods) => {
    let params = "?prods="
    for (let prod in prods) {
        for (let i = 0; i != prods[prod][1]; i++) {
            params += `${prods[prod][0]},${prods[prod][2]},${prods[prod][3]}|`
        }
    }
    window.open(`/checkout/${params}`, '_self');
}

window.onload = () => {
    document.getElementById('drawer-icon').onclick = () => {
        openDrawer();
    }
    document.getElementById('drawer-overlay').onclick = () => {
        closeDrawer();
    }
    document.getElementById('drawer-close').onclick = () => {
        closeDrawer();
    }

    searchBar = document.getElementById('header-search');
    searchBar.onkeydown = (e) => {
        console.log(e)
        if (e.key === 'Enter') {
            window.open(`http://127.0.0.1:3030/search/?token=${searchBar.value.trim()}`, '_self');
        }
    };
}

const openFilterPanel = () => {
    const filterPanel = document.querySelector('section#products div#side-panel');
    const filterPanelOverlay = document.getElementById('side-panel-overlay');
    filterPanel.style.top = '5%';
    filterPanelOverlay.style.top = '0%';
}

const closeFilterPanel = () => {
    const filterPanel = document.querySelector('section#products div#side-panel');
    const filterPanelOverlay = document.getElementById('side-panel-overlay');
    filterPanel.style.top = '-200%';
    filterPanelOverlay.style.top = '-200%';
}

const toastContent = {
    "en": {
        "notValidUsername": "Please, Enter your email!",
        "notValidEmail": "Please, Enter a valid email!",
        "notValidPassword": "Please, Enter a valid password!",
        "loading": "Loading",
        "userNotFound": "No users were found. You may want to Sign Up",
        "userExists": "User already exists. You may want to Login!",
        "tryLater": "Please, Try again later!",
        "passwordMissmatched": "Please, Enter the right password!",
        "repasswordNotMatched": "Passwords not matched",
        "fieldEmpty": "This field can't be empty",
        "tryAgainLater": "Please, Try again Later!",
        "noFilesSelected": "No files Selcted!",
        "fileSelcted": "File Selected Successfully!",
        "notValidPhoneNumber": "Please, Enter your phone number!",
        "notValidCity": "Please, Select your city!",
        "notValidGender": "Please, Select you gender!"
    },
    "ar": {
        "notValidUsername": "أدخل البريد الإلكتروني الخاص بك",
        "notValidEmail": "أدخل بريد إلكتروني صحيح",
        "notValidPassword": "أدخل كلمة مرور صحيح",
        "loading": "جاري التحميل",
        "userNotFound": "لا يوجد مستخدمين بنفس البيانات، ربما ترغب في تسجيل الإشتراك",
        "passwordMissmatched": "كلمة المرور غير صحيحة",
        "repasswordNotMatched": "كلمتي المرور غير متوافقين",
        "fieldEmpty": "هذا الحقل لا يجب أن يكون فارغاً",
        "tryAgainLater": "أعد المحاولة في وقت لاحق",
        "notValidPhoneNumber": "أدخل رقم هاتف صحيح!",
        "notValidCity": "اختر مدينتك!",
        "notValidGender": "اختر النوع!"
    }
}