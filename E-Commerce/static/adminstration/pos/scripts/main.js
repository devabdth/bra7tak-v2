const pickFragment = (element) => {
    const activeSection = document.querySelector('.table-container.active');
    activeSection.classList.remove('active');

    const activeTab = document.querySelector('.fragment-controller.active');
    activeTab.classList.remove('active');

    element.classList.add('active');
    document.querySelector(`.table-container#${element.id}`).classList.add('active');

}