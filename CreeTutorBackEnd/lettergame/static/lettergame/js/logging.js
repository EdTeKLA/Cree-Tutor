var startTime = undefined
var endTime = undefined
var hoveredArr = [];
var startHover = undefined;
var endHover = undefined;
var hovered = 'not changed';
var distractors;

$(window).on("load", function(e){
    startTime = getTime();
    getDistractors();
    return;
});

function getTime(){
    wT = new Date();
    console.log(Intl.DateTimeFormat().resolvedOptions().timeZone);
    whichTime = wT.toISOString();
    return whichTime;
}


function getDistractors(){
    distractors = [];
    let letters = $('input[type=radio]').each(function(){$(this).attr('value')});
    let correct = $('#correct_r').attr('value');
    for(let i = 0; i < letters.length; i++){
        if(letters[i].value != correct){
            distractors.push(letters[i].value);
        }
    }
    return;
}

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

$('body').on('mouseenter', 'input[type=radio]', function(){
    startHover = getTime();
});
$('body').on('mouseout', 'input[type=radio]', function(){
    hovered = $(this).attr('value');
    endHover = getTime();
    var info = [hovered, startHover, endHover];
    hoveredArr.push(info);
    return;
});

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
    endTime = getTime();

    $.ajax({
        type:'POST',
        url: "",
        data:{
            user_r:$('input[name=user_r]:checked').val(),
            correct_r:$("#correct_r").val(),
            time_s: startTime,
            time_e: endTime,
            'arrHov[]': hoveredArr,
            'distract[]': distractors
        },
        success:function(data){
            // console.log(data['letters']);
            modifyForm('game_ans', data);
        },
        error:function(error){console.log(error)}
    });
    startTime = getTime();
});


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
