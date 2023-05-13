let currentModel, currentPosition;


const selectModelTab = (element) => {
    if (element.classList.contains('active')) return;

    const activeTab = document.querySelector('.model-tab.active');
    if (activeTab) activeTab.classList.remove('active');

    currentModel = element.id;
    element.classList.add('active');
}

const toggleJobsDropdown = () => {
    document.getElementById(`jobs-dropdown`).classList.toggle("show");
}

const jobsFilter = () => {
    var input, filter, ul, li, a, i;
    input = document.getElementById("job-search");
    filter = input.value.toUpperCase();
    div = document.getElementById("jobs-dropdown");
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


const chooseJob = (jobText, jobId, lang) => {
    const btn = document.getElementById(`jobs-dropbtn`);
    currentPosition = jobId;
    console.log(jobId);
    btn.innerHTML = jobText;
    btn.innerText = jobText;
    btn.textContent = jobText;

    toggleJobsDropdown();
}


const createAgentSubmit = async () => {
    const nameFieldContainer = document.getElementById('name-field-container');
    const nameField = document.getElementById('name-field');

    const phoneFieldContainer = document.getElementById('phone-field-container');
    const phoneField = document.getElementById('phone-field');

    const emailFieldContainer = document.getElementById('email-field-container');
    const emailField = document.getElementById('email-field');

    const salaryFieldContainer = document.getElementById('salary-field-container');
    const salaryField = document.getElementById('salary-field');

    const statusMsg = document.getElementById('status');

    if (!currentPosition) {
        statusMsg.innerHTML = 'Select Position/Role first!';
        document.getElementById(`jobs-dropbtn`).style.border = '2px red solid';
        return;
    }
    statusMsg.innerHTML = '';
    document.getElementById(`jobs-dropbtn`).style.border = 'none';

    if (!currentModel) {
        statusMsg.innerHTML = 'Select Hiring Model first!';
        return;
    }
    statusMsg.innerHTML = '';

    if (salaryField.value.trim() < 8) {
        salaryFieldContainer.style.border = '2px red solid';
        statusMsg.innerHTML = 'Enter a valid Agent Salary!';
        return;
    }
    salaryFieldContainer.style.border = 'none';
    statusMsg.innerHTML = '';

    if (nameField.value.trim() < 8) {
        nameFieldContainer.style.border = '2px red solid';
        statusMsg.innerHTML = 'Enter a valid Agent Name!';
        return;
    }
    nameFieldContainer.style.border = 'none';
    statusMsg.innerHTML = '';

    if (emailField.value.trim() < 8) {
        emailFieldContainer.style.border = '2px red solid';
        statusMsg.innerHTML = 'Enter a valid Agent Email!';
        return;
    }
    emailFieldContainer.style.border = 'none';
    statusMsg.innerHTML = '';

    if (phoneField.value.trim() < 8) {
        phoneFieldContainer.style.border = '2px red solid';
        statusMsg.innerHTML = 'Enter a valid Agent Phone!';
        return;
    }
    phoneFieldContainer.style.border = 'none';



    statusMsg.innerHTML = 'Loading...';
    const submit = document.querySelector('#create-dialog #options .main-button');
    submit.style.pointerEvents = 'none';
    const cancel = document.querySelector('#create-dialog #options .shadow-button');
    cancel.style.pointerEvents = 'none';

    try {
        const res = await fetch(
            './', {
            method: 'POST',
            body: JSON.stringify({
                name: nameField.value.trim(),
                email: emailField.value.trim(),
                phone: phoneField.value.trim(),
                salary: Number.parseInt(salaryField.value.trim()),
                position: currentPosition,
                model: currentModel,
                bonuses: [],
                deciplines: [],
            }),
            headers: {
                'Content-Type': 'application/json'
            }
        }
        )

        if (res.status === 201) {
            window.open('./', '_self');
            return;
        }
        statusMsg.innerHTML = 'Failed!';
        setTimeout(() => {
            statusMsg.innerHTML = '';
            submit.style.pointerEvents = 'all';
            cancel.style.pointerEvents = 'all';
        }, 3000);
    } catch (e) {
        console.log(e);
        statusMsg.innerHTML = 'Failed!';
        submit.style.pointerEvents = 'all';
        cancel.style.pointerEvents = 'all';
    }

}

const closeCreateAgentDialog = () => {
    document.querySelector('div#create-dialog').style.display = 'none';
    document.querySelector('div#create-dialog-overlay').style.display = 'none';
}

const openCreateAgentDialog = () => {
    document.querySelector('div#create-dialog').style.display = 'flex';
    document.querySelector('div#create-dialog-overlay').style.display = 'flex';
}

const openKPIDialog = (mode, agent) => {
    document.querySelector('div#kpi-dialog-overlay').style.display = 'flex';
    document.querySelector('div#kpi-dialog').style.display = 'flex';

    const headerTitle = document.querySelector('div#kpi-dialog #header h3');
    const submit = document.querySelector('div#kpi-dialog #options .main-button');
    switch (mode) {
        case 'bonus':
            headerTitle.innerHTML = 'Bonus';
            submit.onclick = () => {
                bonusSubmit(agent);
            }
            break;
        case 'decipline':
            headerTitle.innerHTML = 'Decipline';
            submit.onclick = () => {
                deciplineSubmit(agent);
            }
            break;
    }
}

const bonusSubmit = async (agent) => {
    const amountFieldContainer = document.querySelector('div#kpi-dialog .field-container');
    const amountField = document.querySelector('div#kpi-dialog input');
    const submit = document.querySelector('div#kpi-dialog #options .main-button');
    const cancel = document.querySelector('div#kpi-dialog #options .shadow-button');
    const statusMsg = document.querySelector('div#kpi-dialog #options #status-msg');

    try {
        if (amountField.value.trim() == 0) {
            amountFieldContainer.style.border = '2px red solid';
            statusMsg.innerHTML = 'Enter a valid amount!';
            return;
        }
        amountFieldContainer.style.border = 'none';
        statusMsg.innerHTML = 'Loading...';
        submit.style.pointerEvents = 'none';
        cancel.style.pointerEvents = 'none';
        console.log(agent);
        const res = await fetch(
            './', {
            method: 'PATCH',
            body: JSON.stringify({
                id: agent.id,
                amount: Number.parseInt(amountField.value.trim()),
                mode: 'bonus',
            }),
            headers: {
                'Content-Type': 'application/json'
            }
        });

        if (res.status === 200) {
            window.open('./', '_self');
            return;
        }

        statusMsg.innerHTML = 'Failed!';
        setTimeout(() => {
            statusMsg.innerHTML = '';
            submit.style.pointerEvents = 'all';
            cancel.style.pointerEvents = 'all';

        }, 3000);
        submit.style.pointerEvents = 'none';
        cancel.style.pointerEvents = 'none';

    } catch (e) {
        console.log(e)

    }
}

const deciplineSubmit = async (agent) => {
    const amountFieldContainer = document.querySelector('div#kpi-dialog .field-container');
    const amountField = document.querySelector('div#kpi-dialog input');
    const submit = document.querySelector('div#kpi-dialog #options .main-button');
    const cancel = document.querySelector('div#kpi-dialog #options .shadow-button');
    const statusMsg = document.querySelector('div#kpi-dialog #options #status-msg');

    try {
        if (amountField.value.trim() == 0) {
            amountFieldContainer.style.border = '2px red solid';
            statusMsg.innerHTML = 'Enter a valid amount!';
            return;
        }
        amountFieldContainer.style.border = 'none';
        statusMsg.innerHTML = 'Loading...';
        submit.style.pointerEvents = 'none';
        cancel.style.pointerEvents = 'none';

        const res = await fetch(
            './', {
            method: 'PATCH',
            body: JSON.stringify({
                id: agent.id,
                amount: Number.parseInt(amountField.value.trim()),
                mode: 'decipline',
            }),
            headers: {
                'Content-Type': 'application/json'
            }
        });

        if (res.status === 200) {
            window.open('./', '_self');
            return;
        }

        statusMsg.innerHTML = 'Failed!';
        setTimeout(() => {
            statusMsg.innerHTML = '';
            submit.style.pointerEvents = 'all';
            cancel.style.pointerEvents = 'all';

        }, 3000);
        submit.style.pointerEvents = 'none';
        cancel.style.pointerEvents = 'none';

    } catch (e) {
        console.log(e)

    }
}


const closeKPIDialog = () => {
    document.querySelector('div#kpi-dialog-overlay').style.display = 'none';
    document.querySelector('div#kpi-dialog').style.display = 'none';
}

const closeWithdrawDialog = (agentData) => {
    document.querySelector('div#withdraw-dialog').style.display = 'none';
    document.querySelector('div#withdraw-dialog-overlay').style.display = 'none';
}

const openWithdrawDialog = (agentData) => {
    document.querySelector('div#withdraw-dialog #body p').innerHTML = `The total Salary for ${agentData.name} is: ${(agentData.salary + agentData['bonuses'].reduce((a, b) => a + b, 0)) - agentData['deciplines'].reduce((a, b) => a + b, 0)} EGP`
    document.querySelector('div#withdraw-dialog  #options .main-button').onclick = () => {
        withdrawSalary(agentData);
    };
    document.querySelector('div#withdraw-dialog').style.display = 'flex';
    document.querySelector('div#withdraw-dialog-overlay').style.display = 'flex';
}

const withdrawSalary = async (agentData) => {
    const submit = document.querySelector('div#withdraw-dialog  #options .main-button');
    const clear = document.querySelector('div#withdraw-dialog  #options .shadow-button');
    const statusMsg = document.querySelector('div#withdraw-dialog  #options #status-msg');
    try {
        statusMsg.innerHTML = 'Loading...';
        submit.style.pointerEvents = 'none';
        clear.style.pointerEvents = 'none';

        const res = await fetch(
            `./withdraw/?id=${agentData['id']}`, {
            method: 'PATCH'
        });

        if (res.status === 200) {
            window.open('./', '_self');
            return;
        }

        statusMsg.innerHTML = 'Failed!';
        setTimeout(() => {
            statusMsg.innerHTML = '';
            submit.style.pointerEvents = 'all';
            clear.style.pointerEvents = 'all';
        }, 3000)

    } catch (e) {
        console.log(e);
        statusMsg.innerHTML = 'Failed!';
        setTimeout(() => {
            statusMsg.innerHTML = '';
            submit.style.pointerEvents = 'all';
            clear.style.pointerEvents = 'all';
        }, 3000);
    }
}