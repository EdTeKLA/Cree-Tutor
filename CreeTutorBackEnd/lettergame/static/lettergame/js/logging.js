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


$(document).on('submit', '#game_ans', function(e){
    e.preventDefault();

    $.ajax({
      type:'POST',
      url: "",
      data:{
        user_r:$('input[name=user_r]:checked').val(),
        correct_r:$("#correct_r").val()
      },
      success:function(data){
        // console.log(data['letters']);
        modifyForm('game_ans', data);
      },
      error:function(error){console.log(error)}
    });
    }
  );

function modifyForm(formID, data){

  // Update the correct response
  var correct = document.getElementById("correct_r");
  correct.setAttribute("value", data['correct']);

  // All of the children of the form in game.html have the class 'choice_button'. Delete them
  $(".choice_button").remove();
  var form = document.getElementById(formID);

  // Update the src path of the audio file and load the new audio file
  var audio = document.getElementById("aud");
  path = '/static/' + data['sound'];
  var sound = document.getElementById("sound");
  sound.setAttribute("src", path);
  audio.load();

  // Create the new radio options
  for(var i = 0, l = data['letters'].length; i < l; i++){
    var datum = data['letters'][i];
    var rad = document.createElement("INPUT");
    rad.setAttribute("type", "radio");
    rad.setAttribute("class", "choice_button");
    rad.setAttribute("required", true);
    rad.setAttribute("name", "user_r");
    rad.setAttribute("value", datum);
    var lab = document.createElement("LABEL");
    lab.setAttribute("for", datum);
    lab.setAttribute("class", "choice_button");
    lab.innerHTML = datum;
    linebreak = document.createElement("br");
    linebreak.setAttribute("class", "choice_button");
    form.appendChild(rad);
    form.appendChild(lab);
    form.appendChild(linebreak);
  }

  //Re-create the new submit button
  var sub = document.createElement("INPUT");
  sub.setAttribute("class","choice_button");
  sub.setAttribute("type", "submit");
  sub.setAttribute("value","submit");
  form.appendChild(sub);

  return;
}
