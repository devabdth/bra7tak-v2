const closeCategoryFromDialog= ()=> {
	document.getElementById('overlay').style.display= "none";
	document.getElementById('category-form-dialog').style.display= "none";

	const iconAssetContainer= document.getElementById('icon-asset-container');
	iconAssetContainer.removeChild(iconAssetContainer.lastElementChild);
	const coverAssetContainer= document.getElementById('cover-asset-container');
	coverAssetContainer.removeChild(coverAssetContainer.lastElementChild);

	const subcatsContainer= document.getElementById('sub-categories');

	let child= subcatsContainer.lastElementChild;
	while(child) {
		subcatsContainer.removeChild(child);
		child= subcatsContainer.lastElementChild;
	}


}

let cover, icon;

const openCategoryFormDialog= (mode, category)=> {
	const enNameField= document.getElementById('en-name-field');
	const enNameFieldContainer= document.getElementById('en-name-field-container');

	const arNameField= document.getElementById('ar-name-field');
	const arNameFieldContainer= document.getElementById('ar-name-field-container');

	const enDescField= document.getElementById('en-desc-field');
	const enDescFieldContainer= document.getElementById('en-desc-field-container');

	const arDescField= document.getElementById('ar-desc-field');
	const arDescFieldContainer= document.getElementById('ar-desc-field-container');

	const iconAssetContainer= document.getElementById('icon-asset-container');
	const coverAssetContainer= document.getElementById('cover-asset-container');

	const subCategoryFieldContainer= document.getElementById('sub-category-field-container');
	const enSubCategoryField= document.getElementById('en-sub-category-field');
	const arSubCategoryField= document.getElementById('ar-sub-category-field');

	const subcatsContainer= document.getElementById('sub-categories');
	const subcatsAdd= document.getElementById('add-sub-cat');


	if (mode == 0) {
		document.getElementById('delete-category').onclick=()=> {
			deleteCategory(category);
		}
		enNameField.value= category['name']['en'];
		arNameField.value= category['name']['ar'];
		enDescField.value= category['bio']['en'];
		arDescField.value= category['bio']['ar'];

		const iconEle= document.createElement('img'), coverEle= document.createElement('img');
		iconEle.setAttribute('src', `/assets/categories/icons/${category['id']}`);
		coverEle.setAttribute('src', `/assets/categories/covers/${category['id']}`);
		iconAssetContainer.appendChild(iconEle);
		iconAssetContainer.ondblclick= ()=> {
			const input = document.createElement("input");
			input.setAttribute("type", "file");
			input.setAttribute("accept", "image/*");
			input.onchange = e => {
				if (e.target.files.length === 0) {
					return;
				}
				const file_= e.target.files[0]
				const reader= new FileReader();
				reader.onload= ()=> {
					const assetDiv= document.createElement('img');
					assetDiv.className= "asset-card";
					assetDiv.id= file_.name;
					assetDiv.setAttribute('src', reader.result);
					assetDiv.style.objectFit= "contain";
					icon = file_;
					iconAssetContainer.removeChild(iconAssetContainer.lastElementChild);
					iconAssetContainer.appendChild(assetDiv);
				}
				reader.readAsDataURL(file_)
			}

			input.click();
		}

		coverAssetContainer.appendChild(coverEle);
		coverAssetContainer.ondblclick= ()=> {
			const input = document.createElement("input");
			input.setAttribute("type", "file");
			input.setAttribute("accept", "image/*");
			input.onchange = e => {
				if (e.target.files.length === 0) {
					return;
				}
				const file_= e.target.files[0]
				const reader= new FileReader();
				reader.onload= ()=> {
					const assetDiv= document.createElement('img');
					assetDiv.className= "asset-card";
					assetDiv.id= file_.name;
					assetDiv.setAttribute('src', reader.result);
					assetDiv.style.objectFit= "contain";
					cover = file_;
					coverAssetContainer.removeChild(coverAssetContainer.lastElementChild);
					coverAssetContainer.appendChild(assetDiv);
				}
				reader.readAsDataURL(file_)
			}

			input.click();

		}

		for (subCat_ in category['subcats']) {
			const subCat= category['subcats'][subCat_]
			const e= document.createElement('div');
			e.classList.add('sub-category-node');
			const p= document.createElement('p');
			console.log(subCat)
			p.innerHTML= `${subCat['name']['en']} (${subCat['name']['ar']})`;
			const deleteBtn= document.createElement('div');
			deleteBtn.innerHTML= "x";
			deleteBtn.style.cursor= "pointer";
			deleteBtn.onclick= ()=>{
				category['subcats'].splice(category['subcats'][subCat_], 1);
				subcatsContainer.removeChild(e);
			}
			e.appendChild(p)
			e.appendChild(deleteBtn)
			subcatsContainer.appendChild(e)
		}
		subcatsAdd.onclick= ()=> {
			if (enSubCategoryField.value.length > 2 && arSubCategoryField.value.length > 2) {
				category['subcats'].push({
					'name': {
						'en': enSubCategoryField.value.trim(),
						'ar': arSubCategoryField.value.trim(),
					},
					"bio": null,
				});
				enSubCategoryField.value= "";
				arSubCategoryField.value= "";
				let child= subcatsContainer.lastElementChild;
				while(child) {
					subcatsContainer.removeChild(child);
					child= subcatsContainer.lastElementChild;
				}

				for (subCat_ in category['subcats']) {
					const subCat= category['subcats'][subCat_]
					const e= document.createElement('div');
					e.classList.add('sub-category-node');
					const p= document.createElement('p');
					p.innerHTML= `${subCat['name']['en']} (${subCat['name']['ar']})`;
					const deleteBtn= document.createElement('div');
					deleteBtn.innerHTML= "x";
					deleteBtn.style.cursor= "pointer";
					deleteBtn.onclick= ()=>{
						category['subcats'].splice(category['subcats'][subCat_], 1);
						subcatsContainer.removeChild(e);
					}
					e.appendChild(p)
					e.appendChild(deleteBtn)
					subcatsContainer.appendChild(e)
				}


				subCategoryFieldContainer.style.border= "none";
				return;
			}
			subCategoryFieldContainer.style.border= "1px red solid";

		}
		const confirmationBtn= document.getElementById('edit-category-confirmation');
		confirmationBtn.onclick= ()=> {
			confrimEdit(mode, category);
		}

		
	} else if (mode === 1) {
		category= {
			name: {
				en: '',
				ar: '',
			},
			bio: {
				en: '',
				ar: '',
			},
			subcats: []
		};
		const iconEle= document.createElement('div'), coverEle= document.createElement('div');
		iconEle.innerHTML= "+";
		coverEle.innerHTML= "+";
		iconEle.style.cursor= "pointer";
		coverEle.style.cursor= "pointer";
		iconAssetContainer.appendChild(iconEle);
		iconAssetContainer.ondblclick= ()=> {
			const input = document.createElement("input");
			input.setAttribute("type", "file");
			input.setAttribute("accept", "image/*");
			input.onchange = e => {
				if (e.target.files.length === 0) {
					return;
				}
				const file_= e.target.files[0]
				const reader= new FileReader();
				reader.onload= ()=> {
					const assetDiv= document.createElement('img');
					assetDiv.className= "asset-card";
					assetDiv.id= file_.name;
					assetDiv.setAttribute('src', reader.result);
					assetDiv.style.objectFit= "contain";
					icon = file_;
					iconAssetContainer.removeChild(iconAssetContainer.lastElementChild);
					iconAssetContainer.appendChild(assetDiv);
				}
				reader.readAsDataURL(file_)
			}

			input.click();
		}

		coverAssetContainer.appendChild(coverEle);
		coverAssetContainer.ondblclick= ()=> {
			const input = document.createElement("input");
			input.setAttribute("type", "file");
			input.setAttribute("accept", "image/*");
			input.onchange = e => {
				if (e.target.files.length === 0) {
					return;
				}
				const file_= e.target.files[0]
				const reader= new FileReader();
				reader.onload= ()=> {
					const assetDiv= document.createElement('img');
					assetDiv.className= "asset-card";
					assetDiv.id= file_.name;
					assetDiv.setAttribute('src', reader.result);
					assetDiv.style.objectFit= "contain";
					cover = file_;
					coverAssetContainer.removeChild(coverAssetContainer.lastElementChild);
					coverAssetContainer.appendChild(assetDiv);
				}
				reader.readAsDataURL(file_)
			}

			input.click();

		}

		subcatsAdd.onclick= ()=> {
			if (enSubCategoryField.value.length > 2 && arSubCategoryField.value.length > 2) {
				category['subcats'].push({
					'name': {
						'en': enSubCategoryField.value.trim(),
						'ar': arSubCategoryField.value.trim(),
					},
					"bio": null,
				});
				enSubCategoryField.value= "";
				arSubCategoryField.value= "";
				let child= subcatsContainer.lastElementChild;
				while(child) {
					subcatsContainer.removeChild(child);
					child= subcatsContainer.lastElementChild;
				}

				for (subCat_ in category['subcats']) {
					const subCat= category['subcats'][subCat_]
					const e= document.createElement('div');
					e.classList.add('sub-category-node');
					const p= document.createElement('p');
					p.innerHTML= `${subCat['name']['en']} (${subCat['name']['ar']})`;
					const deleteBtn= document.createElement('div');
					deleteBtn.innerHTML= "x";
					deleteBtn.style.cursor= "pointer";
					deleteBtn.onclick= ()=>{
						category['subcats'].splice(category['subcats'][subCat_], 1);
						subcatsContainer.removeChild(e);
					}
					e.appendChild(p)
					e.appendChild(deleteBtn)
					subcatsContainer.appendChild(e)
				}


				subCategoryFieldContainer.style.border= "none";
				return;
			}
			subCategoryFieldContainer.style.border= "1px red solid";

		}

		const confirmationBtn= document.getElementById('edit-category-confirmation');
		confirmationBtn.onclick= ()=> {
			confirmCreate(mode, category);
		}
	}

	document.getElementById('overlay').style.display= "flex";
	document.getElementById('category-form-dialog').style.display= "flex";
}

