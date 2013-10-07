

//-----------------------------------------------------------------------------
// Student info handlers
//-----------------------------------------------------------------------------
function updateFooterPosition(pageNum) {
  $('#footer').css('margin-top', $('#page' + pageNum).innerHeight() +"px");
}

function nextPageHandler(startTimeId) {
	$('html, body').animate({ scrollTop: 0 });
	nextPage();
}

function backPageHandler() {
	$('html, body').animate({ scrollTop: 0 });
	backPage();
}