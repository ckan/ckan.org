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
    form.find("input[name='g-recaptcha-response']").remove();
    form.append("<input type='hidden' name='g-recaptcha-response' value='" + token + "' />");
    form.find('input[type="submit"]').click();
}

function onRecaptchaLoadCallback() {
    renderRecaptchas(window.RECAPTCHA_SITE_KEY);
}

// --- Generic invisible reCAPTCHA helper -----------------------------------
// Used by custom/AJAX forms (e.g. the success-stories submission forms) that
// are not plain <form> submits handled by the code above. Returns a Promise
// that resolves with a fresh token, or an empty string if reCAPTCHA is
// unavailable (the server then rejects the submission).
var recaptchaExtraWidgets = {};
var recaptchaExtraCallbacks = {};

function waitForRecaptcha() {
    return new Promise(function (resolve) {
        if (typeof grecaptcha !== 'undefined' && typeof grecaptcha.ready === 'function') {
            resolve();
            return;
        }
        var attempts = 0;
        var timer = setInterval(function () {
            if (typeof grecaptcha !== 'undefined' && typeof grecaptcha.ready === 'function') {
                clearInterval(timer);
                resolve();
            } else if (++attempts > 100) { // ~10s
                clearInterval(timer);
                resolve();
            }
        }, 100);
    });
}

function getRecaptchaToken(selector) {
    return waitForRecaptcha().then(function () {
        return new Promise(function (resolve) {
            if (typeof grecaptcha === 'undefined' || !window.RECAPTCHA_SITE_KEY) {
                resolve('');
                return;
            }
            var container = document.querySelector(selector);
            if (!container) {
                resolve('');
                return;
            }
            grecaptcha.ready(function () {
                if (!recaptchaExtraWidgets[selector]) {
                    recaptchaExtraWidgets[selector] = grecaptcha.render(container, {
                        'sitekey': window.RECAPTCHA_SITE_KEY,
                        'size': 'invisible',
                        'callback': function (token) {
                            var cb = recaptchaExtraCallbacks[selector];
                            if (cb) {
                                recaptchaExtraCallbacks[selector] = null;
                                cb(token);
                            }
                        }
                    });
                } else {
                    grecaptcha.reset(recaptchaExtraWidgets[selector]);
                }
                recaptchaExtraCallbacks[selector] = resolve;
                grecaptcha.execute(recaptchaExtraWidgets[selector]);
            });
        });
    });
}
