var __stack__ = [];

function snapShot() {
	__stack__.push(currentTable()[0].innerHTML);
}


function undo() {
/* -------------------------------------------------
	AUTHOR      : JEHYEUK LEE
	PUBLISHED   : 2025-05-15
	DESCRIPTION : 
		실행 취소
------------------------------------------------- */
	if (__stack__.length) {
		currentTable()
		.empty()
		.html(__stack__.pop())
		.find('select').each(function() {
			$(this).val($(this).attr('data-selected'));
		});
	}	
}

function loadConf() {
/* -------------------------------------------------
	AUTHOR      : JEHYEUK LEE
	PUBLISHED   : 2025-05-14
	DESCRIPTION : 
		API로 confdata 리스트 요청
		- 정상 응답: 응답 값 select 요소 반영
		- 부정 응답: console 오류 표출
------------------------------------------------- */
	fetch('/load-conf')
	.then(response => response.json())
	.then(data => {
		$('.confdata-list')
		.select2({placeholder: "CONFDATA 검색"})
		.empty()
		.append('<option></option>');
		data.conf.forEach(item => {
			$('.confdata-list').append(`<option>${item}</option>`);
		});
	})
	.catch(error => console.error('Error Loading Conf: ', error));
}
  
function readConf(src) {
/* -------------------------------------------------
	AUTHOR      : JEHYEUK LEE
	PUBLISHED   : 2025-05-14
	DESCRIPTION : 
		API로 선택된 confdata 값 요청
		- 정상 응답:
			.tab 상 DEM 요소 개수 표출
			#SUMMARY 작성
			#{table} 작성
				<thead>에 .column-selector 추가
				<tbody> 각 cell에 .dem-value 추가
				<tbody> row 중 FID/group 속성인 경우 .group 추가
				<tbody> 각 cell에 edit 속성 추가
				<tbody> cell 중 enum 속성인 경우 <select> 추가
------------------------------------------------- */
	__mem__ = {};	
	
	const formData = new FormData();
	formData.append('conf', src);
	
	fetch('/read-conf', {
		method: 'POST',
		body: formData
	})
	.then(response => response.json())
	.then(data => {
	    const meta = ["PATH", "EVENT", "FID", "DTR", "SIG"];
		var admin = JSON.parse(data.admin);
		var keys = JSON.parse(data.keys);
	
		$('.module').html(admin.Model);
		$('.conf-unit').html(admin.Filename);
		$('.user').html(admin.User);
		$('.gen-date').html(admin.Date);
		$('.svn-date').html(admin.SVNDate);
		$('.svn-version').html(admin.SVNRev);
		$('.svn-user').html(admin.SVNUser);
		$('.history').html(data.history);
			
//		Object.entries(meta).forEach(([key, obj]) => {
        meta.forEach(obj => {
		  	let objCount = data[`N${obj}`];
		  	let objClass = keys[obj];
  
		  	$(`.tab[data-label="${obj}"]`).html(`${obj}(${objCount})`);
		  	$(`#${obj}`).html(data[obj]);
			$(`#${obj} .dem-count`).html(`${objCount} ITEMS`);
			$(`#${obj} thead tr td:not(.row)`).addClass("column-selector");
			$(`#${obj} tbody tr td:not(.row)`).addClass("dem-value");

		  	$(`#${obj} tbody tr`).each(function(){
				let objMeta = objClass[$(this).attr('class')];
				if ("group" in objMeta) {
			  		$(this)
					.attr('data-group', objMeta['group'])
					.find('.row').addClass('group');
				}
				$(this).find('.row').attr('title', objMeta.note);
				$(this).find('td:not(.row)').each(function() {
					$val = $(this).html();
			  		$(this).addClass(objMeta["write"]);
			  		if (objMeta["write"] === "selectable") {
						let $select = $('<select></select>').attr('data-selected', $val);
						if (typeof objMeta.option === 'string') {
						    objMeta.option = JSON.parse(objMeta.option);
						}
                        objMeta.option.forEach(function(item) {
				  			$select.append($(`<option value="${item}">${item}</option>`));
				  		});
						$select.val($val);
						$(this).empty().append($select);
			  		}
				})
		  	})
		});
		__stack__ = [];
		snapShot();
	})
	.catch(
		error => {
			console.error('Error Reading Conf: ', error); alert(error);
	});
}
	
