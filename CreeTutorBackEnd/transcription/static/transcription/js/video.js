// These two vars were created to handle
var currentSentence = 60;
var currentInput = "~";
var currentLetter = 0;
var cursorModeTimer = 0;
var cursorMode = 1;
var cursorModeLength = 500;
var letterCorrect = true;

function sendPostRequestForLogging(action, time, story_id, session_id){
    // Sent a POST request to log that a story has been selected/played/paused/finished
    $.ajax({
        type:'POST',
        url: "/transcription/log/" + story_id + "/" + action +  "/" + time + "/" + session_id + "/"  + currentInput +
            "/",
        data:{
        },
        success:function(data){
            // Do nothing
        },
        error:function(error){console.log(error)}
    });
}
function updateProgressBar() {
    // Updating progress bar
    $('.progress-bar').css({"width": (($("#trans_video").get(0).currentTime/$("#trans_video").get(0).duration) * 100 + "%")});
}

function makePlayActive(callback){
    // Check if both the required components have finished work
    $('#loading-spinner').remove();
    $('#play-button').removeClass("hide");
    callback();
}

function handleKeyPress(textInputActivated, time_stamped_sentences, video, keyCode, errorShownDuration, playButton, story_id, session_id){
    if (textInputActivated) {
        if (currentInput === "~") {
            currentInput = "";
        }

        currentInput += String.fromCharCode(keyCode).toLowerCase();
        // Convert the video time to milliseconds
        // If the current letter is the same as the keycode, advance it.
        console.log(time_stamped_sentences[currentSentence][2][currentLetter]);
        if (time_stamped_sentences[currentSentence][2][currentLetter].toLowerCase() === String.fromCharCode(keyCode).toLowerCase()
            || time_stamped_sentences[currentSentence][2][currentLetter] === "'" && keyCode === 222
            || time_stamped_sentences[currentSentence][2][currentLetter] === "’" && keyCode === 222
            || time_stamped_sentences[currentSentence][2][currentLetter] === "“" && keyCode === 222
            || time_stamped_sentences[currentSentence][2][currentLetter] === "\"" && keyCode === 222
            || time_stamped_sentences[currentSentence][2][currentLetter] === "”" && keyCode === 222
            || time_stamped_sentences[currentSentence][2][currentLetter] === "‘" && keyCode === 222
        ){
            // Changes the color of the letter if correct
            $("#transcription_sentence_"+currentSentence+"_letters_"+currentLetter).addClass("doneText");
            letterCorrect = true;
            // Increments the letter
            currentLetter++;
        } else {
            letterCorrect = false;
        }

        // If the sentence has been finished, change currentSentence to next and reset currentLetter
        if (currentLetter >= time_stamped_sentences[currentSentence][2].length){
            currentSentence++;
            currentLetter = 0;
            playButton.trigger('resume_video');
            // Log the input
            sendPostRequestForLogging("sentence_completed", video.currentTime * 1000, story_id, session_id);
            currentInput = "~";
        }
        console.log(keyCode+", "+String.fromCharCode(keyCode));
        console.log(currentLetter);
    } else {
        showError("Click on the text before continuing activity.", errorShownDuration)
    }
}

function cursorBlink() {
    // Increment the timer on the cursor
    cursorModeTimer += 10;
    // If the timer is over 250, meaning 250 ms have passed, flip cursor more and reset timer
    if (cursorModeTimer > cursorModeLength) {
        if (cursorMode === 1) {
            cursorMode = 0;
        } else {
            cursorMode = 1;
        }
        cursorModeTimer = 0;
    }
    // Increment the time
    // Disable all the last few active letters
    for (var i = -25; i < 0; i++){
        var inactiveLetters = $("#transcription_sentence_"+currentSentence+"_letters_"+(currentLetter - 1));
        // Remove all cursor styling from the last few inactive letter
        inactiveLetters.removeClass("cursorIncorrectBackground");
        inactiveLetters.removeClass("cursorActiveBackground");
    }
    // The current active letter
    var currentActiveLetter = $("#transcription_sentence_"+currentSentence+"_letters_"+currentLetter);
    // For the current letter, check if user got it correct or incorrect
    if (cursorMode === 1) {
        if (letterCorrect) {
            currentActiveLetter.removeClass("cursorIncorrectBackground");
            currentActiveLetter.addClass("cursorActiveBackground")
        } else {
            currentActiveLetter.removeClass("cursorActiveBackground");
            currentActiveLetter.addClass("cursorIncorrectBackground")
        }
    } else {
        currentActiveLetter.removeClass("cursorActiveBackground");
        currentActiveLetter.removeClass("cursorIncorrectBackground");
    }
}

// Check if can play according to correct sentences
function canPlay(video, time_stamped_sentences) {
    var whichRange = 0;
    for (var i = 0; i < time_stamped_sentences.length; ++i) {
        var time_in_milli = video.currentTime * 1000;
        if (time_in_milli >= time_stamped_sentences[i][0] && time_in_milli <= time_stamped_sentences[i][1]) {
            whichRange = i;
        }
    }

    if (currentSentence >= whichRange){
        return true;
    } else {
        return false;
    }
}

function showActiveSentenceAndUpdateProgressBar(video, time_stamped_sentences, story_id, session_id) {
    // Make all the sentences disappear, then only show actice sentenes
    // Called to check which word should be highlighted every 33 milliseconds
    // 33 milliseconds because thats more than enough for smooth playback
    // Itereate thorugh all the sentences, hide the ones that are not active
    for (var i = 0; i < time_stamped_sentences.length; ++i) {
        if (currentSentence === i) {
            $("#transcription_sentence_" + i).removeClass("hide");
        } else {
            $("#transcription_sentence_" + i).addClass("hide");
        }
    }

    if (textInputActivated != true) {
        $("#text_input").addClass("inactive_text_color");
    } else {
        $("#text_input").removeClass("inactive_text_color");
    }

    // Afterwards, check if the current range index is equal to sentence number, if not, stop video
    if(canPlay(video, time_stamped_sentences) && playing) {
        $('#play_button').triggerHandler('play_video');
    } else {
        $('#play_button').triggerHandler('stop_video');
    }

    // If the video is finished, show the finished button
    if ($("#trans_video").get(0).currentTime >= $("#trans_video").get(0).duration) {
        $("#finished_button").removeClass("hide");
    }
}

// Stores the current error number, to make sure that the error is removed after the last error, not before.
var currentErrorNumberShown = 0;

function showError(errorText, duration) {
    // Function was created to show errors
    $("#error_message").removeClass("hide");
    $("#error_message span").text(errorText);
    currentErrorNumberShown += 1;
    setTimeout(removeError, duration, currentErrorNumberShown);
}

function removeError(errorNumber) {
    // Function was created to hide errors
    // Make sure the error was not changed after the timeout was set
    // If it was, leave it alone
    if (errorNumber == currentErrorNumberShown){
        $("#error_message").addClass("hide");
        $("#error_message span").text("");
    }
}