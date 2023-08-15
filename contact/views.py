import logging
import traceback

from django.conf import settings
from django.http import JsonResponse, HttpResponse
from django.shortcuts import redirect
from django.utils import timezone
from django.utils.encoding import force_text
from django.utils.http import urlsafe_base64_decode
from django.views.generic import TemplateView

from .models import Email, send_contact_info, Message
from .token import user_activation_token
from .email import send_subscription_email

from django.contrib import messages


form_mapping = {
    '#subscribe_form': 'Subscribe Form',
    '#blog_subscribe_form': 'Subscribe Form',
    '#blog_unsubscribe_form': 'Subscribe Form',
}

def activate_subscription(request, eidb64, token):
    try:
        eid = force_text(urlsafe_base64_decode(eidb64))
        subscriber = Email.objects.filter(
            form_name = 'Subscribe Form',
            address=eid
        ).first()
        url = request._current_scheme_host
    except(TypeError, ValueError, OverflowError, Email.DoesNotExist):
        logging.getLogger("error_logger").error(traceback.format_exc())
        subscriber = None
    if subscriber is not None and user_activation_token.check_token(subscriber, token):
        subscriber.subscribed = True
        subscriber.save()
        try:
            message = Message.objects.get(slug='confirmation-message')
            message_content = message.content
        except Message.DoesNotExist:
            logging.getLogger("error_logger").error(traceback.format_exc())
            message_content = "<p>Congratulations! You have been successfully subscribed.</p>"
        messages.success(request, message_content)
        return redirect(url)
    else:
        return HttpResponse('Activation link is invalid!')


def ajax_unsubscribe(request):
    form_id = request.POST.get('form_id', None)
    form_name = form_mapping.get(form_id, None)
    email = request.POST.get('email', None)
    subscriber = Email.objects.filter(
        form_name=form_name,
        address=email,
    ).first()

    if not subscriber:
        try:
            message = Message.objects.get(slug='unsubscribed-failed-message')
            message_content = message.content
        except Message.DoesNotExist:
            logging.getLogger("error_logger").error(traceback.format_exc())
            message_content = "<p>Subscriber with this email is not registered!</p>"
        response = {
            'failed': True,
            'message_content': message_content
        }
        return JsonResponse(response)

    subscriber.subscribed = False
    subscriber.update = timezone.now()
    subscriber.save()
    try:
        message = Message.objects.get(slug='unsubscribed-message')
        message_content = message.content
    except Message.DoesNotExist:
        logging.getLogger("error_logger").error(traceback.format_exc())
        message_content = "<p>You have been successfully unsubscribed!</p>"
    response = {
        'unsubscribed': True,
        'message_content': message_content
    }
    return JsonResponse(response)



def ajax_email(request):
    if request.is_ajax():
        form_id = request.POST.get('form_id', None)
        form_name = form_mapping.get(form_id, None)
        name = request.POST.get('name', None)
        email = request.POST.get('email', None)
        token = user_activation_token.make_token(email)
        current_site = request._current_scheme_host

        response = {}
        subscriber, created = Email.objects.get_or_create(
            form_name=form_name,
            address=email,
        )
        if created:
            subscriber.full_name = name
            subscriber.save()
        elif subscriber.subscribed:
            try:
                message = Message.objects.get(slug='subscribed-message')
                message_content = message.content
            except Message.DoesNotExist:
                logging.getLogger("error_logger").error(traceback.format_exc())
                message_content = "<p>You have been already subscribed!</p>"
            response = {
                'subscribed': True,
                'message_content': message_content
            }
            return JsonResponse(response)
        else:
            subscriber.full_name = name
            subscriber.update = timezone.now()
            subscriber.save()

        send_subscription_email(
                email=email,
                current_site=current_site,
                token=token
            )

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

        try:
            message = Message.objects.get(slug='thanks-message')
            message_content = message.content
        except Message.DoesNotExist:
            logging.getLogger("error_logger").error(traceback.format_exc())
            message_content = "<p>We have sent you a confirmation email!</p>"
        response = {
            'success': True,
            'message_content': message_content
        }

        return JsonResponse(response)


class SubscriptionPage(TemplateView):
    template_name = "contact/subscription_page.html"

    def get_context_data(self, **kwargs):
        context = super(SubscriptionPage, self).get_context_data(**kwargs)
        context['recaptcha_sitekey'] = settings.RECAPTCHA_PUBLIC_KEY
        return context
