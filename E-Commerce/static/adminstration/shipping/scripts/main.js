let shippingOptions = {};


const initShippingOptions = (shippingOptions_) => {
    shippingOptions = shippingOptions_;
}

const openShippingOptionsDialog = () => {
    document.getElementById('shipping-options-dialog').style.display = 'flex';
    document.getElementById('shipping-options-dialog-overlay').style.display = 'flex';
}

const closeEditShippingOptionsDialog = () => {
    document.getElementById('shipping-options-dialog').style.display = 'none';
    document.getElementById('shipping-options-dialog-overlay').style.display = 'none';
}

const submitEditShippingOptions = async (cities) => {
    let payload = {}
    for (let i of cities) {
        const durationsField = document.getElementById(`${i}-options-del-days`);
        const feesField = document.getElementById(`${i}-options-shipping-fees`);
        payload[i] = {
            durations: Number.parseInt(durationsField.value.trim()),
            fees: Number.parseInt(feesField.value.trim()),
        }
    }

    const subButton = document.getElementById('options-submit');
    subButton.innerHTML = 'Loading...';
    subButton.onclick = () => { };

    try {
        const res = await fetch(
            `/webapp/adminstration/products/shippingOptions/`,
            {
                method: 'PATCH',
                body: JSON.stringify({ data: payload }),
                headers: {
                    'Content-Type': 'application/json'
                },

            }
        );
        if (res.status === 200) {
            window.open('./', '_self');
            return
        }

        subButton.innerHTML = 'Failed!';
        setTimeout(() => {
            subButton.innerHTML = 'Submit';
            subButton.onclick = () => { submitEditShippingOptions(cities); }
        }, 3000);
    } catch (error) {

    }
}

const closeDeleteDialog = () => {
    document.querySelector('div.dialog-overlay#delete-dialog-overlay').style.display = 'none';
    document.querySelector('div#delete-dialog').style.display = 'none';
}

const openDeleteDialog = (shpr) => {
    document.querySelector('div.dialog-overlay#delete-dialog-overlay').style.display = 'flex';
    document.querySelector('div#delete-dialog').style.display = 'flex';

    document.querySelector('div.dialog#delete-dialog p#msg').innerHTML = `Are you sure, you want to delete <span>(${shpr['name']})</span>?`

    const cancel = document.querySelector('div.dialog#delete-dialog button.shadow-button');
    cancel.onclick = closeDeleteDialog;

    const confirm = document.querySelector('div.dialog#delete-dialog button.main-button');
    confirm.onclick = async () => {
        cancel.style.pointerEvents = 'none';
        confirm.style.pointerEvents = 'none';
        confirm.innerHTML = 'Loading...';
        try {
            const res = await fetch(`./?shprid=${shpr.id}`, {
                method: 'DELETE'
            });

            if (res.status === 200) {
                window.open('./', '_self');
                return;
            }
            confirm.innerHTML = 'Failed';
            setTimeout(() => {
                confirm.innerHTML = 'Confirm';
                confirm.style.pointerEvents = 'all';
                cancel.style.pointerEvents = 'all'
            }, 3000);
        } catch (e) {
            console.log(e);
            confirm.innerHTML = 'Failed';
            setTimeout(() => {
                confirm.innerHTML = 'Confirm';
                confirm.style.pointerEvents = 'all';
                cancel.style.pointerEvents = 'all'
            }, 3000);
        }

    };
}

