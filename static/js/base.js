$(document).ready(function () {
  $(document).foundation();
  $("#user_search").autocomplete({
    source: function(request, response) {
      $.getJSON("/auto_search",{
        term: request.term, // in flask, "q" will be the argument to look for using request.args
        }, function(data) {
          response(data.list); // matching_results from jsonify
        });
      },
    messages: {
      noResults: '',
      results: ''
    },  
    minLength: 1
  });
});