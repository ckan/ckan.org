from datetime import datetime

from django.shortcuts import render
from django.core.mail import send_mail
from django.http import JsonResponse  
from django.conf import settings

from .models import Email
from managers.models import Manager

EMAIL_SUBJECT = 'Form submition from ckan.org'

EMAIL_BODY = '''
<b>{}</b> was submitted on {}
with the following e-mail: {}
'''

form_mapping = {
    '#steward_email': 'Steward Form',
    '#steward_email_send': 'Steward Form',
    '#webinar_email': 'Webinar Form',
    '#blog_email': 'Blog Subscription Form',
}

def ajax_email(request):
    if request.headers.get('x-requested-with') == 'XMLHttpRequest':
        form_id = request.POST.get('form_id', None)
        form_name = form_mapping.get(form_id, 'Unknown form')
        email = request.POST.get('email', None)
        response = {}
        Email.objects.create(
            form_name=form_name,
            address=email
        )
        send_to = [x.email for x in Manager.objects.all()]
        from django.template.loader import render_to_string
        from django.utils.html import strip_tags
        html_message = render_to_string('mail.html',
                {'form_name': form_name,
                 'time': datetime.now().strftime("%A, %d %B %Y, %I:%M%p"),
                 'email': email
                 })
        plain_message = strip_tags(html_message)
        send_mail(
            EMAIL_SUBJECT,
            plain_message,
            settings.DEFAULT_FROM_EMAIL,
            send_to,
            fail_silently=False,
            html_message=html_message),
        response = {'success': True}
        return JsonResponse(response)
