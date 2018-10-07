$(function() {

    // When the user clicks on the login tab, show the log in form
    $('#login-form-tab').click(function(e) {
        $("#login-form")
            .delay(200)
            .fadeIn(200);
        $("#signup-form")
            .fadeOut(200);
        $(this).addClass('active');
        $("#signup-form-tab").removeClass('active');
        e.preventDefault();
    });

    // When the user clicks on the sign up tab, show the sign up form
    $('#signup-form-tab').click(function(e) {
        $("#signup-form")
            .delay(200)
            .fadeIn(200);
        $("#login-form")
            .fadeOut(200);
        $(this).addClass('active');
        $("#login-form-tab").removeClass('active');
        e.preventDefault();
    });

    // When the confirm password does not match, tell the user with the mismatch class on the input
    $('#password').on('input', function() {
        const confirmPassword = $('#confirm-password');
        if(confirmPassword.val().length > 0 && $(this).val() !== confirmPassword.val()) {
            confirmPassword.addClass('mismatch');
        } else if (confirmPassword.hasClass('mismatch')) {
            confirmPassword.removeClass('mismatch');
        }
    });
    $('#confirm-password').on('input', function() {
        const confirmPassword = $(this);
        const password = $('#password');
        if(password.val().length > 0 && password.val() !== confirmPassword.val()) {
            confirmPassword.addClass('mismatch');
        } else if (confirmPassword.hasClass('mismatch')) {
            confirmPassword.removeClass('mismatch');
        }
    });
});