const confirmCreate= async(mode, category) => {
	const confirmationBtn= document.getElementById('edit-category-confirmation');
	if (formValidation(1)) {
		try {
			const enNameField= document.getElementById('en-name-field');
			const arNameField= document.getElementById('ar-name-field');
			const enDescField= document.getElementById('en-desc-field');
			const arDescField= document.getElementById('ar-desc-field');
			category['name']= {
				'en': enNameField.value.trim(),
				'ar': arNameField.value.trim(),
			}
			category['bio']= {
				'en': enDescField.value.trim(),
				'ar': arDescField.value.trim(),
			}

			const pxhr= new XMLHttpRequest();
			const formData= new FormData();
			formData.append('category', JSON.stringify(category));
			formData.append('icon', icon);
			formData.append('cover', cover);

			pxhr.onload= ()=> {
				if(pxhr.status === 201) {
					window.open('./', '_self');
					return;
				}
				confirmationBtn.innerHTML= "Failed!";
				confirmationBtn.onclick= ()=> {};
				setTimeout(()=> {
					confirmationBtn.innerHTML= "Submit";
					confirmationBtn.onclick= ()=> {
						confrimEdit(mode, category);
					}
				}, 3000);		
			}

			pxhr.open('POST',`./?cid=${category['id']}`);
			pxhr.send(formData)

		} catch (e) {
			console.log(e);
			confirmationBtn.innerHTML= "Failed!";
			confirmationBtn.onclick= ()=> {};
			setTimeout(()=> {
				confirmationBtn.innerHTML= "Submit";
				confirmationBtn.onclick= ()=> {
					confirmCreate(mode, category);
				}
			}, 3000);		
		}
		return;

	}
	confirmationBtn.innerHTML= "Missing Data!";
	confirmationBtn.onclick= ()=> {};
	setTimeout(()=> {
		confirmationBtn.innerHTML= "Submit";
		confirmationBtn.onclick= ()=> {
			confirmCreate(mode, category);
		}
	}, 3000);	
}

