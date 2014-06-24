var url = "http://link-manager.herokuapp.com/links";

chrome.tabs.getSelected(function(tab) {
	$('#url').val(tab.url);
});

$( "#add" ).submit(function( event ) {
  $('.url').replaceWith('<p>Submitted</p>');
  event.preventDefault();
  $.ajax({
	type: "POST",
	url: url,
	data: $('#add').serialize(),
	success: function(data) {
		alert(data);
	}
});
});

