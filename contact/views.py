import logging
import traceback
from datetime import timedelta

from django.conf import settings
from django.contrib import messages
from django.core.exceptions import ValidationError
from django.core.validators import validate_email
from django.http import HttpResponse, JsonResponse
from django.shortcuts import redirect
from django.utils import timezone
from django.utils.encoding import force_str
from django.utils.http import urlsafe_base64_decode
from django.views.generic import TemplateView

from .decorators import validate_captcha
from .email import send_subscription_email
from .models import Email, Message, send_contact_info
from .token import user_activation_token

form_mapping = {
    "#subscribe_form": "Subscribe Form",
    "#blog_subscribe_form": "Subscribe Form",
    "#blog_unsubscribe_form": "Subscribe Form",
}

# Minimum time between two confirmation emails for the same address. This stops
# the newsletter form from being abused as an email bomb / backscatter source
# (which is what generated the SES abuse complaints and bounces).
CONFIRMATION_RESEND_INTERVAL = timedelta(
    minutes=getattr(settings, "SUBSCRIPTION_CONFIRMATION_RESEND_MINUTES", 15)
)


def _get_message(slug: str, default: str) -> str:
    """Return the admin-editable message for ``slug`` or ``default``."""
    message = Message.objects.filter(slug=slug).first()
    if message and message.content:
        return message.content
    return default


def _error(message: str, status: int = 400) -> JsonResponse:
    return JsonResponse({"success": False, "message_content": message}, status=status)


def activate_subscription(request, eidb64, token):
    try:
        eid = force_str(urlsafe_base64_decode(eidb64))
        subscriber = Email.objects.filter(
            form_name = "Subscribe Form",
            address=eid
        ).first()
        url = request._current_scheme_host or settings.WAGTAILADMIN_BASE_URL
    except(TypeError, ValueError, OverflowError, Email.DoesNotExist):
        logging.getLogger("error_logger").error(traceback.format_exc())
        subscriber = None
    if subscriber is not None and user_activation_token.check_token(subscriber, token):
        was_subscribed = subscriber.subscribed
        subscriber.subscribed = True
        subscriber.save()

        if not was_subscribed:
            # Double opt-in: only add fully confirmed addresses to the Mailchimp
            # audience. Adding (possibly forged) addresses before confirmation
            # meant unconfirmed people received campaigns, generating complaints.
            full_name = subscriber.full_name or ""
            member_info = {
                "email_address": subscriber.address,
                "status": "subscribed",
                "merge_fields": {
                    "FNAME": full_name.split(" ")[0] if full_name else "",
                    "LNAME": full_name.split(" ")[-1] if full_name else "",
                    "FORM": subscriber.form_name,
                },
            }
            send_contact_info(request, member_info)

        message_content = "<p>Congratulations! You have been successfully subscribed.</p>"
        try:
            message = Message.objects.get(slug="confirmation-message")
            message_content = message.content or message_content
        except Message.DoesNotExist:
            logging.getLogger("error_logger").error(traceback.format_exc())
        messages.success(request, message_content)
        return redirect(url) # type: ignore
    else:
        return HttpResponse("Activation link is invalid!")


def ajax_unsubscribe(request):
    form_id = request.POST.get("form_id", None)
    form_name = form_mapping.get(form_id, None)
    email = request.POST.get("email", None)
    subscriber = Email.objects.filter(
        form_name=form_name,
        address=email,
    ).first()

    if not subscriber:
        try:
            message = Message.objects.get(slug="unsubscribed-failed-message")
            message_content = message.content
        except Message.DoesNotExist:
            logging.getLogger("error_logger").error(traceback.format_exc())
            message_content = "<p>Subscriber with this email is not registered!</p>"
        response = {
            "failed": True,
            "message_content": message_content
        }
        return JsonResponse(response)

    subscriber.subscribed = False
    subscriber.update = timezone.now() # type: ignore
    subscriber.save()
    try:
        message = Message.objects.get(slug="unsubscribed-message")
        message_content = message.content
    except Message.DoesNotExist:
        logging.getLogger("error_logger").error(traceback.format_exc())
        message_content = "<p>You have been successfully unsubscribed!</p>"
    response = {
        "unsubscribed": True,
        "message_content": message_content
    }
    return JsonResponse(response)



def ajax_email(request):
    if request.headers.get("x-requested-with") != "XMLHttpRequest":
        return _error("Invalid request.")

    # The newsletter form renders an invisible reCAPTCHA client-side, but until
    # now the token was never checked server-side, so bots could POST directly
    # to this endpoint and trigger confirmation emails to arbitrary addresses.
    if not validate_captcha(request):
        return _error("Captcha verification failed. Please try again.")

    form_id = request.POST.get("form_id", None)
    form_name = form_mapping.get(form_id, None)
    name = (request.POST.get("name") or "").strip()
    email = (request.POST.get("email") or "").strip()

    if not form_name:
        return _error("Invalid form.")

    if not name:
        return _error("Please enter your name.")

    try:
        validate_email(email)
    except ValidationError:
        return _error("Please enter a valid e-mail.")

    token = user_activation_token.make_token(email)
    current_site = f"{request.scheme}://{request.get_host()}"

    subscriber = (
        Email.objects.filter(form_name=form_name, address=email)
        .order_by("id")
        .first()
    )
    created = subscriber is None

    if created:
        subscriber = Email(form_name=form_name, address=email)
        subscriber.full_name = name
        subscriber.save()
    elif subscriber.subscribed:
        return JsonResponse({
            "subscribed": True,
            "message_content": _get_message(
                "subscribed-message", "<p>You have been already subscribed!</p>"
            ),
        })
    elif (
        subscriber.updated
        and timezone.now() - subscriber.updated < CONFIRMATION_RESEND_INTERVAL
    ):
        # A confirmation email was sent very recently - don't send another one.
        return JsonResponse({
            "success": True,
            "message_content": _get_message(
                "thanks-message", "<p>We have sent you a confirmation email!</p>"
            ),
        })
    else:
        subscriber.full_name = name
        subscriber.save()

    send_subscription_email(
        email=email,
        current_site=current_site,
        token=token,
    )

    # NOTE: the address is intentionally NOT added to the Mailchimp audience
    # here. It is only added once the subscriber clicks the confirmation link
    # (see activate_subscription) so that unconfirmed/forged addresses never
    # receive the newsletter.
    return JsonResponse({
        "success": True,
        "message_content": _get_message(
            "thanks-message", "<p>We have sent you a confirmation email!</p>"
        ),
    })


class SubscriptionPage(TemplateView):
    template_name = "contact/subscription_page.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["recaptcha_sitekey"] = settings.RECAPTCHA_PUBLIC_KEY
        return context