const openShippingProviderForm = (mode, props) => {
    const nameField = document.querySelector('div.dialog#form-dialog #name-field');
    const nameFieldContainer = document.querySelector('div.dialog#form-dialog #name-conteiner');
    const msg = document.querySelector('div.dialog#form-dialog #msg');
    const payload = {
        fees: {}, del_days: {},
    }

    const confirm = document.querySelector('div.dialog#form-dialog button.main-button');
    const cancel = document.querySelector('div.dialog#form-dialog button.shadow-button');

    switch (mode) {
        default:
        case 'CREATE':
            confirm.onclick = async () => {
                if (nameField.value.trim().length < 8) {
                    nameFieldContainer.style.border = '2px red solid';
                    msg.innerHTML = 'Enter valid name!';
                    return;
                }
                nameFieldContainer.style.border = 'none';
                msg.innerHTML = '';
                for (let i of props.cities) {
                    let durationsField = document.getElementById(`${i}-form-del-days`);
                    let feesField = document.getElementById(`${i}-form-shipping-fees`);
                    payload.fees[i] = Number.parseInt(feesField.value.trim());
                    payload.del_days[i] = Number.parseInt(durationsField.value.trim());
                }
                payload.name = nameField.value.trim();
                try {
                    confirm.style.pointerEvents = 'none';
                    cancel.style.pointerEvents = 'none';
                    msg.innerHTML = 'Loading...';
                    const res = await fetch(
                        './', {
                        method: 'POST',
                        body: JSON.stringify(payload),
                        headers: {
                            'Content-Type': 'application/json'
                        }
                    }
                    );

                    if (res.status == 201) {
                        window.open('./', '_self');
                        return;
                    }

                    confirm.innerHTML = 'Failed';
                    msg.innerHTML = 'Try again later!';
                    setTimeout(() => {
                        confirm.innerHTML = 'Confirm'
                        msg.innerHTML = '';
                        confirm.style.pointerEvents = 'all';
                        cancel.style.pointerEvents = 'none';
                    })

                } catch (error) {
                    console.log(error);
                    confirm.innerHTML = 'Failed';
                    msg.innerHTML = 'Try again later!';
                    setTimeout(() => {
                        confirm.innerHTML = 'Confirm'
                        msg.innerHTML = '';
                        confirm.style.pointerEvents = 'all';
                        cancel.style.pointerEvents = 'none';
                    });
                }

            }
            break;
        case 'UPDATE':
            nameField.value = props.shpr.name;
            for (let i of props.cities) {
                let durationsField = document.getElementById(`${i}-form-del-days`);
                durationsField.value = props.shpr.del_days[i];
                let feesField = document.getElementById(`${i}-form-shipping-fees`);
                feesField.value = props.shpr.fees[i];
            }

            confirm.onclick = async () => {
                if (nameField.value.trim().length < 8) {
                    nameFieldContainer.style.border = '2px red solid';
                    msg.innerHTML = 'Enter valid name!';
                    return;
                }
                nameFieldContainer.style.border = 'none';
                msg.innerHTML = '';
                for (let i of props.cities) {
                    let durationsField = document.getElementById(`${i}-form-del-days`);
                    let feesField = document.getElementById(`${i}-form-shipping-fees`);
                    props.shpr.fees[i] = Number.parseInt(feesField.value.trim());
                    props.shpr.del_days[i] = Number.parseInt(durationsField.value.trim());
                }
                props.shpr.name = nameField.value.trim();
                try {
                    confirm.style.pointerEvents = 'none';
                    cancel.style.pointerEvents = 'none';
                    msg.innerHTML = 'Loading...';
                    const res = await fetch(
                        `./?shprId=${props.shpr.id}`, {
                        method: 'PATCH',
                        body: JSON.stringify(props.shpr),
                        headers: {
                            'Content-Type': 'application/json'
                        }
                    }
                    );

                    if (res.status == 200) {
                        window.open('./', '_self');
                        return;
                    }

                    confirm.innerHTML = 'Failed';
                    msg.innerHTML = 'Try again later!';
                    setTimeout(() => {
                        confirm.innerHTML = 'Confirm'
                        msg.innerHTML = '';
                        confirm.style.pointerEvents = 'all';
                        cancel.style.pointerEvents = 'none';
                    })

                } catch (error) {
                    console.log(error);
                    confirm.innerHTML = 'Failed';
                    msg.innerHTML = 'Try again later!';
                    setTimeout(() => {
                        confirm.innerHTML = 'Confirm'
                        msg.innerHTML = '';
                        confirm.style.pointerEvents = 'all';
                        cancel.style.pointerEvents = 'none';
                    });
                }

            }
            break;
    }
    document.querySelector('div.dialog#form-dialog').style.display = 'flex';
    document.querySelector('div.dialog-overlay#form-dialog-overlay').style.display = 'flex';

}

const closeShippingProviderForm = (cities) => {
    for (let i of cities) {
        let durationsField = document.getElementById(`${i}-form-del-days`);
        durationsField.value = '0';
        let feesField = document.getElementById(`${i}-form-shipping-fees`);
        feesField.value = '0';
    }
    document.querySelector('div.dialog#form-dialog').style.display = 'none';
    document.querySelector('div.dialog-overlay#form-dialog-overlay').style.display = 'none';
}