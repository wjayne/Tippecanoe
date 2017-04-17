function fake_link(){
	var pn = $('#email').val();
	window.location.href = "/search/" + pn.trim();
	console.log("WHY " + pn)
	return false;
}
