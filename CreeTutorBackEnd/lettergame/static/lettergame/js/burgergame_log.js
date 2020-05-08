function getCookie(name) {
    var cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        var cookies = document.cookie.split(';');
        for (var i = 0; i < cookies.length; i++) {
            var cookie = jQuery.trim(cookies[i]);
            // Does this cookie string begin with the name we want?
            if (cookie.substring(0, name.length + 1) === (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}
var csrftoken = getCookie('csrftoken');

function csrfSafeMethod(method) {
    // these HTTP methods do not require CSRF protection
    return (/^(GET|HEAD|OPTIONS|TRACE)$/.test(method));
}

$.ajaxSetup({
    beforeSend: function(xhr, settings) {
        if (!csrfSafeMethod(settings.type) && !this.crossDomain) {
            xhr.setRequestHeader("X-CSRFToken", csrftoken);
        }
    }
});

function postLevels(level){
level = tuple(level)
    return $.ajax({
        type:'POST',
        url:"",
        data:{
           level:level
        },
          success: function (data) {
          console.log(data)
          burgerReset(data['Conjugation'], data['Verb'], data['PrefixDistractors'], data['SuffixDistractors'], data['VerbDistractors']);
      },
      error:function(error){
        console.log(error)
      }
    });

}
function postCompletedSession(numberCorrect){
    let numberOfCorrect = tuple(numberCorrect)
    return $.ajax({
        type:'POST',
        url:"",
        data: {
        numberCorrect:numberOfCorrect
        },
          success: function (data) {
          console.log(data) // view the incoming data
          // Catch the incoming data here, and the pass what you want to a function
          // in the burgergame.js
      },
      error:function(error){
        console.log(error)
      }
    });
}