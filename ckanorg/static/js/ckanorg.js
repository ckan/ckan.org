var modal = document.getElementById("thanks-modal");
var span = $(".close")[0];
var thanks = "<h4>Thank you for getting in touch!</h4><p>We’ll get back to you within one business day!</p>"
var blog_thanks = "<h4>Thank you for subscribing our blog!</h4>"

span.onclick = function() {
    $('#thanks-modal').fadeOut();
}
window.onclick = function(event) {
    if (event.target == modal) {
        $('#thanks-modal').fadeOut();
    }
}

function showError(error, form_id) {
    $(form_id)[0].value = '';
    $(form_id).addClass('contactFormError');
    $(form_id).attr('placeholder', error);
}

function webinarSubmitAction(e){
    submitAction(e, '#webinar_email');
}

function stewardSubmitAction(e){
    submitAction(e, '#steward_email');
}

function stewardSendSubmitAction(e){
    submitAction(e, '#steward_email_send');
}

function blogSubmitAction(e){
    submitAction(e, '#blog_email');
}

function isTooFast(form_id) {
    var now = new Date();
    var minutes = 1;
    var delta = minutes * 60 * 1000;
    var item = window.localStorage.getItem(form_id);
    if (item) {
        var was_set = new Date(item);
        var current_delta = now - was_set;
        if (current_delta < delta) {
            return true;
        } else {
            window.localStorage.removeItem(form_id);
            return false;
        }
    } else {
        return false
    }
}

function submitAction(e, form_id){
    e.preventDefault();
    var re = /^(([^<>()\[\]\.,;:\s@\"]+(\.[^<>()\[\]\.,;:\s@\"]+)*)|(\".+\"))@(([^<>()[\]\.,;:\s@\"]+\.)+[^<>()[\]\.,;:\s@\"]{2,})$/i;
    var valid = re.test($(form_id)[0].value);
    var token = $(form_id)[0]['form'].querySelector(
        'iframe').contentDocument.getElementById(
            'iframe-csrf').getAttribute('value');
    if (!valid) {
        showError('Please enter a valid e-mail', form_id);
    } else {
        var too_fast = isTooFast(form_id);
        if (too_fast) {
            showError('Please try again later', form_id);
        } else {
            window.localStorage.setItem(form_id, new Date());
            $(form_id).addClass('waiting');
            $.ajax({
                type : "POST", 
                url: "/ajax-posting/",
                data: {
                    email: $(form_id).val(),
                    form_id: form_id,
                    csrfmiddlewaretoken: token,
                    dataType: "json",
                },
                success: function(data){
                    $(form_id)[0].value = '';
                    $(form_id).removeClass('waiting');
                    $(form_id).removeClass('contactFormError');
                    $(form_id).attr('placeholder', 'Your email');
                    if (form_id == "#blog_email") {
                        $("#thanks-text").html(blog_thanks)
                    } else {
                        $("#thanks-text").html(thanks)
                    }
                    $('#thanks-modal').fadeIn();
                },
                error: function(){
                    showError('Error on submit. Please try again.');
                }
            });
        }
    }
}

$('#webinarForm').on('submit', webinarSubmitAction);
// $('#stewardForm').on('submit', stewardSubmitAction);
// $('#stewardFormSend').on('submit', stewardSendSubmitAction);
$('#blogForm').on('submit', blogSubmitAction);

$.each(['#webinar_email', '#steward_email', '#blog_email'], function(_, id){
    $(id).focus(function(){
        $(id).attr('placeholder', '');
    });
});

$.each(['#webinar_email', '#steward_email', '#blog_email'], function(_, id){
    $(id).focusout(function(){
        $(id)
            .attr('placeholder', 'Your email')
            .removeClass('contactFormError');
    });
});
