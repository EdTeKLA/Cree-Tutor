$(function() {

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