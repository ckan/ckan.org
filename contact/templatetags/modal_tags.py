import uuid

from django import template
from django.conf import settings as django_settings

from ..models import CkanOrgSettings, ContactPage

register = template.Library()


@register.inclusion_tag("tags/form_modal.html", takes_context=True)
def form_modal(context, form_name=None):
    request = context.get("request")
    if request is None:
        return context

    if form_name is None:
        settings = CkanOrgSettings.for_request(request)
        form_page = settings.modal_form_page
        if not form_page:
            return context
        form_page = form_page.specific
    else:
        # .filter().first() instead of .get(): if no page (or several) match
        # form_name it returns None (or one row) rather than raising
        # DoesNotExist/MultipleObjectsReturned and 500-ing the whole page.
        form_page = ContactPage.objects.filter(form_name=form_name).first()
        if form_page is None:
            return context

    context["form_page"] = form_page
    context["form"] = form_page.get_form(page=form_page, user=request.user)
    context["form_id"] = uuid.uuid4().hex
    context["recaptcha_sitekey"] = django_settings.RECAPTCHA_PUBLIC_KEY

    return context
