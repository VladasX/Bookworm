// JQuery code to be added in here.

// Used to pass book's title and description to a popup window.
$('#book-modal').on('show.bs.modal', function (event) {
  var bookTitle = $(event.relatedTarget).data('title');
  var bookDesc = $(event.relatedTarget).data('desc');
  $(this).find(".modal-header").text(bookTitle);
  $(this).find(".modal-body").text(bookDesc);
  $(this).find(".modal-rating").text("");
});

// Used to pass review info to a popup window.
$('#book-modal').on('show.bs.modal', function (event) {
  var bookTitle = $(event.relatedTarget).data('title');
  var reviewText = $(event.relatedTarget).data('desc');
  var reviewRating = $(event.relatedTarget).data('rating');
  $(this).find(".modal-header").text(bookTitle);
  $(this).find(".modal-body").text(reviewText);
  $(this).find(".modal-rating").text(reviewRating);
});

// Used to toggle what navbar item is active.
$(document).ready(function() {
  $('li.active').removeClass('active');
  $('a[href="' + location.pathname + '"]').addClass('active'); 
});

// Used to hide the search bar if on the search page.
$(function(){
      if (window.location.pathname == "/search/") {
            $('#navsearchbar').hide();
      } else {
            $('#navsearchbar').show();
      }
 });