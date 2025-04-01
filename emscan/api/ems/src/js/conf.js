var TAB = 'Summary';

function highlight() {
	$('td:contains("배타적 FID 관계")').parent().css('border-top', '2px double grey');
	$('td:contains("배타적 FID System Constant 조건")').parent().css('border-bottom', '2px double grey');
	
	$('td:contains("FID 금지 요건인 Event")').parent().css('border-top', '2px double grey');
	$('td:contains("상기 Event 요건의 System Constant")').parent().css('border-bottom', '2px double grey');
	
	$('td:contains("FID 금지 요건인 Sum-Event")').parent().css('border-top', '2px double grey');
	$('td:contains("상기 Sum-Event의 System Constant")').parent().css('border-bottom', '2px double grey');
	
	$('td:contains("FID 금지 요건인 Signal")').parent().css('border-top', '2px double grey');
	$('td:contains("상기 Signal 요건의 System Constant")').parent().css('border-bottom', '2px double grey');
	
	$('td:contains("FID가 Mode7 조건인 Signal")').parent().css('border-top', '2px double grey');
	$('td:contains("상기 Signal의 System Constant 조건")').parent().css('border-bottom', '2px double grey');
	
	$('.color-ref').css('display', 'none');
}

function openTab(evt, key) {
    var tabcontent, tablinks;

    tabcontent = document.getElementsByClassName("tabcontent");
    for (var i = 0; i < tabcontent.length; i++) {
      tabcontent[i].style.display = "none";
    }

    tablinks = document.getElementsByClassName("tablinks");
    for (var i = 0; i < tablinks.length; i++) {
      tablinks[i].className = tablinks[i].className.replace(" active", "");
    }
	TAB = key;
    document.getElementById(key).style.display = "table";
    evt.currentTarget.className += " active";
	if (TAB == 'Summary'){
		$('.color-ref').css('display', 'none');
	} else {
		$('.color-ref').css('display', 'flex');
	}
}

function addRow(button) {
    var tr = $(button).parent();
	var set = [tr];
	tr.prevAll().each(function() {
		if ($(this).hasClass('group-top')){
			set.push($(this).clone());
			return false;
		}
		set.push($(this).clone())
	});
	set.forEach(item => {
		$(item).find("td.dem-value").text("");
		tr.after(item[0].outerHTML);
	});
}

function editCell(cell) {
    if (cell.querySelector("input")) return;

    let originalText = cell.innerText;
    let input = document.createElement("input");
    input.type = "text";
    input.value = originalText;
    cell.innerText = "";
    cell.appendChild(input);
    input.focus();

    input.addEventListener("blur", function() {
      saveCell(cell, input.value);
	  
	  var col = $(cell).parent().find('td:first');
	  if (
	    (col.text() == "진단 Event 명칭") || 
		(col.text() == "Event Path 명칭") || 
	    (col.text() == "함수 식별자 명칭") ||
		(col.text() == "DTR test 명칭") || 
		(col.text() == "신호 명칭")
	  ){
		  if (originalText != input.value) {
			  $('td[value="' + originalText +'"]').attr("value", input.value);
		  }
		  
	  }
	  
    });
	
	
}

function editParagraph(cell) {
	if (cell.querySelector("textarea")) return;
	
	let originalText = cell.innerText;
    let input = document.createElement("textarea");
	let rows = originalText.split('\n').length + 1;

    input.value = originalText;
	input.rows = rows;
    cell.innerText = "";
    cell.appendChild(input);
    input.focus();
	
    input.addEventListener("blur", function() {
      saveCell(cell, input.value);
    });
	
	input.addEventListener("Enter", function() {
		let newRows = input.value.split("\n").length + 1;
		input.rows = newRows;
	});
	
}

function saveCell(cell, newValue) {
    cell.innerText = newValue;
}

function loadConf() {
    fetch('/load-conf')
        .then(response => response.json())
        .then(data => {
            $('.confdata-list')
                .select2({placeholder: "CONFDATA 검색"})
                .empty()
                .append('<option></option>');
            data.conf.forEach(item => {
                $('.confdata-list').append('<option>' + item + '</option>');
            });
        })
        .catch(error => console.error('Error Loading Conf: ', error));
	
	$('.reload').click(function(){
		readConf($('.confdata-list').val());
	})
}

function readConf(src) {
    const formData = new FormData();
    formData.append('conf', src);

    fetch('/read-conf', {
        method: 'POST',
        body: formData
    })
	.then(response => response.json())
	.then(data => {
		var admin = JSON.parse(data.admin);
		var meta = JSON.parse(data.meta);
		
		$('.module').html(admin.Model);
		$('.conf-unit').html(admin.Filename);
		$('.user').html(admin.User);
		$('.gen-date').html(admin.Date);
		$('.svn-date').html(admin.SVNDate);
		$('.svn-version').html(admin.SVNRev);
		$('.svn-user').html(admin.SVNUser);
		$('.history').html(data.history);
		
		Object.entries(meta).forEach(([key, obj]) => {
			$('#' + obj).html(data[obj]);
			$('.tab-' + obj).html(obj + "(" + data["N_" + obj] + ")");
		});
		$('.group-bottom').append('<button class="add-row" onclick="addRow(this);"><i class="fa fa-plus"></i></button>');
		
		$('.fa-trash').click(function(){
			$('td[value="' + $(this).parent().attr('value') + '"]').remove();
			var tds = $("#" + TAB + " thead tr td")
			var cnt = tds.length - 2;
			$(tds[0]).html(cnt + " ITEMS");
			$('.tab-' + TAB).html(TAB + "(" + cnt + ")");
		});
		
		$('.fa-plus').click(function(){
			var n = 1;
			var elem = "new_element";
			
			$(this).parent().prevAll().each(function() {
				var val = $(this).attr("value");
				if (typeof val === "string" && val.startsWith("new_element")) {
					n += 1;
				}
			});
			elem = elem + '_' + n;
			
			$(this).parent().before('<td class="conf-action" value="' + elem + '"><i class="fa fa-trash"></i></td>');
			$("#" + TAB + " tbody tr").each(function(i, e) {
				if (i == 0){
					$(e).find("td:last").after('<td class="dem-value" onclick="editCell(this);" value="'+elem+'">' + elem + '</td>');
				} else {
					$(e).find("td:last").after('<td class="dem-value" onclick="editCell(this);" value="'+elem+'"></td>');
				}				
			});
			
			$(".table-container").scrollLeft($(".table-container")[0].scrollWidth);
		});
	})
	.catch(
		error => {
			console.error('Error Reading Conf: ', error);
			alert(error);
	});
}

function downloadConf(conf) {
	const formData = new FormData();
	const tables = $("table").map(function() {
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
		a.download = conf.replace(".xml", "_sample.xml");
		document.body.appendChild(a);
		a.click();
		a.remove();
	})
	.catch(error => console.error("Error:", error));
}
