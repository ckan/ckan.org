var form = ''
$('.captcha-submit').on('click', function (event) {
    event.preventDefault();
    form = '#' + $(this).attr('data-form-id');

    if ($(form)[0].checkValidity() == true) {
        grecaptcha.execute();
    } else { 
        $(form).find('input[type="submit"]').click();
    }
});

var onSubmit = function(token) {
    $(form).append("<input type='hidden' name='g-recaptcha-response' value='" + token + "' />");
    $(form).find('input[type="submit"]').click();
};