function downloadConf(conf) {
/* -------------------------------------------------
	AUTHOR      : JEHYEUK LEE
	PUBLISHED   : 2025-05-14
	DESCRIPTION : 
		API로 confdata 파일 생성 요청 및 파일 응답
------------------------------------------------- */
	const formData = new FormData();
	const tables = $("table").map(function() {
		$(this).find('tbody tr td.selectable').each(function(){
			$(this).text($(this).find('select').val());
		});
		return $(this).prop("outerHTML");
	}).get().join("\n");
	  
	formData.append('conf', conf);
	formData.append('tables', tables);
  
	fetch('/download-conf', {
		method: 'POST',
		body: formData
	})
	.then(response => response.blob())  // XML 파일로 응답 받기
	.then(blob => {
		const url = window.URL.createObjectURL(blob);
		const a = document.createElement("a");
		a.href = url;
		a.download = conf;
		document.body.appendChild(a);
		a.click();
		a.remove();
	})
	.catch(error => console.error("Error:", error));
}

function backTest() {
/* -------------------------------------------------
	AUTHOR      : JEHYEUK LEE
	PUBLISHED   : 2025-07-16
	DESCRIPTION :
		API로 confdata 파일 생성 요청 및 파일 응답
------------------------------------------------- */
}
  
function editCell(cell) {
/* -------------------------------------------------
	AUTHOR      : JEHYEUK LEE
	PUBLISHED   : 2025-05-14
	DESCRIPTION : 
		Cell 수정: *Select 요소는 별개로 처리
------------------------------------------------- */
	var $cell = $(cell);
	if ($cell.find("input").length) return;
  	$(`td[value="${$cell.attr("value")}"`).addClass('column-selected');
	$('<input type="text">')
	.val($cell.text())
	.appendTo(
		$cell.empty().addClass('on-edit')
	)
	.on('keydown', function(e) {
		if (e.key == 'Enter') {
			$cell.text($(this).val()).removeClass('on-edit');		
			updateKey($cell, $(this).val());
		}		
	})
	.on('blur', function() {
		$cell.text($(this).val()).removeClass('on-edit');
		updateKey($cell, $(this).val());
	})
	.focus();
}

function editParagraph(cell) {
/* -------------------------------------------------
	AUTHOR      : JEHYEUK LEE
	PUBLISHED   : 2025-05-14
	DESCRIPTION : 
		Summary/History 작성 
------------------------------------------------- */
	var $cell = $(cell);
	if ($cell.find("textarea").length) return;
  
	$('<textarea>')
	.attr("rows", $(cell).find('br').length + 1)
	.val($cell.html().replace(/<br\s*\/?>/gi, '\n'))
	.appendTo(
	  $cell.empty().addClass('on-edit')
	)
	.on('blur', function() {
	  $cell
	  .html($(this).val().replace(/\n/g, '<br>'))
	  .removeClass('on-edit');
	})
	.focus();
}

function currentTable() {
/* -------------------------------------------------
	AUTHOR      : JEHYEUK LEE
	PUBLISHED   : 2025-05-14
	DESCRIPTION : 
		현재 테이블
------------------------------------------------- */
	return $(`#${$('.tab.active').attr('data-label')}`);
}
  
function updateKey(cell, newVal) {
/* -------------------------------------------------
	AUTHOR      : JEHYEUK LEE
	PUBLISHED   : 2025-05-14
	DESCRIPTION : 
		Element Name 또는 Syscon 정보 기반 UID 생성
------------------------------------------------- */
	let cls = cell.parent().attr("class");
	let uid = cell.attr("value");
	if (!["ELEMENT_NAME", "SYSCON"].includes(cls)) {
		return;
	}
	updateEventCounter();
	if (cls === "ELEMENT_NAME") {
		let keyName = newVal;
		let keySysc = currentTable().find(`tbody tr.SYSCON td[value="${uid}"]`).text();
		$(`td[value="${uid}"]`).attr("value", `${keyName}-${keySysc}`.replaceAll(" ", ""));
	} else{
		let keyName = currentTable().find(`tbody tr.ELEMENT_NAME td[value="${uid}"]`).text();
		let keySysc = newVal;
		$(`td[value="${uid}"]`).attr("value", `${keyName}-${keySysc}`.replaceAll(" ", ""));
	}
}
  
