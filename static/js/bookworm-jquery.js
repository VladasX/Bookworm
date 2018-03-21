// JQuery code to be added in here.

// Used to pass book's title and description to a popup window
$('#book-modal').on('show.bs.modal', function (event) {
  var bookTitle = $(event.relatedTarget).data('title');
  var bookDesc = $(event.relatedTarget).data('desc');
  $(this).find(".modal-header").text(bookTitle);
  $(this).find(".modal-body").text(bookDesc);
});