const deleteCategory= async (category)=> {
	try {
		const res= await fetch(
			`./?cid=${category['id']}`, {
				method: "DELETE"
			}
		);

		if (res.status === 200) {
			window.open('./', '_self');
			return;
		}
		document.getElementById('delete-category').innerHTML= "Failed!"
		document.getElementById('delete-category').onclick= ()=> {}
		setTimeout(()=> {
			document.getElementById('delete-category').innerHTML= "Delete";
			document.getElementById('delete-category').onclick= ()=> {
				deleteCategory(category);
			}

		}, 3000);

	} catch (e) {
		console.log(e);
		document.getElementById('delete-category').innerHTML= "Failed!"
		document.getElementById('delete-category').onclick= ()=> {}
		setTimeout(()=> {
			document.getElementById('delete-category').innerHTML= "Delete";
			document.getElementById('delete-category').onclick= ()=> {
				deleteCategory(category);
			}

		}, 3000);

	}
}

const confrimEdit= async (mode, category)=> {
	const confirmationBtn= document.getElementById('edit-category-confirmation');
	if (formValidation(0)) {
		try {
			const enNameField= document.getElementById('en-name-field');
			const arNameField= document.getElementById('ar-name-field');
			const enDescField= document.getElementById('en-desc-field');
			const arDescField= document.getElementById('ar-desc-field');
			category['name']= {
				'en': enNameField.value.trim(),
				'ar': arNameField.value.trim(),
			}
			category['bio']= {
				'en': enDescField.value.trim(),
				'ar': arDescField.value.trim(),
			}

			const xhr= new XMLHttpRequest();
			const formData= new FormData();
			formData.append('category', JSON.stringify(category));
			console.log(icon);
			console.log(cover);
			if (icon !== undefined) {
				formData.append('icon', icon);
			}
			if (cover !== undefined) {
				formData.append('cover', cover);
			}

			xhr.onload= ()=> {
				if(xhr.status === 200) {
					window.open('./', '_self');
					return;
				}
				confirmationBtn.innerHTML= "Failed!";
				confirmationBtn.onclick= ()=> {};
				setTimeout(()=> {
					confirmationBtn.innerHTML= "Submit";
					confirmationBtn.onclick= ()=> {
						confrimEdit(mode, category);
					}
				}, 3000);		
			}

			xhr.open('PATCH',`./?cid=${category['id']}`);
			xhr.send(formData)

		} catch (e) {
			console.log(e);
			confirmationBtn.innerHTML= "Failed!";
			confirmationBtn.onclick= ()=> {};
			setTimeout(()=> {
				confirmationBtn.innerHTML= "Submit";
				confirmationBtn.onclick= ()=> {
					confrimEdit(mode, category);
				}
			}, 3000);		
		}
		return;

	}
	confirmationBtn.innerHTML= "Missing Data!";
	confirmationBtn.onclick= ()=> {};
	setTimeout(()=> {
		confirmationBtn.innerHTML= "Submit";
		confirmationBtn.onclick= ()=> {
			confrimEdit(mode, category);
		}
	}, 3000);
}


