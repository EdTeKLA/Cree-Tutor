function goBack(audioFile){
    // Send the user back after back button is clicked
    window.history.back();
}

function getAudioFile(callback, location, story_id){
    // Sent a POST request to log that a story has been selected
    sendPostRequestForLogging("select", 0.0, story_id);

    // Load the audio
    audio_obj = new Audio(location);
    callback(audio_obj);
}

function sendPostRequestForLogging(action, time, story_id){
    // Sent a POST request to log that a story has been selected/played/paused/finished
    $.ajax({
        type:'POST',
        url: "/shadowing/log/" + story_id + "/" + action +  "/" + time + "/",
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
        var baselineEstablised = false;

        var context = new AudioContext();
        var source = context.createMediaStreamSource(stream);
        var processor = context.createScriptProcessor(2048, 1, 1);
        var analyser = context.createAnalyser();

        source.connect(analyser);
        analyser.connect(processor);

        // Baseline created at the start, it runs for 5 seconds
        var baseline = -1;
        // Time we get access to the microphone
        var date = new Date();
        var microphoneAccessTime = date.getTime();
        // Baseline time, this will tell the script how long the baseline should last
        // Seconds * 1000
        var baselineTime = 3000;
        // Stepsize for update rule
        alpha = 0.1;

        // Processing when there is audio input
        processor.onaudioprocess = function () {
            // Process the frequency of the input coming in
            var array = new Uint8Array(analyser.frequencyBinCount);
            analyser.getByteFrequencyData(array);
            var values = 0;

            // Values for average
            var length = array.length;
            for (var i = 0; i < length; i++) {
                values += (array[i]);
            }

            // Perform average
            var average = values / length;

            var date = new Date();
            // Perform baseline update if within the time limit
            if (date.getTime() - microphoneAccessTime <= baselineTime){
                // Check if baseline is 0, if yes, this is the first its being called
                if (baseline == -1){
                    baseline = average;
                } else {
                    // Baseline isn't 0
                    baseline = baseline + alpha * (average - baseline);
                    // console.log("Baseline: " + baseline + "\t\t Average: " + average);
                }
            } else {
                if (baselineEstablised == false){
                    baselineEstablised = true;
                    callback();
                }
                // Print the average, for debugging/testing
                // console.log("Not baseline: " + average);
            }
        }
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

function makePlayActive(baselineStatus, downloadStatus, audio, callback){
    // Check if both the required components have finished work
    if (baselineStatus && downloadStatus && audio != null) {
        $('#loading-spinner').remove();
        $('#play-button').removeClass("hide");
        callback();
    }
}

var finished = false;

function highLightActiveWordAndProgressBar(audio, time_stamped_words, story_id) {
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
        sendPostRequestForLogging("finish", audio.currentTime, story_id);
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
