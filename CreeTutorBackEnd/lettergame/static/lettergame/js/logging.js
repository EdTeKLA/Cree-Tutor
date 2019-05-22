var startTime = undefined;
var endTime = undefined;
var hoveredArr = [];
var startHover = undefined;
var endHover = undefined;
var hovered = 'not changed';
var distractors;

$(window).on("load", function(e){
    // Onload, function sets StartTime to when the user started looking at this page
    startTime = getTime();
    return;
});

function getTime(){
    // Function gets current date and converts it into ISO format
    // returns the date
    wT = new Date();
    // console.log(Intl.DateTimeFormat().resolvedOptions().timeZone);
    whichTime = wT.toISOString();
    // console.log(whichTime);
    return whichTime;
}


function getDistractors(){
    // gets all the values of the radio buttons, except for the correct answer, and pushes them onto a global list
    distractors = [];
    let letters = $('input[type=radio]').each(function(){$(this).attr('value')});
    let correct = $('#correct_r').attr('value');
    for(let i = 0; i < letters.length; i++){
        if(letters[i].value != correct){
            distractors.push(letters[i].value);
        }
    }
    // console.log(distractors);
    return;
}


$('body').on('mouseenter', 'input[type=radio]', function(){
    // Gets the time for when user hovers over a radio input
    startHover = getTime();
});
$('body').on('mouseout', 'input[type=radio]', function(){
    // Gets the time for when a user leaves hover over a radio input
    hovered = $(this).attr('value');
    endHover = getTime();
    // adds the gathered time and radio input value to a list, which itslef is then pushed to the global list hoveredArr
    var info = [hovered, startHover, endHover];
    hoveredArr.push(info);
    return;
});

$(document).on('submit', '#game_ans', function(e){
    getDistractors();
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
            // if the post is a success, modify the form for the next question
            modifyForm('game_ans', data);
        },
        error:function(error){console.log(error)}
    });
    startTime = getTime();
});


function modifyForm(formID, data){
    console.log("modifyForm");
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
    sub.setAttribute("class","btn btn-primary choice_button");
    sub.setAttribute("type", "submit");
    sub.setAttribute("value","submit");
    form.appendChild(sub);

    return;
}
