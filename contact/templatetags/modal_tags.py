from django import template
from ..models import CkanOrgSettings

register = template.Library()

@register.inclusion_tag('tags/form_modal.html', takes_context=True)
def form_modal(context):
    if 'request' in context:
        request = context['request']
        settings = CkanOrgSettings.for_request(request)
        form_page = settings.modal_form_page

        if not form_page:
            return context

        form_page = form_page.specific

        context['form_page'] = form_page
        context['form'] = form_page.get_form(page=form_page, user=request.user)

    return context
