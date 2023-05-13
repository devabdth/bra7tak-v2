const pickFragment = (element) => {
    const activeSection = document.querySelector('.table-container.active');
    activeSection.classList.remove('active');

    const activeTab = document.querySelector('.fragment-controller.active');
    activeTab.classList.remove('active');

    element.classList.add('active');
    document.querySelector(`.table-container#${element.id}`).classList.add('active');
}
let selectedExpenseTab;

const selectExpenseTab = (element) => {
    if (element.classList.contains('active')) return;

    const activeTab = document.querySelector('.expense-tab.active');
    if (activeTab) activeTab.classList.remove('active');

    selectedExpenseTab = element.id;
    element.classList.add('active');
}


const closeAddEntryDialog = () => {
    document.querySelector('#add-entry-dialog').style.display = 'none';
    document.querySelector('#add-entry-dialog-overlay').style.display = 'none';
}

const openEntryDialog = () => {
    document.querySelector('#add-entry-dialog').style.display = 'flex';
    document.querySelector('#add-entry-dialog-overlay').style.display = 'flex';
}

const addEntryDialogConfirmation = async () => {
    const statusMsg = document.querySelector('#add-entry-dialog #status-msg');
    const amountField = document.querySelector('#add-entry-dialog input.single-line-field');
    const directionField = document.querySelector('#add-entry-dialog input#direction');
    if (!(Number.parseInt(amountField.value.trim()))) {
        statusMsg.innerHTML = 'Add Expense amount!';
        return;
    }
    statusMsg.innerHTML = '';

    if (!selectedExpenseTab) {
        statusMsg.innerHTML = 'Select Expense Direction';
        return;
    }
    statusMsg.innerHTML = 'Loading...';

    try {
        document.querySelector('#add-entry-dialog .main-button').style.pointerEvents = 'none';
        document.querySelector('#add-entry-dialog .shadow-button').style.pointerEvents = 'none';
        const res = await fetch(
            './enteries/', {
            method: 'POST',
            body: JSON.stringify({
                amount: Number.parseInt(amountField.value.trim()),
                direction: directionField.value.trim().length == 0 ? selectedExpenseTab.charAt(0).toUpperCase() + selectedExpenseTab.slice(1) : `${selectedExpenseTab.charAt(0).toUpperCase() + selectedExpenseTab.slice(1)}: (${directionField.value.trim()})`,
            })
        });

        if (res.status === 201) {
            window.open('./', '_self');
            return;
        }

        document.querySelector('#add-entry-dialog .main-button').style.pointerEvents = 'all';
        document.querySelector('#add-entry-dialog .shadow-button').style.pointerEvents = 'all';
        statusMsg.innerHTML = 'Failed, Try again later!';
    } catch (error) {
        document.querySelector('#add-entry-dialog .main-button').style.pointerEvents = 'all';
        document.querySelector('#add-entry-dialog .shadow-button').style.pointerEvents = 'all';
        statusMsg.innerHTML = 'Failed, Try again later!';
    }
}