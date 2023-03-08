var modal = document.getElementById("thanks-modal");
var span = $(".close")[0];
var message_error = "<h4>Error!</h4><p style='text-align: center;'>Error on submit. Please try again.</p>"

span.onclick = function() {
    $('#thanks-modal').fadeOut();
}
window.onclick = function(event) {
    if (event.target == modal) {
        $('#thanks-modal').fadeOut();
    }
}

function showError(error, form_field) {
    form_field.attr('value', '');
    form_field.addClass('contactFormError');
    form_field.attr('placeholder', error);
}

function subscribeSubmitAction(e){
    submitAction(e, '/ajax-posting/', '#subscribe_form');
}

function blogSubscribeSubmitAction(e){
    submitAction(e, '/ajax-posting/', '#blog_subscribe_form');
}

function blogUnsubscribeSubmitAction(e){
    submitAction(e, '/ajax-unsubscribe/', '#blog_unsubscribe_form');
}

function submitAction(e, url, form_id){
    e.preventDefault();
    var name = $(form_id).find('input[name="name"]');
    var email = $(form_id).find('input[name="email"]');
    var valid_name = typeof name.val() !== 'undefined' && name.val() != '';
    var re = /^(([^<>()\[\]\.,;:\s@\"]+(\.[^<>()\[\]\.,;:\s@\"]+)*)|(\".+\"))@(([^<>()[\]\.,;:\s@\"]+\.)+[^<>()[\]\.,;:\s@\"]{2,})$/i;
    var valid_email = re.test(email.val());
    var token = $(form_id).find('iframe').contents().find('#iframe-csrf').attr('value');

    if (!valid_name) {
        showError('Please enter your name', name);
    }
    if (!valid_email) {
        showError('Please enter a valid e-mail', email);
    } 
    if (valid_name && valid_email) {
        window.localStorage.setItem(form_id, new Date());
        $('#loading-spinner').html('<img src="/static/img/spin.gif">');
        $.ajax({
            type : "POST", 
            url: url,
            data: {
                name: name.val(),
                email: email.val(),
                form_id: form_id,
                csrfmiddlewaretoken: token,
                url: window.location.href,
                dataType: "json",
            },
            success: function(data){
                email.val('');
                name.val('');
                $('#loading-spinner').html('');
                email.removeClass('contactFormError');
                name.removeClass('contactFormError');
                email.attr('placeholder', 'your@email.com');
                name.attr('placeholder', 'your name');
                if (data.subscribed) {
                    $("#thanks-text").html(data.message_content);
                } else if (data.unsubscribed) {
                    $("#thanks-text").html(data.message_content);
                } else if (data.failed) {
                    $("#thanks-text").html(data.message_content);
                } else {
                    $("#thanks-text").html(data.message_content);
                }
                $('#thanks-modal').fadeIn();
            },
            error: function(){
                $("#thanks-text").html(message_error);
                $('#thanks-modal').fadeIn();
            }
        });
    }
}

$('#subscribe_form').on('submit', subscribeSubmitAction);
$('#blog_subscribe_form').on('submit', blogSubscribeSubmitAction);
$('#blog_unsubscribe_form').on('submit', blogUnsubscribeSubmitAction);

$('#blog_unsubscribe_newsletter').on('change', function(){
    if ($(this).is(':checked')) {
        $('.blog-subscribe-form').hide();
        $('#blog_unsubscribe_name')
            .attr('value', 'Unknown')
            .hide();
        $('#blog_unsubscribe_email')
            .attr('value', '');
        $('.blog-unsubscribe-form').show();
    } else {
        $('.blog-unsubscribe-form').hide();
        $('#blog_unsubscribe_name')
            .attr('value', 'Unknown');
        $('#blog_unsubscribe_email')
            .attr('value', '');
        $('.blog-subscribe-form').show();
    }
});

$.each([
    '#subscribe_email',
    '#subscribe_name',
    '#blog_subscribe_email',
    '#blog_subscribe_name'], 
    function(_, id){
    $(id).focus(function(){
        $(id).attr('placeholder', '');
    });
});

$.each([
    '#subscribe_email',
    '#blog_subscribe_email'],
    function(_, id){
    $(id).focusout(function(){
        $(id)
            .attr('placeholder', 'your@email.com')
            .removeClass('contactFormError');
    });
});

$.each(['#subscribe_name', '#blog_subscribe_name'], function(_, id){
    $(id).focusout(function(){
        $(id)
            .attr('placeholder', 'your name')
            .removeClass('contactFormError');
    });
});
