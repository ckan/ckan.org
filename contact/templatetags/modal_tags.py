import uuid

from django import template
from django.conf import settings as django_settings
from ..models import CkanOrgSettings, ContactPage


register = template.Library()


@register.inclusion_tag("tags/form_modal.html", takes_context=True)
def form_modal(context, form_name=None):
    if "request" in context:
        request = context["request"]
        if form_name is None:
            settings = CkanOrgSettings.for_request(request)
            form_page = settings.modal_form_page
            if not form_page:
                return context
            form_page = form_page.specific
        else:
            form_page = ContactPage.objects.get(form_name=form_name)
        context["form_page"] = form_page
        context["form"] = form_page.get_form(page=form_page, user=request.user)
        context["form_id"] = uuid.uuid4().hex
        context["recaptcha_sitekey"] = django_settings.RECAPTCHA_PUBLIC_KEY

    return context
