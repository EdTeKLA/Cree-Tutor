function showError(toError, toShow, toAddErrorMessage, errorMessage) {
    toError.addClass('error');
    toShow.removeClass('hidden');
    toAddErrorMessage.text(errorMessage);
}

function hideError(toUnError, toHide) {
    toUnError.removeClass('error');
    toHide.addClass('hidden');
}

function shouldDisableSignUp() {

    return $("#email").hasClass('error') ||
        $("#confirm-password").hasClass('error') ||
        $("#email").val().length === 0
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
        } else if (confirmPassword.hasClass('error')) {
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
        } else if (confirmPassword.hasClass('error')) {
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
        } else if (email.hasClass('error')) {
            hideError(email, $("#email-group .form-field-message"));
            $('#signup-button').prop('disabled', shouldDisableSignUp());
        }
    });

    function getCookie(name) {
        var cookieValue = null;
        if (document.cookie && document.cookie !== '') {
            var cookies = document.cookie.split(';');
            for (var i = 0; i < cookies.length; i++) {
                var cookie = jQuery.trim(cookies[i]);
                // Does this cookie string begin with the name we want?
                if (cookie.substring(0, name.length + 1) === (name + '=')) {
                    cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                    break;
                }
            }
        }
        return cookieValue;
    }

    var csrftoken = getCookie('csrftoken');

    function csrfSafeMethod(method) {
        // these HTTP methods do not require CSRF protection
        return (/^(GET|HEAD|OPTIONS|TRACE)$/.test(method));
    }


    $.ajaxSetup({
        beforeSend: function(xhr, settings) {
            if (!csrfSafeMethod(settings.type) && !this.crossDomain) {
                xhr.setRequestHeader("X-CSRFToken", csrftoken);
            }
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
                } else if (data['success']) {
                    // TODO: instant login and redirect to profile page instead?
                    // should be first time profile page, then tell user where they can go edit their details at any time?
                    $("#login-form")
                        .delay(200)
                        .fadeIn(200);
                    $("#signup-form")
                        .fadeOut(200);
                    $(this).addClass('active');
                    $("#signup-form-tab").removeClass('active');
                    document.getElementById("login_email").value = $("#email").val();
                    document.getElementById("login_password").value = $("#password").val();
                    e.preventDefault();
                }
            },
            error:function(error){console.log(error)}
        });
    });

    $(document).on('submit', '#login-form', function(e){
        e.preventDefault();

        $.ajax({
            type:'POST',
            url: "/signin/",
            data:{
                password: $("#login_password").val(),
                email: $("#login_email").val()
            },
            success:function(data){
                if (data['error']) {
                    $(".form-group .form-message").removeClass("hidden");
                    $(".form-group .form-message span").text(data.error);
                } else if (data['redirect']) {
                    console.log(data);
                    window.location.href = data['redirect'];
                }
            },
            error:function(error){console.log(error)}
        });
    });
});