let product;
const initializeProduct = (p) => {
    product = p;
}


let slideShowSlides;
const initializeSlideShow = (pid, listSource, baseUrl) => {
    const currentSlide = document.getElementById('current-slide');

    slideShowSlides = listSource.map(item => document.getElementById(`${pid}-${item}`));
    slideShowSlides.map(slide => {
        slide.onclick = () => {
            if (slide.classList.contains('active-slide')) {
                return;
            }

            slideShowSlides.map(slide_ => {
                slide_.classList.remove('active-slide');
            });

            slide.classList.add('active-slide');
            currentSlide.style.backgroundImage = `url(${baseUrl}/assets/products/name/${slide.id}/)`;
        }

    });
}

const formatPrice = (input) => {
    const formatter = new Intl.NumberFormat('en-US', {
        style: 'currency',
        currency: 'EGP'
    });
    return formatter.format(input.toString());
}

const increaseAmount = () => {
    const amountField = document.getElementById('amount-field');
    let amount = Number.parseInt(amountField.value.trim());
    const price = document.getElementById('price-tag');
    if (amount < 15) {
        amount = amount + 1;
        amountField.value = `${amount}`;
        switch (amount) {
            case 1:
                price.innerHTML = `${formatPrice(amount * product['pricing']['currentPrice'])}`;
                break;
            case 2:
            case 3:
                price.innerHTML = `${formatPrice(amount * product['pricing']['twoPiecesPrice'])}<span style="color: red;">${formatPrice(amount * product['pricing']['currentPrice'])}</span>`;
                break;
            case 4:
            case 5:
                price.innerHTML = `${formatPrice(amount * product['pricing']['fourPiecesPrice'])}<span style="color: red;">${formatPrice(amount * product['pricing']['currentPrice'])}</span>`;
                break;
            case 6:
            case 7:
            case 8:
            case 9:
            case 10:
            case 11:
                price.innerHTML = `${formatPrice(amount * product['pricing']['sixPiecesPrice'])}<span style="color: red;">${formatPrice(amount * product['pricing']['currentPrice'])}</span>`;
                break;
            case 12:
            case 13:
            case 14:
            case 15:
                price.innerHTML = `${formatPrice(amount * product['pricing']['dozinPiecesPrice'])}<span style="color: red;">${formatPrice(amount * product['pricing']['currentPrice'])}</span>`;
                break;
        }
    }
}

const decreaseAmount = () => {
    const amountField = document.getElementById('amount-field');
    let amount = Number.parseInt(amountField.value.trim());
    const price = document.getElementById('price-tag');
    if (amount > 1) {
        amount = amount - 1;
        amountField.value = `${amount}`;
        switch (amount) {
            case 1:
                price.innerHTML = `${formatPrice(amount * product['pricing']['currentPrice'])}`;
                break;
            case 2:
            case 3:
                price.innerHTML = `${formatPrice(amount * product['pricing']['twoPiecesPrice'])}<span style="color: red;">${formatPrice(amount * product['pricing']['currentPrice'])}</span>`;
                break;
            case 4:
            case 5:
                price.innerHTML = `${formatPrice(amount * product['pricing']['fourPiecesPrice'])}<span style="color: red;">${formatPrice(amount * product['pricing']['currentPrice'])}</span>`;
                break;
            case 6:
            case 7:
            case 8:
            case 9:
            case 10:
            case 11:
                price.innerHTML = `${formatPrice(amount * product['pricing']['sixPiecesPrice'])}<span style="color: red;">${formatPrice(amount * product['pricing']['currentPrice'])}</span>`;
                break;
            case 12:
            case 13:
            case 14:
            case 15:
                price.innerHTML = `${formatPrice(amount * product['pricing']['dozinPiecesPrice'])}<span style="color: red;">${formatPrice(amount * product['pricing']['currentPrice'])}</span>`;
                break;
        }

    }

}

const addToCartListener = (lang) => {
    const statusMsg = document.getElementById('status-msg');
    if (!currentSize) {
        statusMsg.innerHTML = lang == 'en' ? 'Please, Pick size first!' : 'من فضلك إختر المقاس أولاً';
        statusMsg.style.fontFamily = lang == 'en' ? 'Poppins' : 'Cairo';
        return;
    }

    if (!currentColor) {
        statusMsg.innerHTML = lang == 'en' ? 'Please, Pick color first!' : 'من فضلك إختر اللون أولاً';
        statusMsg.style.fontFamily = lang == 'en' ? 'Poppins' : 'Cairo';
        return;
    }
    const amountField = document.getElementById('amount-field');
    const amount = Number.parseInt(amountField.value.trim())

    const urlParts = window.location.href.split('/products/');
    const url = urlParts[0];
    const productId = urlParts[1].split('/')[0];

    addToCart(url, productId, amount, currentSize, currentColor);
}

const orderNowListener = (uid, url, productId, lang) => {
    const statusMsg = document.getElementById('status-msg');
    if (!currentSize) {
        statusMsg.innerHTML = lang == 'en' ? 'Please, Pick size first!' : 'من فضلك إختر المقاس أولاً';
        statusMsg.style.fontFamily = lang == 'en' ? 'Poppins' : 'Cairo';
        return;
    }

    if (!currentColor) {
        statusMsg.innerHTML = lang == 'en' ? 'Please, Pick color first!' : 'من فضلك إختر اللون أولاً';
        statusMsg.style.fontFamily = lang == 'en' ? 'Poppins' : 'Cairo';
        return;
    }

    const amountField = document.getElementById('amount-field');
    const count = Number.parseInt(amountField.value.trim());
    if (uid !== undefined) {
        addToCart(url, productId, count, currentSize, currentColor)
    }
    dryCheckout(url, [[productId, count, currentSize, currentColor]]);
}


const amountCustom = (count) => {
    const amountField = document.getElementById('amount-field');
    const price = document.getElementById('price-tag');
    amountField.value = `${count}`;
    switch (count) {
        case 1:
            price.innerHTML = `${formatPrice(count * product['pricing']['currentPrice'])}`;
            break;
        case 2:
        case 3:
            price.innerHTML = `${formatPrice(count * product['pricing']['twoPiecesPrice'])}<span style="color: red;">${formatPrice(count * product['pricing']['currentPrice'])}</span>`;
            break;
        case 4:
        case 5:
            price.innerHTML = `${formatPrice(count * product['pricing']['fourPiecesPrice'])}<span style="color: red;">${formatPrice(count * product['pricing']['currentPrice'])}</span>`;
            break;
        case 6:
        case 7:
        case 8:
        case 9:
        case 10:
        case 11:
            price.innerHTML = `${formatPrice(count * product['pricing']['sixPiecesPrice'])}<span style="color: red;">${formatPrice(count * product['pricing']['currentPrice'])}</span>`;
            break;
        case 12:
        case 13:
        case 14:
        case 15:
            price.innerHTML = `${formatPrice(count * product['pricing']['dozinPiecesPrice'])}<span style="color: red;">${formatPrice(count * product['pricing']['currentPrice'])}</span>`;
            break;

    }

}

let currentColor, currentSize;
const pickColor = (color) => {
    if (currentColor !== undefined) {
        document.getElementById(`${currentColor}-btn`).classList.remove('active');
    }
    currentColor = color;
    document.getElementById(`${color}-btn`).classList.add('active');
}

const pickSize = (size) => {
    if (currentSize !== undefined) {
        document.getElementById(`${currentSize}-btn`).classList.remove('active');
    }
    currentSize = size;
    document.getElementById(`${size}-btn`).classList.add('active');
}
