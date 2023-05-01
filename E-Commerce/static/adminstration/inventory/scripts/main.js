const colors = [
    'Red', 'Blue', 'Black', 'White', 'Pink', 'Violet', 'Orange', 'Brown',
    'Lavender', 'Dark Blue', 'Dark Cyan', 'Dark Green', 'Gold', 'Olive', 'Dark Olive Green',
    'Silver', 'Grey', 'Sky Blue', 'Saddle Brown', 'Maroon', 'Purple', 'Mint Cream', 'Fuchsia',
    'Beige', 'Antique White', 'Blue Violet', 'Indigo', 'Khaki', 'Light Blue', 'Light Green', 'Navy',
    'Snow', 'Spring Green',
];

const sizes = [
    'Small', 'Medium', 'X Large', 'XX Large', 'XXX Large', 'XXXX Large',
]
const requestFragment = (index) => {
    const depositController = document.querySelector('.fragment-controller#deposit-requests');
    const withdrawController = document.querySelector('.fragment-controller#withdraw-requests');
    const depositFragment = document.querySelector('.requests-fragment#deposit-requests');
    const withdrawFragment = document.querySelector('.requests-fragment#withdraw-requests');

    switch (index) {
        case 0:
        default:
            depositController.classList.add('active');
            depositFragment.classList.add('active');
            withdrawController.classList.remove('active');
            withdrawFragment.classList.remove('active');
            break;
        case 1:
            depositController.classList.remove('active');
            depositFragment.classList.remove('active');
            withdrawController.classList.add('active');
            withdrawFragment.classList.add('active');
            break;

    }
}

const toggleProductRow = (element) => {
    const collapse = element.childNodes[5];
    collapse.classList.toggle('active');
}

const closeAllDialogs = () => {
    const overlay = document.getElementById('overlay');
    const depositDialog = document.getElementById('deposit-dialog');
    const requestsDialog = document.getElementById('deposit-request-submission');
    overlay.style.display = 'none';
    depositDialog.style.display = 'none';
    requestsDialog.style.display = 'none';

}

const openDepositDialog = (product) => {
    const overlay = document.getElementById('overlay');
    const dialog = document.getElementById('deposit-dialog');
    const headerClose = document.getElementById('dialog-header-close-action');
    const inputFieldContainer = document.getElementById('quantity-field-container');
    const inputField = document.getElementById('quantity-field');
    const cancelOption = document.getElementById('dialog-options-cancel');
    const confirmOption = document.getElementById('dialog-options-confirm');
    const statusMsg = document.getElementById('status-msg');

    headerClose.onclick = closeAllDialogs;
    cancelOption.onclick = closeAllDialogs;

    confirmOption.onclick = async () => {
        if (!(deposittedItems.id)) {
            statusMsg.innerHTML = 'Please, Select Product first!';
            return;
        }

        if (!currentSelectedColor) {
            statusMsg.innerHTML = 'Please, Select Color first!';
            return;
        }

        if (!currentSelectedSize) {
            statusMsg.innerHTML = 'Please, Select Size first!';
            return;
        }

        if (inputField.value.trim() == '') {
            statusMsg.innerHTML = 'Please, Enter Deposit Amount!';
            inputFieldContainer.style.border = '2px red solid';
            return;
        }

        if (Number.parseInt(inputField.value.trim()) < 0 || Number.parseInt(inputField.value.trim) > 50) {
            statusMsg.innerHTML = 'You can Deposit 0 to 50 pieces only!';
            inputFieldContainer.style.border = '2px red solid';
            return;
        }
        inputFieldContainer.style.border = 'none';

        const payload = {
            color: currentSelectedColor,
            size: currentSelectedSize,
            quantity: Number.parseInt(inputField.value.trim()),
            productId: deposittedItems.id,
        }

        confirmOption.style.pointerEvents = 'none';
        cancelOption.style.pointerEvents = 'none';
        headerClose.style.pointerEvents = 'none';
        statusMsg.innerHTML = 'Loading...';

        try {
            const res = await fetch('./deposit/', {
                method: 'PATCH',
                body: JSON.stringify(payload),
                header: {
                    'Content-Type': 'application/json',
                }
            });

            if (res.status !== 200) {
                confirmOption.style.pointerEvents = 'all';
                cancelOption.style.pointerEvents = 'all';
                headerClose.style.pointerEvents = 'all';
                statusMsg.innerHTML = 'Please, Try again later!';
                return;
            }

            window.open('./', '_self');

        } catch (error) {
            console.log(error);
            confirmOption.style.pointerEvents = 'all';
            cancelOption.style.pointerEvents = 'all';
            headerClose.style.pointerEvents = 'all';
            statusMsg.innerHTML = 'Please, Try again later!';
        }
    }

    overlay.style.display = 'flex';
    dialog.style.display = 'flex';
}


let currentProduct;
const toggleProductsDropdown = () => {
    document.getElementById(`products-dropdown`).classList.toggle("show");
}

