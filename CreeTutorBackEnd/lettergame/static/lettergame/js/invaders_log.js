// TODO: we can probably delete this because it's now in static/common/js/common.js but leaving for now until we can test to make sure


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

function postInvaders(){
    // e.preventDefault();
    let letters = [];
    let positions = [];
    let hit = [];
    for(let i = 0; i < invaders.length; i++){
        letters.push(invaders[i].children[0].text);
        pos = Math.floor(invaders[i].x) + "," + Math.floor(invaders[i].y);
        positions.push(pos)
        hit.push(invaders[i].hit);
    }
    let hit = [];
    return $.ajax({
      type:'POST',
      url: "",
      data:{
        correct: correct,
        populate: populate,
        numInvadersLeft: invaders.length,
        'onScreenLetters[]':letters,
        'positions[]':positions,
        'hit[]':hit
      },
        success: function (data) {
          console.log(data)
          populateInvaders(data['letters'], data['correct'], data['sound']);
          // console.log("ya length")
          // console.log(invaders.length)
        //console.log(data);
      },
      error:function(error){
        console.log(error)
      }
    });
}
