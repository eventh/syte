function setupDocuments(el) {
  var href = el.href;

  if ($('#documents-profile').length > 0) {
    window.location = href;
    return;
  }

  var spinner = new Spinner(spin_opts).spin();
  $('#documents-link').append(spinner.el);

  require(["json!/documents/", "text!templates/document-list.html"],
    function(data, view) {
      if (data.error || data.length === 0) {
        window.location = href;
        return;
      }

      var template = Handlebars.compile(view);
      $(template(data)).modal().on('hidden', function () {
        $(this).remove();
        adjustSelection('home-link');
      });

      spinner.stop();

    }
  );

  window.location = href;
}
