import datetime
import logging
import traceback

from django.conf import settings
from django.template.loader import render_to_string
from django.utils.http import urlsafe_base64_encode
from django.utils.encoding import force_bytes
from django.core.mail import EmailMessage, send_mail
from django.utils.html import strip_tags

from managers.models import Manager


EMAIL_SUBJECT = ''

EMAIL_BODY = '''
<b>{}</b> was submitted on {}
with the following e-mail: {}
'''


def send_subscription_email(email, current_site, token):
    mail_subject = 'Welcome Aboard! Confirm Your CKAN Monthly Newsletter Subscription'
    message = render_to_string('contact/subscription_email.html', {
        'domain': current_site,
        'eid': urlsafe_base64_encode(force_bytes(email)),
        'token': token,
    })
    try:
        complete_email = EmailMessage(mail_subject, message, to=[email])
        complete_email.content_subtype = 'html'
        complete_email.send()
    except Exception as e:
        logging.getLogger("error").error(traceback.format_exc())
        return False
    return True


def send_managers_email(form_name, email):
    send_to = [x.email for x in Manager.objects.all()]
    html_message = render_to_string('mail.html', {
        'form_name': form_name,
        'time': datetime.now().strftime("%A, %d %B %Y, %I:%M%p"),
        'email': email,
    })
    plain_message = strip_tags(html_message)
    try:
        send_mail(
            subject='Form submition from ckan.org',
            message=plain_message,
            from_email=settings.DEFAULT_FROM_EMAIL,
            recipient_list=send_to,
            fail_silently=False,
            html_message=html_message
        )
    except Exception as e:
        logging.getLogger("error").error(traceback.format_exc())
        return False
    return True