function appendColumn(pos) {
/* -------------------------------------------------
	AUTHOR      : JEHYEUK LEE
	PUBLISHED   : 2025-05-14
	DESCRIPTION : 
		열 추가
------------------------------------------------- */
	let uid = Date.now().toString(36) + Math.random().toString(36).substring(2, 6);
	let $cellIndex = (pos == "left" ? $('td.column-selected').first() : $('td.column-selected').last()).index();
	let $copied = $('td.column-copied-top');
	if ($copied.length) {
		$cellIndex = $copied.first().index();
	}
	if (($cellIndex === -1) && (pos === "left")) {
		$cellIndex = 1;
	}

	currentTable().find('tr').each(function() {
		const $refCell = $(this).children().eq($cellIndex);
		const $cellCls = $refCell.attr('class');
		let $newCell = $(`<td value="${uid}">`).addClass($cellCls);
		if ($copied.length) {
			if ($refCell.find('select').length) {
				$newCell
				.html($refCell.html())
				.find('select')
				.val($refCell.find('select').val());
			} else {
		  		if ($refCell.parent().hasClass('ELEMENT_NAME')) {
					$newCell.html(`${$refCell.text()}-Copy`);
		  		} else {
					$newCell.html($refCell.html());
		  		}		
			} 
		} else {
			if ($refCell.find('select').length) {
		  		$newCell.html($refCell.html());	
			}
	  	}
	  	$newCell.attr('value', uid);
	  
		if (pos == "left") {
			$refCell.before($newCell);
	  	} else {
			$refCell.after($newCell);
	  	}
	});
	clearOperation();
	updateEventCounter();
}

function appendRow(pos) {
/* -------------------------------------------------
	AUTHOR      : JEHYEUK LEE
	PUBLISHED   : 2025-05-14
	DESCRIPTION : 
		행 추가(FID group 요소 대상)
------------------------------------------------- */
	let $selected = $('tr.row-selected');
	if (!$selected.length) {
		return;
	}
	let $selectedHtml = $selected.map(function() {
		const $_row = $(this).clone();
		if (!$_row.find('select').length) {
			$_row.find('td:not(.row)').text('');	
	  	}	  
	  	return $_row[0].outerHTML;
	}).get().join('');

	if (pos === "after") {
		$selected.last().after($selectedHtml);
	} else {
		$selected.first().before($selectedHtml);
	}
	clearOperation();
}
  
function deleteColumn() {
/* -------------------------------------------------
	AUTHOR      : JEHYEUK LEE
	PUBLISHED   : 2025-05-14
	DESCRIPTION : 
		선택된 열 삭제
------------------------------------------------- */
	while ($('td.column-selected').length > 0) {
		const $selected = $('td.column-selected').first().attr('value');
		$(`td[value="${$selected}"]`).remove();
	}
	updateEventCounter();
  }

function deleteRow() {
/* -------------------------------------------------
	AUTHOR      : JEHYEUK LEE
	PUBLISHED   : 2025-05-14
	DESCRIPTION : 
		선택된 행 삭제
------------------------------------------------- */
	$('.row-selected').remove();
}
  
function copyColumn() {
/* -------------------------------------------------
	AUTHOR      : JEHYEUK LEE
	PUBLISHED   : 2025-05-14
	DESCRIPTION : 
		열 복사
------------------------------------------------- */
	let $selected = $('td.column-selected').first().attr('value');
	clearOperation();
	$selected = $(`td[value="${$selected}"]`);
	$selected.each(function(i) {
		if (i == 0) {
			$(this).addClass('column-copied-top');
		} else if (i === $selected.length - 1) {
			$(this).addClass('column-copied-bottom');
		} else {
			$(this).addClass('column-copied-middle');
		}
	})
}
  
