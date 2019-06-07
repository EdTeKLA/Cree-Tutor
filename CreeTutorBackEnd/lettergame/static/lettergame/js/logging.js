var startTime = undefined;
var endTime = undefined;
var hoveredArr = [];
var startHover = undefined;
var endHover = undefined;
var hovered = 'not changed';
var distractors;
var audio = undefined;
var form_data = undefined;

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

    var correct_r = $("#correct_r");

    // Log the answers, and distractions for this question
    $.ajax({
        type:'POST',
        url: "",
        data:{
            user_r:$(this).attr('value'),
            correct_r:correct_r.val(),
            time_s: startTime,
            time_e: endTime,
            'arrHov[]': hoveredArr,
            'distract[]': distractors
        },
        success:function(data){
            // // if the post is a success, modify the form for the next question
            form_data = data;
        },
        error:function(error){console.log(error)}
    });

    //
    hoveredArr = [];
    startTime = getTime();

    // Now disable all buttons
    disableAllButtons();

    // Fetching the buttons that will be needed by both decisions next
    var next_button = $("#next-button");
    // Save the pushed button
    var pushed_button = $(this);

    if (correct_r.val() === pushed_button.val()){
        // Highlight the correct answer in green
        correct_r.addClass("btn-primary");
        // Now show the next button
        next_button.addClass('btn-primary');
        next_button.removeClass('btn-danger');
        next_button.removeClass("hide");
        // Highlight the correct button
        pushed_button.addClass("btn-primary");
        pushed_button.removeClass("disabled");
        pushed_button.removeClass("btn-default");
    } else{
        // Highlight the incorrect button
        pushed_button.addClass("btn-danger");
        pushed_button.removeClass("disabled");
        pushed_button.removeClass("btn-default");
        // Get the speaker button
        var speaker_button = $("#speaker-button");
        speaker_button_img = speaker_button.find('#speaker-button-img');
        // Get the buttons for the incorrect answer
        var try_again = $("#try-again-button");
        var show_ans = $("#show-answer-button");
        // Remove the class that hides them
        try_again.removeClass("hide");
        try_again.removeClass("disabled");
        try_again.attr("disabled", false);
        show_ans.removeClass("hide");
        // Make the width of those buttons be correct
        try_again.width(speaker_button_img.css("width"));
        show_ans.width(speaker_button_img.css("width"));
        // Make the height of those buttons be correct
        try_again.height(((speaker_button_img.height() - speaker_button_img.height() * 0.05)/2) +  "px");
        show_ans.height(((speaker_button_img.height() - speaker_button_img.height() * 0.05)/2) +  "px");
        // Getting the layout right
        try_again.css("margin", speaker_button_img.height() * 0.075);
        show_ans.css("margin", speaker_button_img.height() * 0.075);
        // Hide the speaker
        speaker_button.addClass("hide");
    }
});

$(document).on('click', '#try-again-button', function(e){
    // The incorrect button was pressed and the person wants to try again

    // Enable all buttons and remove the Next button
    enableAllButtons();
    $("#next-button").addClass("hide");

    // Show the speaker again and remove the wrong buttons
    // Get the speaker button
    var speaker_button = $("#speaker-button");
    speaker_button.removeClass("hide");
    // Get the buttons for the incorrect answer
    var try_again = $("#try-again-button");
    try_again.addClass("hide");
    var show_ans = $("#show-answer-button");
    show_ans.addClass("hide");
});

$(document).on('click', '#show-answer-button', function(e){
    // The incorrect button was pressed and the person wants to show the answer
    // Disable all the answer buttons
    var buttons = getInputFormButtons();
    var next_button = $("#next-button");

    // Highlight the button with the correct answer
    var correct_r = $("#correct_r");
    for (var i = 0; i < buttons.length; i++){
        if (correct_r.val() === $(buttons[i]).val()){
            // Show the correct answer
            $(buttons[i]).addClass("btn-primary");
            $(buttons[i]).removeClass('btn-default');
            break;
        }
    }

    // Show the next button
    next_button.addClass("btn-danger");
    next_button.removeClass('btn-primary');
    next_button.removeClass("hide");
    // Play the sound
    $("#speaker-button").click();

    // Disable the try-again button
    var try_again = $("#try-again-button");
    try_again.addClass("disabled");
    try_again.attr("disabled", true);
});

function disableAllButtons(){
    // Disable all the answer buttons
    var buttons = getInputFormButtons();

    // Go through every button and disable it
    for (var i = 0; i < buttons.length; i++){
        $(buttons[i]).addClass("disabled");
        $(buttons[i]).attr("disabled", true);
    }
}

function enableAllButtons() {
    // Enable all the answer buttons
    var buttons = getInputFormButtons();

    // Go through every button and disable it
    for (var i = 0; i < buttons.length; i++){
        $(buttons[i]).addClass("btn-default");
        $(buttons[i]).removeClass("disabled");
        $(buttons[i]).removeClass("btn-primary");
        $(buttons[i]).removeClass("btn-danger");
        $(buttons[i]).attr("disabled", false);
    }
}

function getInputFormButtons(){
    // Disable all the answer buttons
    return $("#game_ans").find('.submit_answer');
}

$(document).on('click', '#next-button', function (e) {
    // Clear the screen, show the speaker and modify the form
    var next_button = $("#next-button");
    next_button.addClass('hide');

    // Show the new answer
    modifyForm('game_ans', form_data);

    // Remove the wrong answer button if they are showing
    $('#try-again-button').addClass('hide');
    $('#show-answer-button').addClass('hide');
    // Now show the speaker
    $('#speaker-button').removeClass('hide');
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
