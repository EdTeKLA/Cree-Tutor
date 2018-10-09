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
                var message = document.createElement("div");
                message.innerHTML = data['error'];
                document.body.appendChild(message);
            }
            else if (data['success']){
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
            if (data['error']){
                var message = document.createElement("div");
                message.innerHTML = data['error'];
                document.body.appendChild(message);
                console.log(data);
            }
            else if (data['redirect']){
                console.log(data);
                window.location.href = data['redirect'];
            }
        },
        error:function(error){console.log(error)}
    });
});
