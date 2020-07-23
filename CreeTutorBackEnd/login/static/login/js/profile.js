$(window).resize(function() {
    // This will execute whenever the window is resized
    // deal with the drop down menu for mobile screen display
    navBar()
});

function navBar(){
    console.log('hello')
    if ($(window).width() < 975 ) {
        $('#small-screen-nav').show();
        $('#wide-screen-nav').hide();
    }
    else if ($(window).width() >= 975 ) {
        $('#small-screen-nav').hide();
        $('#wide-screen-nav').show();
    }
}

$(document).ready(function(){
    // format the menu burger
    navBar()
    /* Edit button functions for the main profile page and language page */
    // Main profile information button functionality
    // Show the profile editing form when the Edit button is clicked
    $('a#name-form-button').click(function() {
        $('#name-details').hide();
        $('a#name-form-button').hide();
        $('#name-form').show();
    });
    $('a#gender-form-button').click(function() {
        $('#gender-details').hide();
        $('a#gender-form-button').hide();
        $('#gender-form').show();
    });
    $('a#age-form-button').click(function() {
        $('#age-details').hide();
        $('a#age-form-button').hide();
        $('#age-form').show();
    });

    // Revert back to static display of user profile when form editing is cancelled
    $('#name-form-cancel-button').click(function() {
        $('#name-details').show();
        $('a#name-form-button').show();
        $('#name-form').hide();
    });
    $('#gender-form-cancel-button').click(function() {
        $('#gender-details').show();
        $('a#gender-form-button').show();
        $('#gender-form').hide();
    });
    $('#age-form-cancel-button').click(function() {
        $('#age-details').show();
        $('a#age-form-button').show();
        $('#age-form').hide();
    });

    // Email section button functionality
    // Show email editing form when email Edit button is clicked
    $('#email-form-button').click(function() {
        $('#email').hide();
        $('#email-form').show();
    });
    // Revert back to static display of user email when form editing is cancelled
    $('#email-form-cancel-button').click(function() {
        $('#email-form').hide();
        $('#email').show();
    });
});