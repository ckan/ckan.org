import time
import logging
import traceback

from django.http import JsonResponse, HttpResponse
from django.shortcuts import redirect
from django.utils.encoding import force_text
from django.utils.http import urlsafe_base64_decode

from .models import Email, send_contact_info
from .token import user_activation_token
from .email import send_subscription_email


form_mapping = {
    '#subscribe_email': 'Subscribe Form',
    '#blog_subscribe_email': 'Subscribe Form',
    '#blog_email': 'Blog Subscription Form',
}

def activate_subscription(request, eidb64, token):
    try:
        eid = force_text(urlsafe_base64_decode(eidb64))
        email = Email.objects.filter(address=eid).first()
        url = request._current_scheme_host
    except(TypeError, ValueError, OverflowError, email.DoesNotExist):
        logging.getLogger("error_logger").error(traceback.format_exc())
        email = None
    if email is not None and user_activation_token.check_token(email, token):
        email.subscribed = True
        email.save()
        return redirect(url)
    else:
        return HttpResponse('Activation link is invalid!')


def ajax_email(request):
    if request.is_ajax():
        form_id = request.POST.get('form_id', None)
        form_name = form_mapping.get(form_id, 'Unknown form')
        name = request.POST.get('name', 'Unknown')
        email = request.POST.get('email', None)
        token = user_activation_token.make_token(email)
        current_site = request._current_scheme_host

        response = {}

        status = True
        if not Email.objects.filter(address=email).exists():
            Email.objects.create(
                form_name=form_name,
                full_name=name, 
                address=email,
                subscribed=False,
            )
            status = send_subscription_email(
                email=email,
                current_site=current_site,
                token=token
            )
        else:
            Email.objects.filter(address=email).first().update(subscribed=True)

        if status is True:
            member_info = {
                "email_address": email,
                "status": "subscribed",
                "merge_fields": {
                    "FNAME": name.split(" ")[0],
                    "LNAME": name.split(" ")[-1],
                    "FORM": form_name,
                }
            }
            send_contact_info(request, member_info)

        response = {'success': True}

        return JsonResponse(response)

