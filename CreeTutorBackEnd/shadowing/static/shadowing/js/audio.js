function sendPostRequestForLogging(action, time, story_id, session_id){
    // Sent a POST request to log that a story has been selected/played/paused/finished
    $.ajax({
        type:'POST',
        url: "/shadowing/log/" + story_id + "/" + action +  "/" + time + "/" + session_id + "/",
        data:{
        },
        success:function(data){
            // Do nothing
        },
        error:function(error){console.log(error)}
    });
}

function microphoneLevels(callback){
    var handleSuccess = function(stream) {
        accessToMicGranted = true;
        callback();
    };

    // If we successfully got access to the microphone, call handleSuccess
    navigator.mediaDevices.getUserMedia({ audio: true, video: false })
        .then(handleSuccess)
        .catch(showMicrophoneError)

}

function showMicrophoneError() {
    // Function was created to show microphone error incase the device does not have a microphone or the user denies us
    // access
    $("#error_message").removeClass("hide");
    $("#error_message span").text("Microphone access needed to perform this activity, " +
        "please refresh and allow microphone access.");
}

function makePlayActive(accessToMicGranted, downloadStatus, audio, callback){
    // Check if both the required components have finished work
    if (accessToMicGranted && downloadStatus && audio != null) {
        $('#loading-spinner').remove();
        $('#play-button').removeClass("hide");
        $('#rewind-button').removeClass("hide");
        $('#rewind_button').removeClass("hide");
        callback();
    }
}

var finished = false;

function highLightActiveWordAndProgressBar(audio, time_stamped_words, story_id, session_id) {
    // Make all the words black
    // Called to check which word should be highlighted every 33 milliseconds
    // 33 milliseconds because thats more than enough for smooth playback
    if (audio.currentTime < audio.duration) {
        var time_in_milli = audio.currentTime * 1000;
        // Iterate through every words, check if the word should be highlighted, if yes, change
        // the styling of the word and the words around it
        for (var i = 0; i < time_stamped_words.length; ++i) {
            if (time_in_milli > time_stamped_words[i][0] && time_in_milli < time_stamped_words[i][1]) {
                changeColorOfWordWithPrefixAndIndex("shadowing_word_", i, time_stamped_words.length);
                break;
            }
        }

        // Updating progress bar
        $('.progress-bar').css({"width": ((audio.currentTime/audio.duration) * 100 + "%")});
    } else if (audio.currentTime >= audio.duration && !finished){
        finished = true;
        // If the current time is equal to the end time.
        $(".shadowing_word_span").css('color', '#000000');
        $("#finished_button").removeClass("hide");
        $("#play_button").addClass("disabled");
        $("#play_button").attr("disabled", true);
        sendPostRequestForLogging("finish", audio.currentTime, story_id, session_id);
    }
}

function changeColorOfWordWithPrefixAndIndex(prefix, index, max){
    super_dark_red_words = 4;
    dark_red_words = 2;
    // Make all words red
    $(".shadowing_word_span").css('color', '#000000');
    // Iterate through 4 times
    // Set the words to be super dark
    for (var i = dark_red_words; i <= super_dark_red_words; ++i){
        if ((index - i) > -1){
            $("#" + prefix + (index - i)).css('color', '#724141');
        }
        if ((index + i) < max){
            $("#" + prefix + (index + i)).css('color', '#724141');
        }
    }

    // Iterate through 2 times for darker but not super dark words
    for (i = 0; i <= dark_red_words; ++i){
        if ((index - i) > -1){
            $("#" + prefix + (index - i)).css('color', '#9F3838');
        }
        if ((index + i) < max){
            $("#" + prefix + (index + i)).css('color', '#9F3838');
        }
    }

    // Make the current work, bright red.
    $("#" + prefix + index).css('color', '#DD2E2E');
}
