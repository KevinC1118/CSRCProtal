jQuery(function($) 
{
    $('#dateinput').datepicker({
    	dateFormat: 'yy-mm-dd',
    	showOn: 'both',
    	buttonImageOnly: true,
    	buttonImage: '/static/images/datepicker/icon.png',
    	});
});

jQuery(document).ready(function(){
	var date = new Date();
	// Setting year and month select element.
	selectElementYear($('#year'));
	selectElementMonth($('#month'));
	
	(function(){
		
		var year = date.getFullYear();
		var month = '0' + (date.getMonth() + 1);
		var day = date.getDate();
		
		$('#dateinput').val(year + '-' + month + '-' + day);
		
	})();
	
	(function(){
		
		var hour = date.getHours();
		var minute = date.getMinutes();
		
		var timeArray = new Array();
		var bhour = $('#bhour');
		var ehour = $('#ehour');
		
		var option1,option2;
		
		for(i=0,max=24;i<max;i++) {
			timeArray.push('0' + i + ':00', '0' + i + ':30');
			option1 = $('<option/>');
			option1.val(getHour(parseInt(i)) + ':00');
			option1.text(getHour(parseInt(i)) + ':00');
			
			option2 = $('<option/>');
			option2.val(getHour(parseInt(i)) + ':30');
			option2.text(getHour(parseInt(i)) + ':30');
			
			option1.appendTo(bhour);
			option2.appendTo(bhour);
			option1.clone().appendTo(ehour);
			option2.clone().appendTo(ehour);
		}
		
		if(minute <= 15)
			ehour.val(getHour(hour) + ":00");
		else if(minute > 15 & minute <= 45)
			ehour.val(getHour(hour) + ':30');
		else
			ehour.val(getHour(hour + 1) + ':00');
		
		setbhour();
		
		bhour.change(function(){
			var bhourV = bhour.val().toString();
			// Not check 00 time
			var bhourNum = parseFloat(bhourV.substr(0,2)) + (bhourV.substr(3).search('30') != -1 ? 0.5 : 0 );
			
			var ehourV = ehour.val().toString();
			var ehourNum = parseFloat(ehourV.substr(0,2)) + (ehourV.substr(3).search('30') != -1 ? 0.5 : 0 );
			
			if(bhourNum >= ehourNum) {
				var num = Math.floor(bhourNum);
				ehour.val(bhourNum > num ? getHour(num + 2) + ':30' : getHour(num + 2) + ':00');
			}
		});
		
		ehour.change(function() {
			
			var bhourV = bhour.val().toString();
			var bhourInt = parseFloat(bhourV.substr(0,2)) + (bhourV.substr(3).search('30') != -1 ? 0.5 : 0 );
			
			var ehourV = ehour.val().toString();
			var ehourNum = parseFloat(ehourV.substr(0,2)) + (ehourV.substr(3).search('30') != -1 ? 0.5 : 0 );
			
			if(ehourNum <= bhourInt) {
				var num = Math.floor(ehourNum);
				bhour.val(ehourNum > num ? getHour(num - 2) + ':30' : getHour(num - 2) + ':00');
			}
		});
	})();
});

function setbhour() {
	
	var ehourV = $('#ehour').val();
	var h = ehourV.toString().substr(0,2);
	var m = ehourV.toString().substr(2);
	$('#bhour').val(getHour(parseInt(h) - 2).toString() + m);
}
function setehour() {
	
	var bhourV = $('#bhour').val();
	var h = bhourV.toString().substr(0,2);
	var m = bhourV.toString().substr(2);
	$('#ehour').val(getHour(parseInt(h) + 2).toString() + m);
}
function getHour(hour) {
	
	if(hour == 24) return '00';
	
	if(hour > 24) hour = hour - 24;
	if(hour < 0) hour = Math.abs(hour);
	
	return hour >= 10 ? hour : '0' + hour;
}
function search() {
    var year = $('#year').val();
    var month = $('#month').val();
    window.location.href = '/employee/show_monthrecord/' + year + '/' + month;
}
function print() {
	var date = new Date();
	var year = date.getFullYear();
	var month = date.getMonth() + 1;
	window.location.href = '/employee/print_workinghours/' + year + '/' + month;
}