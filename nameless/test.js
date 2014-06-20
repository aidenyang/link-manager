chrome.tabs.getSelected(function(tab) {
	$('.url').append(tab.url);
});

$( "#add" ).submit(function( event ) {
  $('.url').replaceWith('<p>Submitted</p>');
  event.preventDefault();
});