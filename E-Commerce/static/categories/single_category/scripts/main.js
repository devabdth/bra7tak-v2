let subCats = [];
const initSubCategoriesCheckboxed = (subCatsIds) => {
	subCats = subCatsIds.map((subCatId) => {
		return document.getElementById(`${subCatId}-checkbox`)
	});
}

const initWithParams = (params) => {
	if (!params) {
		return;
	}

	if (params.token) {
		const tokenField = document.getElementById('token-field');
		tokenField.value = `${params.token}`;
	}

	if (params.minPrice) {
		const minPriceField = document.getElementById('min-price-field');
		minPriceField.value = `${params.minPrice}`;
	}

	if (params.maxPrice) {
		const maxPriceField = document.getElementById('max-price-field');
		maxPriceField.value = `${params.maxPrice}`;
	}

	if (params.subcat) {
		const subCats_ = params.subcat.split(',');
		for (subCat in subCats_) {
			if (subCat.trim() !== '') {
				document.getElementById(`${subCats_[subCat]}-checkbox`).checked = true;
			}
		}

	}

}


const filter = () => {
	const tokenField = document.getElementById('token-field');
	const minPriceField = document.getElementById('min-price-field');
	const maxPriceField = document.getElementById('max-price-field');

	const token = tokenField.value.trim();
	const minPrice = Number.parseInt(minPriceField.value.trim());
	const maxPrice = Number.parseInt(maxPriceField.value.trim());

	const selectedSubCats = [];
	for (let subcat in subCats) {
		if (subCats[subcat].checked) {
			selectedSubCats.push(subCats[subcat].id.split('-')[0]);
		}
	}

	const url = window.location.href.split('?')[0];
	let tokenPart, minPricePart, maxPricePart, selectedSubCatsPart;
	if (!(token.trim().length === '')) {
		tokenPart = `token=${token}&`;
	}

	if (minPrice) {
		minPricePart = `minPrice=${minPrice}&`;
	}

	if (maxPrice) {
		maxPricePart = `maxPrice=${maxPrice}&`;
	}

	if (selectedSubCats.length !== 0) {
		selectedSubCatsPart = `subcat=${selectedSubCats.toString()}&`;
	}
	console.log({
		token: tokenPart || '',
		minPrice: minPrice,
		maxPrice: maxPrice,
		subCats: selectedSubCats,
	})

	let newUrl = `${url}?${tokenPart || ''}${minPricePart || ''}${maxPricePart || ''}${selectedSubCatsPart || ''}`;
	window.open(newUrl, '_self');
}


const filterClear = () => {
	window.open(window.location.href.split('?')[0], '_self');
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
	filterPanel.style.top = '-101%';
	filterPanelOverlay.style.top = '-101%';
}