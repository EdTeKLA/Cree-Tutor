function showError(toError, toShow, toAddErrorMessage, errorMessage) {
    toError.addClass('error-border');
    toShow.removeClass('hidden');
    toAddErrorMessage.text(errorMessage);
}

function hideError(toUnError, toHide) {
    toUnError.removeClass('error-border');
    toHide.addClass('hidden');
}

function shouldDisableSignUp() {

    return $("#email").hasClass('error-border') ||
        $("#confirm-password").hasClass('error-border') ||
        $("#email").val().length === 0 ||
        $("#password").val().length === 0 ||
        $("#confirm-password").val().length === 0;
}

$(function() {

    // TODO: need to clean up this code a bit to limit the queries being performed and remove duplicate code
    // TODO: need to do more testing on the error handling

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

    // When the confirm password does not match, tell the user with the error class on the input
    // Only enable the submit button when the user has entered something in both fields (and it matches)
    $('#password').on('input', function() {
        const confirmPassword = $('#confirm-password');

        if(confirmPassword.val().length > 0 && $(this).val() !== confirmPassword.val()) {
            showError(
                confirmPassword,
                $("#confirm-password-group .form-field-message"),
                $("#confirm-password-group .form-field-message span"),
                "Passwords do not match");
            $('#signup-button').prop('disabled', shouldDisableSignUp());
        } else if (confirmPassword.hasClass('error-border')) {
            hideError(confirmPassword, $("#confirm-password-group .form-field-message"));
            $('#signup-button').prop('disabled', shouldDisableSignUp());
        }
    });

    $('#confirm-password').on('input', function() {
        const confirmPassword = $(this);
        const password = $('#password');

        if(password.val().length > 0 && password.val() !== confirmPassword.val()) {
            showError(
                confirmPassword,
                $("#confirm-password-group .form-field-message"),
                $("#confirm-password-group .form-field-message span"),
                "Passwords do not match");
            $('#signup-button').prop('disabled', shouldDisableSignUp());
        } else if (confirmPassword.hasClass('error-border')) {
            hideError(confirmPassword, $("#confirm-password-group .form-field-message"));
            $('#signup-button').prop('disabled', shouldDisableSignUp());
        }
    });

    $('#email').on('focusout', function() {
        const email = $(this);

        if (email.val().match("[^@]+@[^@]+\\.[^@]+") == null) {
            showError(
                email,
                $("#email-group .form-field-message"),
                $("#email-group .form-field-message span"),
                "Email is invalid");
            $('#signup-button').prop('disabled', shouldDisableSignUp());
        } else if (email.hasClass('error-border')) {
            hideError(email, $("#email-group .form-field-message"));
            $('#signup-button').prop('disabled', shouldDisableSignUp());
        }
    });

    $(document).on('submit', '#signup-form', function(e){
        e.preventDefault();

        $.ajax({
            type:'POST',
            url: "/signup/",
            data:{
                password: $("#password").val(),
                email: $("#email").val()
            },
            success:function(data){
                if (data['error']){
                    // TODO: right now all errors sent back come from the email, this may not always be the case going forwards
                    showError(
                        $("#email"),
                        $("#email-group .form-field-message"),
                        $("#email-group .form-field-message span"),
                        data.error);
                    $('#signup-button').prop('disabled', shouldDisableSignUp());
                } else if (data['redirect']) {
                    window.location.href = data['redirect'];
                }
            },
            error:function(error) {
                console.log(error);
            }
        });
    });

    $(document).on('submit', '#login-form', function(e){
        e.preventDefault();

        $.ajax({
            type:'POST',
            url: "/signin/",
            data:{
                password: $("#login-password").val(),
                email: $("#login-email").val()
            },
            success:function(data){
                if (data['error']) {
                    $(".form-group .form-message").removeClass("hidden");
                    $(".form-group .form-message span").text(data.error);
                } else if (data['redirect']) {
                    window.location.href = data['redirect'];
                }
            },
            error:function(error){console.log(error)}
        });
    });
});