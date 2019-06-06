var startTime = undefined;
var endTime = undefined;
var hoveredArr = [];
var startHover = undefined;
var endHover = undefined;
var hovered = 'not changed';
var distractors;
var audio = undefined;

$(window).on("load", function(e){
    // Onload, function sets StartTime to when the user started looking at this page
    startTime = getTime();
    // Show the tooltip that suggests that the person click the speaker button to play the audio for 1500ms
    $('[data-toggle="tooltip"]').tooltip();
    $("#speaker-button").tooltip('show');
    setTimeout(function(){ $("#speaker-button").tooltip('hide'); }, 1500);
    // Get the audio file and click the speaker
    getAudioAndClickSpeaker();

    return;
});

function getAudioAndClickSpeaker(){
    // Get the audio file from the server
    audio = new Audio(audioFileLocation, playAudio);
    // Click the speaker button to play the audio
    $("#speaker-button").click();
}

$(document).on('click', '#speaker-button', function (e) {
    // When the speaker-button is clicked, the function that plays audio is called
    playAudio();
});

function playAudio(){
    // Function plays the audio
    audio.play();
}

function getTime(){
    // Function gets current date and converts it into ISO format
    // returns the date
    wT = new Date();
    whichTime = wT.toISOString();
    return whichTime;
}


function getDistractors(){
    // gets all the values of the submit buttons, except for the correct answer, and pushes them onto a global list
    distractors = [];
    let letters = $('[type=submit]').each(function () { $(this).attr('value'); });
    let correct = $('#correct_r').attr('value');
    for(let i = 0; i < letters.length; i++){
        if(letters[i].value != correct){
            distractors.push(letters[i].value);
        }
    }
    return;
}


$(document).on('mouseenter', '[type=submit]', function(){
    // Gets the time for when user hovers over a radio input
    startHover = getTime();
});

$(document).on('mouseout', '[type=submit]', function(){
    // Gets the time for when a user leaves hover over a radio input
    hovered = $(this).attr('value');
    endHover = getTime();
    // adds the gathered time and radio input value to a list, which itslef is then pushed to the global list hoveredArr
    var info = [hovered, startHover, endHover];
    hoveredArr.push(info);
    return;
});

$(document).on('click', '[type=submit]', function(e){
    // When a button is pushed, send a POST request logging the event and getting a new set up of questions
    e.preventDefault();
    getDistractors();
    endTime = getTime();

    $.ajax({
        type:'POST',
        url: "",
        data:{
            user_r:$(this).attr('value'),
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

    hoveredArr = [];
    startTime = getTime();
});


function modifyForm(formID, data){
    // Update the correct response
    var correct = document.getElementById("correct_r");
    correct.setAttribute("value", data['correct']);

    // All of the children of the form in game.html have the class 'choice_button'. Delete them
    $(".submit_answer").remove();
    var form = document.getElementById(formID);

    // Load the new audio file once you get the new links
    audioFileLocation = '/static/' + data['sound'];
    getAudioAndClickSpeaker();

    // Create the new radio options
    for(var i = 0, l = data['letters'].length; i < l; i++){
        var datum = data['letters'][i];
        var rad = document.createElement("INPUT");
        rad.setAttribute("type", "submit");
        rad.setAttribute("class", "btn btn-default m-3 pl-5 pr-5 submit_answer");
        rad.setAttribute("value", datum);
        form.appendChild(rad);
    }

    return;
}
