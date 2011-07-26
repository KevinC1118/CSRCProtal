/**
 * 
 */
function selectElementYear(obj, y) {
	
	var date = new Date();
	var year = date.getFullYear();
	var select_year = $(obj);
	var option;
	
	for(i=2,max=0;i>=max;i--) {
		option = $('<option/>');
		value = year - i
		option.val(value);
		option.text(value);
		option.appendTo(select_year);
	}
	if(y)
		select_year.val(y);
	else
		select_year.val(year);
}

function selectElementMonth(obj, m) {
	
	var date = new Date();
	var month = date.getMonth() + 1;
	var select_month = $(obj);
	var option;
	
	for(i=1,max=13;i<max;i++) {
		option = $('<option/>');
		option.val(i);
		option.text(i.toString());
		option.appendTo(select_month);
	}
	if(m)
		select_month.val(m);
	else
		select_month.val(month);
}