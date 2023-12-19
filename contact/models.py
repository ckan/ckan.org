from django.db import models
from django.shortcuts import render
from django.template.loader import render_to_string
from django.template.response import TemplateResponse
from django.shortcuts import redirect

from modelcluster.models import ParentalKey

from wagtail.admin.mail import send_mail
from wagtail.models import Page
from wagtail.fields import RichTextField
from wagtail.contrib.forms.models import AbstractEmailForm, AbstractFormField
from wagtail.contrib.settings.models import BaseSiteSetting, register_setting
from wagtail.snippets.models import register_snippet
from wagtail.admin.panels import FieldPanel, InlinePanel, PageChooserPanel, HelpPanel
from wagtailcache.cache import WagtailCacheMixin

from managers.models import Manager
from contact.forms import WagtailCaptchaEmailForm

import mailchimp_marketing as MailchimpMarketing
from mailchimp_marketing.api_client import ApiClientError


@register_setting
class MailChimpSettings(BaseSiteSetting):
    api_key = models.CharField(
        max_length=255,
        help_text="Mailchimp API key",
        blank=True,
    )
    audience_id = models.CharField(
        max_length=255,
        help_text="MailChimp list ID",
        blank=True,
    )

    class Meta:
        verbose_name = 'MailChimp settings'
        verbose_name_plural = "MailChimp settings"

    panels = [
        FieldPanel('api_key'),
        FieldPanel('audience_id'),
        HelpPanel(
            template='contact/mailchimp_info.html',
            heading='Important info',
        )
    ]


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

    class Meta:
        verbose_name = 'CKAN.org settings'

    panels = [
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
        i = item.split(": ")
        out[i[0].split("/")[0].replace(
            " ", "_").replace(
            "-", "_").replace(
            ".", "_").replace(
            "?", "").strip("_").lower()] = i[1]
    return out


def send_contact_info(request, member_info:dict):
    """Send contact info to MailChimp audience/list

    Args:
        request (_type_): _description_
        member_info (dict): contains the following keys 'email_address', 'status',
        'merged_fields' ('FNAME', 'LNAME', 'PHONE', 'COMPANY', 'FORM')
    """
    mailchimp_api_key = MailChimpSettings.for_request(request).api_key
    mailchimp_audience_id = MailChimpSettings.for_request(request).audience_id
    if mailchimp_api_key and mailchimp_audience_id:
        try:
            client = MailchimpMarketing.Client()
            client.set_config({
                "api_key": mailchimp_api_key,
                "server": mailchimp_api_key.split("-")[-1],
            })
            client.lists.add_list_member(mailchimp_audience_id, member_info)
        except ApiClientError as error:
            print("An exception occurred: {}".format(error.text))


class ContactPage(WagtailCacheMixin, WagtailCaptchaEmailForm):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        send_to = [x.email for x in Manager.objects.all()]
        self.to_address = ','.join(send_to)

    template = 'contact/contact_page.html'
    landing_page_template = 'contact/contact_page_landing.html'
    subpage_types =[]
    max_count = 5
    cache_control = 'no-cache'

    form_name = models.CharField(
        max_length=255,
        blank=True,
    )
    intro = RichTextField(
        features=['h2', 'h3', 'h4', 'h5', 'h6', 'bold', 'italic', 'link', 'superscript', 'subscript'],
        blank=True,
    )
    thank_you_text = models.TextField(
        blank=True,
        null=True,
        help_text='Use HTML tags for text design.',
    )
    button_text = models.CharField(
        max_length = 50,
        blank=True,
        help_text = "Submit button text for this form.",
        default="Contact Us"
    )

    class Meta:
        verbose_name = 'Contact form'
        verbose_name_plural = "Contact forms"

    content_panels = AbstractEmailForm.content_panels + [
        FieldPanel('form_name'),
        FieldPanel('intro'),
        FieldPanel('thank_you_text'),
        FieldPanel('subject'), 
        FieldPanel('from_address'),
        FieldPanel('button_text'),
        InlinePanel('form_fields', label='Form Fields'),
    ]

    def send_mail(self, form):
        addresses = [x.strip() for x in self.to_address.split(',')]
        plain_message = self.render_email(form).replace('Your', 'Sender')
        fields = parse_contact_form(plain_message)
        if self.form_name == "Webinar Form":
            html_message = render_to_string('contact/webinar_form_mail.html', fields)
        else:
            html_message = render_to_string('contact/contact_form_mail.html', fields)
        sender_name  = fields.get('sender_name', '')
        if sender_name:
            self.subject = f'{self.subject} Sender name: {sender_name}'
        send_mail(self.subject, plain_message, addresses, self.from_address, html_message=html_message)

    # @check_recaptcha(required_score=0.85)
    def serve(self, request, *args, **kwargs):
        if request.method == 'POST':
            form = self.get_form(request.POST, request.FILES, page=self, user=request.user)

            if form.is_valid():
                form_submission = self.process_form_submission(form)
                email = form.cleaned_data.get("your_e_mail_address", '')
                name = form.cleaned_data.get("your_name", '')
                phone = form.cleaned_data.get("your_phone_number", '')
                company = form.cleaned_data.get("your_companyorganization_name", '')

                ##* Create email object and save form data in DB
                Email.objects.create(
                    form_name=self.form_name,
                    full_name = name,
                    address=email
                )

                ##* Send form data to Mailchimp audience
                member_info = {
                    "email_address": email,
                    "status": "subscribed",
                    "merge_fields": {
                        "FNAME": name.split(" ")[0],
                        "LNAME": name.split(" ")[-1],
                        "PHONE": phone,
                        "COMPANY": company,
                        "FORM": self.form_name,
                    }
                }
                send_contact_info(request, member_info)

                return self.render_landing_page(request, form_submission, *args, **kwargs)
            else:
                return render(request, "recaptcha_error.html")
        else:
            form = self.get_form(page=self, user=request.user)

        context = self.get_context(request)
        context['form'] = form
        return TemplateResponse(request, self.get_template(request), context)

    def render_landing_page(self, request, form_submission=None, *args, **kwargs):
        redirect_page = Page.objects.get(id=request.POST.get('source-page-id'))
        if redirect_page:
            request.session['form_page_success'] = True
            return redirect(redirect_page.url, permanent=False)

        return super().render_landing_page(request, form_submission, *args, **kwargs)


@register_snippet
class Email(models.Model):

    form_name = models.CharField(
        max_length=64,
        blank=False,
        null=False,
    )
    full_name = models.CharField(
        max_length=128,
        blank=True,
        null=True,
    )
    address = models.EmailField(
        verbose_name="Email",
        max_length=254,
        blank=False,
        null=False,
    )
    subscribed = models.BooleanField(
        default=False,
    )
    submitted = models.DateTimeField(
        auto_now_add=True,
    )
    updated = models.DateTimeField(
        auto_now=True,
    )

    def __str__(self):
        return self.address


@register_snippet
class Message(models.Model):

    title = models.CharField(
        max_length=254,
        blank=False,
        null=False,
    )
    slug = models.CharField(
        max_length=64,
        blank=True,
        null=True,
        help_text='Used for references in templates.',
    )
    type = models.CharField(
        max_length=64,
        blank=True,
        null=True,
    )
    content = models.TextField(
        blank=True,
        null=True,
        help_text='Use HTML tags for text design.',
    )

    def __str__(self):
        return self.title
