function setupAbout(el) {
  var href = el.href;

  if ($('#about-profile').length > 0) {
    window.location = href;
    return;
  }

  var spinner = new Spinner(spin_opts).spin();
  $('#about-link').append(spinner.el);

  require(["json!/about/", "text!templates/about.html"],
    function(data, view) {
      if (data.error || data.length === 0) {
        window.location = href;
        return;
      }

      var template = Handlebars.compile(view);
      $(template(data)).modal().on('hidden', function () {
        $(this).remove();
        adjustSelection('home');
      });

      spinner.stop();
    }
  );

  window.location = href;
}
