$(function() {

    $('#login-form').click(function(e) {
        $("#login-form")
            .delay(100)
            .fadeIn(100)
            .addClass('active');
        $("#signup-form")
            .fadeOut(100)
            .removeClass('active');
        e.preventDefault();
    });
    $('#signup-form').click(function(e) {
        $("#signup-form")
            .delay(100)
            .fadeIn(100);
        $("#login-form")
            .fadeOut(100)
            .removeClass('active');

        $(this).addClass('active');
        console.log($(this));
        e.preventDefault();
    });

});