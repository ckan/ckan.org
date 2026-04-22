var recaptchaWidgets = {};

function renderRecaptchas(sitekey) {
    // Find all forms that contain a button with class 'captcha-submit'
    $('form').has('.captcha-submit').each(function() {
        var formId = $(this).attr('id');
        if (!formId) {
            // Skip forms without an ID
            return;
        }
        var containerId = 'recaptcha-container-' + formId;
        // If the container does not exist, create it at the end of the form
        if ($('#' + containerId).length === 0) {
            $(this).append('<div id="' + containerId + '"></div>');
        }
        recaptchaWidgets[formId] = grecaptcha.render(containerId, {
            'sitekey': sitekey,
            'size': 'invisible',
            'callback': function(token) {
                onSubmit(token, formId);
            }
        });
    });
}

$('.captcha-submit').on('click', function (event) {
    event.preventDefault();
    var formId = $(this).attr('data-form-id');
    var form = '#' + formId;
    if ($(form)[0].checkValidity() == true) {
        grecaptcha.execute(recaptchaWidgets[formId]);
    } else { 
        $(form).find('input[type="submit"]').click();
    }
});

function onSubmit(token, formId) {
    var form = $('#' + formId);
    form.append("<input type='hidden' name='g-recaptcha-response' value='" + token + "' />");
    form.find('input[type="submit"]').click();
}

function onRecaptchaLoadCallback() {
    renderRecaptchas(window.RECAPTCHA_SITE_KEY);
}
