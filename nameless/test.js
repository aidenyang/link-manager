
var url = "https://link-manager.herokuapp.com/links";

chrome.tabs.getSelected(function(tab) {
	$('#url').val(tab.url);
});

$( "#add" ).submit(function( event ) {
  event.preventDefault();
  $.ajax({
	type: "POST",
	url: url,
	dataType: 'json',
	data: $('#add').serialize(),
	success: function(data) {
		alert("success!");
	},
	error: function() {
		alert("error!");
	}
});
});

