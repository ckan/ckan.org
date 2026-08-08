import typing
from datetime import datetime

from django.db import models
from django.shortcuts import redirect
from django.template.loader import render_to_string
from managers.models import Manager
from modelcluster.models import ParentalKey
from wagtail.admin.mail import send_mail
from wagtail.admin.panels import FieldPanel, InlinePanel, PageChooserPanel
from wagtail.contrib.forms.models import AbstractEmailForm, AbstractFormField
from wagtail.contrib.settings.models import BaseSiteSetting, register_setting
from wagtail.fields import RichTextField
from wagtail.models import Page
from wagtail.snippets.models import register_snippet
from wagtailcache.cache import WagtailCacheMixin


@register_setting
class CkanOrgSettings(BaseSiteSetting):
    modal_form_page = models.ForeignKey(
        'wagtailcore.Page',
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name='+',
        verbose_name='Modal Form'
    )

    panels: typing.ClassVar[list] = [
        PageChooserPanel('modal_form_page', page_type='contact.ContactPage')
    ]


class FormField(AbstractFormField):
    page = ParentalKey(
        'ContactPage',
        on_delete=models.CASCADE,
        related_name='form_fields',
    )

def parse_contact_form(message):
    out = {}
    items = message.split("\n")
    for item in items:
        if ": " not in item:
            continue
        key, value = item.split(": ", 1)
        out[key.split("/")[0].replace(
            " ", "_").replace(
            "-", "_").replace(
            ".", "_").strip("_").lower()] = value
    return out

class ContactPage(WagtailCacheMixin, AbstractEmailForm):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        send_to = [x.email for x in Manager.objects.all()]
        self.to_address = ','.join(send_to)

    template = 'contact/contact_page.html'
    landing_page_template = 'contact/contact_page_landing.html'
    subpage_types: typing.ClassVar[list] = []
    max_count = 1
    cache_control = 'no-cache'

    intro = RichTextField(
        blank=True,
    )
    thank_you_text = RichTextField(
        blank=True,     
    )
    content_panels = AbstractEmailForm.content_panels + [
        FieldPanel('intro'),
        FieldPanel('thank_you_text'),
        FieldPanel('subject'), 
        FieldPanel('from_address'),
        InlinePanel('form_fields', label='Form Fields'),
    ]

    def send_mail(self, form):
        addresses = [x.strip() for x in self.to_address.split(',')]
        plain_message = self.render_email(form).replace('Your', 'Sender')
        fields = parse_contact_form(plain_message)
        html_message = render_to_string('contact_us_mail.html', fields)
        send_mail(self.subject, plain_message, addresses, self.from_address, html_message=html_message)


    def render_landing_page(self, request, form_submission=None, *args, **kwargs): # type: ignore
        redirect_page = Page.objects.get(id=request.POST.get('source-page-id'))
        if redirect_page:
            request.session['form_page_success'] = True
            return redirect(redirect_page.url, permanent=False)

        return super().render_landing_page(request, form_submission, *args, **kwargs)


@register_snippet
class Email(models.Model):

    submitted = models.DateTimeField(
        default=datetime.now,
    )
    form_name = models.CharField(
        max_length=64,
        blank=False,
        null=False,
    )
    address = models.EmailField(
        max_length=254,
        blank=False,
        null=False,
    )

    def __str__(self):
        return self.address
