let cats= [];
const initCategoriesCheckboxes= (catIds)=> {
	cats = catIds.map((catId)=> {
		return document.getElementById(`${catId}-checkbox`)
	});
}

const initWithParams= (params)=> {
	if (!params) {
		return;
	}

	if(params.token) {
		const tokenField= document.getElementById('token-field');
		tokenField.value = `${params.token}`;
	}

	if(params.minPrice) {
		const minPriceField= document.getElementById('min-price-field');
		minPriceField.value = `${params.minPrice}`;
	}

	if(params.maxPrice) {
		const maxPriceField= document.getElementById('max-price-field');
		maxPriceField.value = `${params.maxPrice}`;
	}

	if (params.cats){
		const cats_= params.cats.split(',');
		for(cat in cats_){
			if(cat.trim() !== ''){
			 	document.getElementById(`${cats_[cat]}-checkbox`).checked= true;
			}
		}

	}

}


const filter= ()=> {
	const tokenField= document.getElementById('token-field');
	const minPriceField= document.getElementById('min-price-field');
	const maxPriceField= document.getElementById('max-price-field');

	const token= tokenField.value.trim();
	const minPrice= Number.parseInt(minPriceField.value.trim());
	const maxPrice= Number.parseInt(maxPriceField.value.trim());

	const selectedCats= [];
	for(let cat in cats) {
		if(cats[cat].checked){
			selectedCats.push(cats[cat].id.split('-')[0]);
		}
	}

	const url= window.location.href.split('?')[0];
	let tokenPart, minPricePart, maxPricePart, selectedCatsPart;
	if(!(token.trim().length === '')) {
		tokenPart= `token=${token}&`;
	}
	
	if(minPrice) {
		minPricePart= `minPrice=${minPrice}&`;
	}
	
	if(maxPrice) {
		maxPricePart= `maxPrice=${maxPrice}&`;
	}

	if(selectedCats.length !== 0){
		selectedCatsPart= `cats=${selectedCats.toString()}&`;
	}

	let newUrl=	`${url}?${tokenPart || ''}${minPricePart || ''}${maxPricePart || ''}${selectedCatsPart || ''}`;
	window.open(newUrl, '_self');
}


const filterClear= ()=> {
	window.open(window.location.href.split('?')[0], '_self');
}