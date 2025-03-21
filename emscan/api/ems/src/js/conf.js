var TAB = 'Summary';

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
		
		$('.fa-trash').click(function(){
			$('td[value="' + $(this).parent().attr('value') + '"]').remove();
			var cnt = $('thead td').length;
			
		});
	})
	.catch(
		error => {
			console.error('Error Reading Conf: ', error);
			alert(error);
	});
		
		

}
