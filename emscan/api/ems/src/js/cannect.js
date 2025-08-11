
function notReady(){
	alert("Function Not Ready");
}

function toggleEngineType() {
/* -------------------------------------------------
	AUTHOR      : JEHYEUK LEE
	PUBLISHED   : 2025-07-30
	DESCRIPTION : 
		ENGINE TYPE TOGGLE
------------------------------------------------- */
	$('.toggle i').toggleClass('bi-toggle2-off bi-toggle2-on');
	if ($('.toggle i').hasClass('bi-toggle2-off')){
		$('.engine-type').html('ICE');
		$('.bi-file-earmark-code').attr('title', '%ComDef');
		$('.bi-box-arrow-in-right').attr('title', '%ComRx');
		$('.bi-box-arrow-right').attr('title', '%ComTx');
	} else {
		$('.engine-type').html('HEV');
		$('.bi-file-earmark-code').attr('title', '%ComDef_HEV');
		$('.bi-box-arrow-in-right').attr('title', '%ComRx_HEV');
		$('.bi-box-arrow-right').attr('title', '%ComTx_HEV');
	}
};

function genComDef() {
/* -------------------------------------------------
	AUTHOR      : JEHYEUK LEE
	PUBLISHED   : 2025-07-30
	DESCRIPTION : 
		GENERATE COMDEF MODULE
------------------------------------------------- */
	const engType = $('.engine-type').text()
	
	const formData = new FormData();
	formData.append('engineType', engType);
	
	fetch('/download-comdef', {
		method: 'POST',
		body: formData
	})
	.then(response => response.blob())  // XML 파일로 응답 받기
	.then(blob => {
		const url = window.URL.createObjectURL(blob);
		const a = document.createElement("a");
		a.href = url;
		a.download = engType == "HEV" ? "ComDef_HEV":"ComDef";
		document.body.appendChild(a);
		a.click();
		a.remove();
	})
	.catch(error => console.error("Error:", error));
};

function genComDef() {
/* -------------------------------------------------
	AUTHOR      : JEHYEUK LEE
	PUBLISHED   : 2025-07-30
	DESCRIPTION : 
		GENERATE COMDEF MODULE
------------------------------------------------- */
	document.getElementById("spinner").style.display = "block";
  	document.getElementById("blur-overlay").style.display = "block";

	const engType = $('.engine-type').text()
	
	const formData = new FormData();
	formData.append('engineType', engType);
	
	fetch('/download-comdef', {
		method: 'POST',
		body: formData
	})
	.then(response => response.blob())  // XML 파일로 응답 받기
	.then(blob => {
		const url = window.URL.createObjectURL(blob);
		const a = document.createElement("a");
		a.href = url;
		a.download = engType == "HEV" ? "ComDef_HEV":"ComDef";
		document.body.appendChild(a);
		a.click();
		a.remove();
	})
	.catch(error => console.error("Error:", error))
	.finally(e => {
		document.getElementById("spinner").style.display = "none";
  		document.getElementById("blur-overlay").style.display = "none";
	});
};

function genComRx() {
/* -------------------------------------------------
	AUTHOR      : JEHYEUK LEE
	PUBLISHED   : 2025-07-30
	DESCRIPTION : 
		GENERATE COMRX MODULE
------------------------------------------------- */
	document.getElementById("spinner").style.display = "block";
  	document.getElementById("blur-overlay").style.display = "block";

	const engType = $('.engine-type').text()
	
	const formData = new FormData();
	formData.append('engineType', engType);
	
	fetch('/download-comrx', {
		method: 'POST',
		body: formData
	})
	.then(response => response.blob())  // XML 파일로 응답 받기
	.then(blob => {
		const url = window.URL.createObjectURL(blob);
		const a = document.createElement("a");
		a.href = url;
		a.download = engType == "HEV" ? "ComRx_HEV":"ComRx";
		document.body.appendChild(a);
		a.click();
		a.remove();
	})
	.catch(error => console.error("Error:", error))
	.finally(e => {
		document.getElementById("spinner").style.display = "none";
  		document.getElementById("blur-overlay").style.display = "none";
	});
};


$('.toggle i').on('click', toggleEngineType);
$('.engine-type').on('click', toggleEngineType);
$('.tool .bi-file-earmark-code').on('click', genComDef);
$('.tool .bi-box-arrow-in-right').on('click', genComRx);
$('.tool .bi-box-arrow-right').on('click', notReady);
$('.tool .bi-search-heart').on('click', notReady);
$('.tool .bi-filetype-xlsx').on('click', notReady);
$('.tool .bi-journals').on('click', notReady);
$('.tool .bi-cloud-download').on('click', notReady);
$('.tool .bi-folder2-open').on('click', notReady);