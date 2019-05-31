/*
File was created to get the feedback from a user, submit it and redirect.
 */

function processFeedbackAnswersAndSend(e, field_set_names, story_id, session_id){
    /*
    Function sents the information about the feedback back to the server and redirects.
     */
    // Preventing the page from refreshing
    e.preventDefault();

    // Get all the answers
    var answers = {};
    for (var i = 0; i < field_set_names.length; i++){
        answers[field_set_names[i]] = $('#q_' + field_set_names[i] + '_field_set input:radio:checked').val();
    }
    console.log(answers);
    // Now send of information to server
    $.ajax({
        type:'POST',
        url: "/shadowing/feedback/" + story_id + "/" + session_id + "/",
        data:{
            "answers": JSON.stringify(answers),
        },
        success:function(data){
            window.location.href = data['redirect'];
        },
        error:function(error) {
            $("#error_message").removeClass("hide");
            $("#error_message span").text("An unknown error occured.");
            console.log(error);
        }
    });
}