function clearOperation() {
/* -------------------------------------------------
	AUTHOR      : JEHYEUK LEE
	PUBLISHED   : 2025-05-14
	DESCRIPTION : 
		열 복사
------------------------------------------------- */
	$('td')
	.removeClass('column-selected')
	.removeClass('emphasis')
	.removeClass('column-copied-top')
	.removeClass('column-copied-middle')
	.removeClass('column-copied-bottom');
	$('tr')
	.removeClass('row-selected');
}
  
function updateEventCounter() {
/* -------------------------------------------------
	AUTHOR      : JEHYEUK LEE
	PUBLISHED   : 2025-05-14
	DESCRIPTION : 
		현재 테이블의 DEM 요소 개수 업데이트
------------------------------------------------- */
	let $currentTable = currentTable();
	let $tabName = $currentTable.attr('id');
	let $count = $currentTable.find('tr').eq(1).find('td').filter(function() {
		return $(this).text() !== '';
	}).length - 1;

	$(`.tab[data-label="${$tabName}"]`).html(`${$tabName}(${$count})`);
	$currentTable.find('.dem-count').html(`${$count} ITEMS`);
	currentTable().find('.column-selector').each(function(i){
		$(this).text(i + 1);
	})
}
  

$(document)
.ready(function(){
    if($('.backtest').length){
        $('.bi-download').addClass('config-exception');
    }
})
.on('select2:select', '.confdata-list', function(e) {
/* =============================================================
	[EVENT BINDER]
	CONFDATA READ
============================================================= */
	readConf(e.params.data.id);
})
.on('click', '.reload', function() {
	readConf($('.confdata-list').val());
})
.on('click', '.download', function() {
	var conf = $('.confdata-list').val();
	if (!conf) {
		alert("선택된 Confdata가 없습니다.");
	} else {
		downloadConf(conf);
	}	
})
.on("click", "td.group", function() {
	var $row = $(this).parent();
	var $rowN = $row.index();
	var $tbody = $row.parent();	
	
	for (var i = $rowN; i >= 14; i--) {
		let $_row = $tbody.children().eq(i);
		if ($_row.attr('class').replace(' row-selected', '') === $_row.attr('data-group')) {
			$_row.toggleClass('row-selected');
			$tbody.children().eq(i + 1).toggleClass('row-selected');
			$tbody.children().eq(i + 2).toggleClass('row-selected');
			break;
		}
	}
})
.on("click", ".roll-back", function() {
	undo();
})
.on('keydown', function (e) {
  	if (e.ctrlKey && (e.key === 'z' || e.key === 'Z')) {
		e.preventDefault();
		undo();
  	}
})
.on("click", ".add-column-left", function() {
	snapShot();
	appendColumn("left");
})
.on("click", ".add-column-right", function() {
	snapShot();
	appendColumn("right");
})
.on("click", ".delete-column", function() {
	snapShot();
	deleteColumn();
})
.on("click", ".copy-column", function() {
	snapShot();
	copyColumn();
})
.on("click", ".add-row-bottom", function() {
	snapShot();
	appendRow('after');
})
.on("click", ".add-row-top", function() {
	snapShot();
	appendRow('before');
})
.on("click", ".delete-row", function() {
	snapShot();
	deleteRow();
})
.on("click", ".tab", function(){
	var tab = $(this).attr('data-label');
	$('.tabcontent').removeClass('active');
	$('.tab').removeClass('active');
	$('#' + tab).addClass('active');
	$(this).addClass('active');
	
	currentTable().find('.column-selector').each(function(i){
		$(this).text(i + 1);
	})
	__stack__ = [];
	snapShot();
})
.on("click", ".column-selector", function() {
	$(`td[value="${$(this).attr("value")}"]`).toggleClass('column-selected emphasis');
})
.on("click", ".writable", function() {
	clearOperation();
	snapShot();
	if ($(this).attr("class").includes("paragraph")) {
		editParagraph(this);
	} else {
		editCell(this);
	}	
})
.on("focus", ".selectable select", function() {
	snapShot();
	$(this).on('change', function() {
		$(this).attr('data-selected', $(this).val());
	})	
})
.on('keydown', function(e) {
	if (e.key === 'Escape') {
		clearOperation();
	}
})
  
loadConf();
  