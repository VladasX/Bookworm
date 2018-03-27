// AJAX code.

// Checks if a username is taken and updates a label to let the user know if it is or isn't.
$("#id_username").change(function () {
  var username = $(this).val();

  $.ajax({
    url: '/ajax/validate_username/',
    data: {
      'username': username
    },
    dataType: 'json',
    success: function (data) {
    	var label = document.getElementById('is_taken_label')
		if (data.is_taken) {
			label.innerHTML = "Username is already taken."
			label.classList =  "col-7 stat badge-pill badge-danger"
			label.style["max-width"] = "188px"
		} else{
			label.innerHTML = "Username is available."
			label.classList =  "col-7 stat badge-pill badge-success"
			label.style["max-width"] = "158px"
      }
    }
  });

});