var stack = [], 
    current_slide,
    slide_list, 
    vocab_slides, 
    audioFileLocation, 
    audio;

// for future development to allow the site to display either full sro or syllabics
var use_syllabic = true;

// button colors
var mouse_off = '#94d6af',
    mouse_hover = '#7fb896',
    sound_radius = '20px';

$(document).ready(function(){
    vocab_slides = JSON.parse(document.getElementById('vocab_slides').textContent);
    slide_list = Object.keys(vocab_slides);
    // console.log(vocab_slides);
    // console.log(slide_list);
    // set up the first slide
    slideSetup();
    // on next and back button click
    $('#back-button').on('click', getPreviousSlide);
    $('#next-button').on('click', getNextSlide);
});

function slideSetup(){
    // grabs the first slide name from the 
    current_slide = slide_list.shift();
    // show slide
    showSlide();
    // show next button
    var next_button = $("#next-button");
    next_button.removeClass('btn-light');
    next_button.addClass('btn-primary');
}

function showSlide(){
    var img_url = '/media/images/' + vocab_slides[current_slide].image,
        sound_url = '/media/sounds/' + encodeURIComponent(vocab_slides[current_slide].sound);
    // show image
    $('#vocab-img').replaceWith(
        "<img id='vocab-img' class='mt-2 mb-0' src='"+img_url+"'/>"
    );

    $('#vocab-img').height(300);
    // show phrase and sound
    $('#phrase').replaceWith(buildPhraseDiv(vocab_slides[current_slide]));
    // sound button set up
    $('#sound-button').css("border-radius", sound_radius);
    $('#sound-button').css("background-color",mouse_off);
    // Get the audio file and click the speaker
    setSound(sound_url);
}

function buildPhraseDiv(slide){
    // determine whether we want to display sro or syllabics
    if (use_syllabic) {
        cree = slide.syllabic.split(',');
    }
    else {
        cree = slide.sro.split(',');
    }
    // split the translation into an array and start the phrase table html code
    var translation = slide.translation.split(','),
        phrase_table_str = '<div id="phrase">';
    
    var i;
    phrase_table_str += '<div class="row mt-3 mb-2" id="sound-button">';
    for (i=0; i<cree.length; i++) {
        phrase_table_str += '<div class="btn col btn-lg" data-toggle="tooltip" data-placement="right" title="Click to play">'
                            + cree[i]+'</div>'
    }
    phrase_table_str += '</div><div class="row mb-3">'
    for (i=0; i<translation.length; i++) {
        phrase_table_str += '<div class="col inline">'+ translation[i]+'</div>'
    }
    phrase_table_str += '</div></div>';
    
    return phrase_table_str;
}

function getNextSlide(){
    var next_button = $("#next-button");
    var back_button = $("#back-button");
    if (slide_list.length > 0) {
        stack.push(current_slide);
        current_slide = slide_list.shift();
        // show slide
        showSlide();
        // set up back button
        back_button.removeClass('btn-light');
        back_button.addClass('btn-primary');
        if (slide_list.length < 1){
            disableButton(next_button);
        }
    }
}

function disableButton(button){
    button.removeClass('btn-primary');
    button.addClass('btn-light');
}

function getPreviousSlide(){
    var back_button = $('#back-button');
    var next_button = $("#next-button");
    if (stack.length > 0) {
        // add the current slide back to slide_list
        slide_list.unshift(current_slide);
        // get previous slide
        current_slide = stack.pop();
        // show slide
        showSlide();
        // set up next button
        next_button.addClass('btn-primary');
        next_button.removeClass('btn-light');
        if (stack.length < 1){
            disableButton(back_button);
        }
    }
    
}

function setSound(sound_url){
    // Get the audio file from the server
    audio = new Audio(sound_url, playAudio);
    // click the speaker button to play the audio
    $('#sound-button').hover(
        function () {
            $('#sound-button').css("background-color",mouse_hover);
        },
        function() {
            $('#sound-button').css("background-color",mouse_off);
        }
        
    );
    $("#sound-button").on('click', playAudio);
}

function playAudio(){
    // Function plays the audio
    audio.play();
}