const productsFilter = () => {
    var input, filter, ul, li, a, i;
    input = document.getElementById("product-search");
    filter = input.value.toUpperCase();
    div = document.getElementById("products-dropdown");
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


const chooseDepositProduct = (productText, product, lang, wtoggle, callback) => {
    const btn = document.getElementById(`products-dropbtn`);
    currentProduct = product;
    btn.innerHTML = productText;
    btn.innerText = productText;
    btn.textContent = productText;

    showSizesnColorsSeciton(product);

    if (wtoggle ?? true) {
        toggleProductsDropdown();
    }
}
let currentSelectedColor, currentSelectedSize;
const deposittedItems = {}
const showSizesnColorsSeciton = (product) => {
    const titles = document.querySelectorAll('#deposit-dialog > #body h3');
    titles.forEach(element => {
        element.style.display = 'flex';

    });
    if (!product) return;
    const colorsSection = document.querySelector('div#deposit-dialog #colors-section')
    const sizesSection = document.querySelector('div#deposit-dialog #sizes-section')
    colorsSection.innerHTML = '';
    sizesSection.innerHTML = '';

    deposittedItems.id = product.id;

    for (let color of colors) {
        const colorDiv = document.createElement('div');
        colorDiv.classList.add('color-div');
        colorDiv.setAttribute('id', color);

        const title = document.createElement('p');
        title.innerHTML = color;

        const color_ = document.createElement('div');
        color_.style.backgroundColor = color.replace(' ', '').replace(' ', '').toLowerCase();
        color_.onclick = () => {
            if (currentSelectedColor) {
                document.getElementById(currentSelectedColor).classList.remove('active');
            }
            currentSelectedColor = color;
            colorDiv.classList.add('active');
        }

        colorDiv.appendChild(color_);
        colorDiv.appendChild(title);

        colorsSection.appendChild(colorDiv);
    }

    for (let size of sizes) {
        const sizeDiv = document.createElement('div');
        sizeDiv.classList.add('size-div');
        sizeDiv.setAttribute('id', size);
        sizeDiv.innerHTML = size;
        sizeDiv.onclick = () => {
            if (currentSelectedSize) {
                document.getElementById(currentSelectedSize).classList.remove('active');
            }
            currentSelectedSize = size;
            sizeDiv.classList.add('active');
        }
        sizesSection.appendChild(sizeDiv);
    }
}

const openRequestDialog = async (request, mode) => {
    const statusMsg = document.getElementById('request-dialog-status-msg');
    const dialog = document.getElementById('deposit-request-submission');
    const overlay = document.getElementById('overlay');

    const headerClose = document.getElementById('request-submission-header-close-action');
    headerClose.onclick = closeAllDialogs;

    const cancelOption = document.getElementById('request-dialog-options-cancel');
    cancelOption.onclick = closeAllDialogs;

    const confrimOption = document.getElementById('request-dialog-options-confirm');
    const dialogBody = document.querySelector('div#deposit-request-submission #body');

    const title = document.createElement('p');
    title.setAttribute('id', 'title');
    title.innerHTML = 'Are you sure you want to submit depositting back the following products is done successfully!';
    dialogBody.appendChild(title);
    for (let product of request.products) {
        const productRow = document.createElement('p');
        productRow.innerHTML = `${product.productName} <br>&nbsp;<span>Color:</span> ${product.color}&nbsp;&nbsp;&nbsp;<span>Size:</span> ${product.size}&nbsp;&nbsp;&nbsp;<span>Quantity:</span> ${product.quantity}<br>`

        dialogBody.appendChild(productRow);
    }

    confrimOption.onclick = async () => {
        statusMsg.innerHTML = 'Loading...';
        headerClose.style.pointerEvents = 'none';
        confrimOption.style.pointerEvents = 'none';
        cancelOption.style.pointerEvents = 'none';
        try {
            console.log(request)
            const res = await fetch(`/webapp/adminstration/inventory/requests/submission/${mode}/${request['rid']}/`, {
                method: 'PATCH',
            });

            if (res.status !== 200) {
                statusMsg.innerHTML = 'Failed, Try again later...';
                confrimOption.style.pointerEvents = 'all';
                headerClose.style.pointerEvents = 'all';
                cancelOption.style.pointerEvents = 'all';
                return;
            }
            window.open('./', '_self');

        } catch (error) {
            statusMsg.innerHTML = 'Failed, Try again later...';
            confrimOption.style.pointerEvents = 'all';
            headerClose.style.pointerEvents = 'all';
            cancelOption.style.pointerEvents = 'all';
        }
    }

    dialog.style.display = 'flex';
    overlay.style.display = 'flex';
}

const exportInventorySheet = async (product, element) => {
    element.onclick = () => { }
    element.innerHTML = 'Loading...';
    let res;
    if (product === 'all') {
        res = await fetch(`/webapp/adminstration/inventory/report/generalReport/`);
    } else {
        res = await fetch(`/webapp/adminstration/inventory/report/${product}`);
    }

    if (res.status === 200) {
        console.log(res);
        element.innerHTML = 'Successfull';
        setTimeout(() => {
            element.innerHTML = 'Export Sheet';
            element.onclick = () => {
                exportInventorySheet(product, element);
            }
        }, 3000);

        const blob = await res.blob();
        const newBlob = new Blob([blob]);

        const blobUrl = window.URL.createObjectURL(newBlob);

        const link = document.createElement('a');
        link.href = blobUrl;
        link.setAttribute('download', `${product == 'all' ? `General Report` : product}: ${new Date().toLocaleString()}.xlsx`);
        document.body.appendChild(link);
        link.click();
        link.parentNode.removeChild(link);

        // clean up Url
        window.URL.revokeObjectURL(blobUrl);

    } else {
        element.innerHTML = 'Failed';
        setTimeout(() => {
            element.innerHTML = 'Export Sheet';
            element.onclick = () => {
                exportInventorySheet(product, element);
            }
        }, 3000);

    }


}