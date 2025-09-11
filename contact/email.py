import datetime
from email.mime.image import MIMEImage
import logging
import os
import traceback

from django.conf import settings
from django.template.loader import render_to_string
from django.utils.http import urlsafe_base64_encode
from django.utils.encoding import force_bytes
from django.core.mail import EmailMessage, send_mail
from django.utils.html import strip_tags

from managers.models import Manager


EMAIL_FROM = "comms@ckan.org"
EMAIL_SUBJECT = "Form submission from ckan.org"
EMAIL_BODY = "<b>{}</b> was submitted on {} with the following e-mail: {}"
EMAIL_IMAGES = [
    "logo_ckan.png",
    "icons8-linkedin-circled-50.png",
    "icons8-twitter-circled-50.png",
    "globe-circle-icon.png",
    "youtube-round-icon.png",
]


def send_subscription_email(email: str, current_site: str, token: str) -> bool:
    """
    Sends a subscription confirmation email for the CKAN Monthly Newsletter.

    The email includes a confirmation link with a token and embeds several images
    for branding and social media icons. The email is sent in HTML format.

    Args:
        email (str): Recipient's email address.
        current_site (str): The domain of the current site, used in the confirmation link.
        token (str): Unique token for confirming the subscription.

    Returns:
        bool: True if the email was sent successfully, False otherwise.
    """
    subject = "You're Almost In - Confirm Your Subscription to CKAN Monthly Newsletter"
    message = render_to_string(
        "contact/subscription_email.html",
        {
            "domain": current_site,
            "eid": urlsafe_base64_encode(force_bytes(email)),
            "token": token,
        },
    )

    try:
        complete_email = EmailMessage(
            subject=subject,
            body=message,
            from_email=EMAIL_FROM,
            to=[email]
        )
        complete_email.content_subtype = "html"
        for f in EMAIL_IMAGES:
            fp = open(os.path.join(settings.BASE_DIR, f"static/img/{f}"), "rb")
            msg_img = MIMEImage(fp.read())
            fp.close()
            msg_img.add_header("Content-ID", "<{}>".format(f))
            complete_email.attach(msg_img)
        complete_email.send()
    except Exception:
        logging.getLogger("error").error(traceback.format_exc())
        return False

    return True


def send_managers_email(form_name: str, email: str) -> bool:
    """
    Sends a notification email to all managers when a form is submitted.

    The email contains the form name, submission time, and the submitter's email address.
    The message is sent in both HTML and plain text formats.

    Args:
        form_name (str): The name of the submitted form.
        email (str): The email address of the person who submitted the form.

    Returns:
        bool: True if the email was sent successfully, False otherwise.
    """
    send_to = [x.email for x in Manager.objects.all()]
    html_message = render_to_string("mail.html", {
        "form_name": form_name,
        "time": datetime.now().strftime("%A, %d %B %Y, %I:%M%p"),
        "email": email,
    })
    plain_message = strip_tags(html_message)

    try:
        send_mail(
            subject=EMAIL_SUBJECT,
            message=plain_message,
            from_email=settings.DEFAULT_FROM_EMAIL,
            recipient_list=send_to,
            fail_silently=False,
            html_message=html_message
        )
    except Exception:
        logging.getLogger("error").error(traceback.format_exc())
        return False

    return True
