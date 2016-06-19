

$(document).ready(function () {
  $(document).foundation();

  $("#user_search").autocomplete({
    source: function(request, response) {
      $.getJSON("{{ url_for('auto_search') }}",{
        q: request.term, // in flask, "q" will be the argument to look for using request.args
        }, function(data) {
          response(data.list); // matching_results from jsonify
        });
      },
    messages: {
      noResults: '',
      results: ''
    },  
    minLength: 2
  });
  
  $('.clip').click(function(event) {
    console.log(event.target.id);
  });
});