const formValidation= (mode)=> {
	const enNameField= document.getElementById('en-name-field');
	const enNameFieldContainer= document.getElementById('en-name-field-container');
	if(!enNameField.value) {
		enNameFieldContainer.style.border= "1px red solid";
		return false;
	}
	enNameFieldContainer.style.border= "none";

	const arNameField= document.getElementById('ar-name-field');
	const arNameFieldContainer= document.getElementById('ar-name-field-container');
	if(!arNameField.value) {
		arNameFieldContainer.style.border= "1px red solid";
		return false;
	}
	arNameFieldContainer.style.border= "none";

	const enDescField= document.getElementById('en-desc-field');
	const enDescFieldContainer= document.getElementById('en-desc-field-container');
	if(!enDescField.value) {
		enDescFieldContainer.style.border= "1px red solid";
		return false;
	}
	enDescFieldContainer.style.border= "none";

	const arDescField= document.getElementById('ar-desc-field');
	const arDescFieldContainer= document.getElementById('ar-desc-field-container');
	if(!arDescField.value) {
		arDescFieldContainer.style.border= "1px red solid";
		return false;
	}
	arDescFieldContainer.style.border= "none";

	const iconAssetContainer= document.getElementById('icon-asset-container');
	const coverAssetContainer= document.getElementById('cover-asset-container');
	if (mode === 1) {
		if (icon === undefined){
			iconAssetContainer.style.border= "1px red solid";
			return false;
		}
		iconAssetContainer.style.border= "none";

		if (cover=== undefined){
			coverAssetContainer.style.border= "1px red solid";
			return false;
		}
		coverAssetContainer.style.border= "none";
	}

	return true;
	
}