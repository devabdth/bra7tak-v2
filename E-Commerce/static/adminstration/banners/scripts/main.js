const closeBannerEditDialog= ()=> {
	document.getElementById('overlay').style.display= "none";
	document.getElementById('banner-edit-dialog').style.display= "none";

}

const openBannerEditDialog= async (mode, banner)=> {
	const enSubtitleField= document.getElementById('en-subtitle-field');
	const arSubtitleField= document.getElementById('ar-subtitle-field');
	const enTitleField= document.getElementById('en-title-field');	
	const arTitleField= document.getElementById('ar-title-field');	
	const oldField= document.getElementById('old-field');
	const newField= document.getElementById('new-field');	
	const enActionTextField= document.getElementById('en-action-text-field');
	const arActionTextField= document.getElementById('ar-action-text-field');
	const actionLinkField= document.getElementById('action-link-field');
	const cardActionLinkField= document.getElementById('card-action-link-field');		
	const backgroundColorField= document.getElementById('background-color-field');
	const subtitleColorField= document.getElementById('subtitle-color-field');
	const titleColorField= document.getElementById('title-color-field');
	const actionBackgroundColorField= document.getElementById('action-background-color-field');
	const actionTextColorField= document.getElementById('action-text-color-field');
	const assetContainer= document.getElementById('asset-container');

	if (mode === 0){
		let newAsset, newAssetFile;
		enSubtitleField.value= banner['subtitle']['en'] || "";
		enTitleField.value= banner['title']['en'] || "";
		arSubtitleField.value= banner['subtitle']['ar'] || "";
		arTitleField.value= banner['title']['ar'] || "";
		oldField.value= banner['pricing']['perviousPrice'] || "";
		newField.value= banner['pricing']['perviousPrice'] || "";
		enActionTextField.value= banner['action_text']['en'] || "";
		arActionTextField.value= banner['action_text']['ar'] || "";
		actionLinkField.value= banner['action_link'] || "";
		cardActionLinkField.value= banner['card_action_link']
		backgroundColorField.value= banner['background_color']
		subtitleColorField.value= banner['subtitle_color']
		titleColorField.value= banner['title_color']
		actionBackgroundColorField.value= banner['action_background_color']
		actionTextColorField.value= banner['action_text_color'];
		assetContainer.innerHTML= `
			<img src="/assets/banners/assets/${banner['id']}"/>
		`;
		if (banner['id'] === 'mainBanner' || banner['id'] === 'subBannerOne' || banner['id'] === 'subBannerTwo') {
			document.getElementById('delete-banner').style.display= "none";
			document.getElementById('delete-banner').onclick= ()=> {}
		} else {
			document.getElementById('delete-banner').onclick= ()=> {
				console.log('Deleted');
			}

		}

		document.getElementById('overlay').style.display= "flex";
		document.getElementById('banner-edit-dialog').style.display= "flex";
		assetContainer.ondblclick= ()=> {
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
					newAsset = file_.name;
					banner['aset'] = file_.name;
					newAssetFile= file_;
					assetContainer.removeChild(assetContainer.lastElementChild);
					assetContainer.appendChild(assetDiv);
				}
				reader.readAsDataURL(file_)
			}

			input.click();

		}
		document.getElementById('cancel-edit-banner').onclick= closeBannerEditDialog;
		document.getElementById('confirm-edit-banner').onclick= ()=> {
			if(formValidation()){
				const payload= {
					subtitle: {
						en: enSubtitleField.value.trim(),
						ar: arSubtitleField.value.trim(),
					},
					title: {
						en: enTitleField.value.trim(),
						ar: arTitleField.value.trim(),
					},
					old: oldField.value,
					new: newField.value,
					actionText: {
						en: enActionTextField.value.trim(),
						ar: arActionTextField.value.trim(),
					},
					actionLink: actionLinkField.value,
					cardActionLink: cardActionLinkField.value,
					backgroundColor: backgroundColorField.value,
					subtitleColor: subtitleColorField.value,
					titleColor: titleColorField.value,
					actionBackgroundColor: actionBackgroundColorField.value,
					actionTextColor: actionTextColorField.value,
				};
				confirmEditBanner(banner['id'], payload, newAsset, newAssetFile);
				return;
			}
			document.getElementById('confirm-edit-banner').innerHTML= "Missing Data!"
			setTimeout(()=> {
				document.getElementById('confirm-edit-banner').innerHTML= "Submit!"

			}, 2000);

		}
	}
	
}


const confirmEditBanner= async (bid, payload, newAsset, newAssetFile)=> {
	try {
		const req= new XMLHttpRequest();
		const reqData= new FormData();
		reqData.append('banner', JSON.stringify(payload));
		reqData.append("asset", newAssetFile);
		req.onload= ()=> {
			if(req.status === 200) {
				window.open('./', '_self');
				return;
			}

			document.getElementById('confirm-edit-banner').innerHTML= "Failed!";
			document.getElementById('confirm-edit-banner').onclick= ()=> {};
			setTimeout(()=> {
				document.getElementById('confirm-edit-banner').innerHTML= "Submit";
				document.getElementById('confirm-edit-banner').onclick= ()=> {
					confirmEditBanner(bid, payload);
				}
			}, 3000)
		}	

		req.open('PATCH',`./?bid=${bid}`);
		req.send(reqData)
		
	} catch(e) {
		console.log(e);

		document.getElementById('confirm-edit-banner').innerHTML= "Failed!";
		document.getElementById('confirm-edit-banner').onclick= ()=> {};
		setTimeout(()=> {
			document.getElementById('confirm-edit-banner').innerHTML= "Submit";
			document.getElementById('confirm-edit-banner').onclick= ()=> {
				confirmEditBanner(bid, payload);
			}
		}, 3000)
		
	}
}

const formValidation= ()=> {
	const enSubtitleField= document.getElementById('en-subtitle-field');
	const enSubtitleFieldContainer= document.getElementById('en-subtitle-field-container');
	if(!enSubtitleField.value) {
		enSubtitleFieldContainer.style.border= "1px red solid";
		return false;
	}
	enSubtitleFieldContainer.style.border= "none";

	const arSubtitleField= document.getElementById('ar-subtitle-field');
	const arSubtitleFieldContainer= document.getElementById('ar-subtitle-field-container');
	if(!arSubtitleField.value) {
		arSubtitleFieldContainer.style.border= "1px red solid";
		return false;
	}
	arSubtitleFieldContainer.style.border= "none";

	const enTitleField= document.getElementById('en-title-field');
	const enTitleFieldContainer= document.getElementById('en-title-field-container');
	if(!enTitleField.value) {
		enTitleFieldContainer.style.border= "1px red solid";
		return false;
	}
	enTitleFieldContainer.style.border= "none";

	const arTitleField= document.getElementById('ar-title-field');
	const arTitleFieldContainer= document.getElementById('ar-title-field-container');
	if(!arTitleField.value) {
		arTitleFieldContainer.style.border= "1px red solid";
		return false;
	}
	arTitleFieldContainer.style.border= "none";
	
	const oldField= document.getElementById('old-field');
	const oldFieldContainer= document.getElementById('old-field-container');

	const newField= document.getElementById('new-field');
	const newFieldContainer= document.getElementById('new-field-container');

	const enActionTextField= document.getElementById('en-action-text-field');
	const enActionTextFieldContainer= document.getElementById('en-action-text-field-container');
	const arActionTextField= document.getElementById('ar-action-text-field');
	const arActionTextFieldContainer= document.getElementById('ar-action-text-field-container');
	const actionLinkField= document.getElementById('action-link-field');
	const actionLinkFieldContainer= document.getElementById('action-link-field-container');	
	if(enActionTextField.value.trim().length !== 0) {
		if(!arActionTextField.value){
			arActionTextFieldContainer.style.border= "1px red solid";
			return false;
		}
		arActionTextFieldContainer.style.border= "none";
		if(!actionLinkField.value){
			actionLinkFieldContainer.style.border= "1px red solid";
			return false;
		}
		actionLinkFieldContainer.style.border= "none";
	}

	const cardActionLinkField= document.getElementById('card-action-link-field');
	const cardActionLinkFieldContainer= document.getElementById('card-action-link-field-container');
	if(!cardActionLinkField.value) {
		cardActionLinkFieldContainer.style.border= "1px red solid";
		return false;
	}
	cardActionLinkFieldContainer.style.border= "none";

	const backgroundColorFieldContainer= document.getElementById('background-color-field-container');
	const backgroundColorField= document.getElementById('background-color-field');
	if(!backgroundColorField.value) {
		backgroundColorFieldContainer.style.border= "1px red solid";
		return false;
	}
	backgroundColorFieldContainer.style.border= "none";

	const subtitleColorFieldContainer= document.getElementById('subtitle-color-field-container');
	const subtitleColorField= document.getElementById('subtitle-color-field');
	if(!subtitleColorField.value) {
		subtitleColorFieldContainer.style.border= "1px red solid";
		return false;
	}
	subtitleColorFieldContainer.style.border= "none";
	
	const titleColorFieldContainer= document.getElementById('title-color-field-container');
	const titleColorField= document.getElementById('title-color-field');
	if(!titleColorField.value) {
		titleColorFieldContainer.style.border= "1px red solid";
		return false;
	}
	titleColorFieldContainer.style.border= "none";
	
	const actionBackgroundColorFieldContainer= document.getElementById('action-background-color-field-container');
	const actionBackgroundColorField= document.getElementById('action-background-color-field');
	if(!actionBackgroundColorField.value) {
		actionBackgroundColorFieldContainer.style.border= "1px red solid";
		return false;
	}
	actionBackgroundColorFieldContainer.style.border= "none";
	
	const actionTextColorFieldContainer= document.getElementById('action-text-color-field-container');
	const actionTextColorField= document.getElementById('action-text-color-field');
	if(!actionTextColorField.value) {
		actionTextColorFieldContainer.style.border= "1px red solid";
		return false;
	}
	actionTextColorFieldContainer.style.border= "none";
	return true;

}