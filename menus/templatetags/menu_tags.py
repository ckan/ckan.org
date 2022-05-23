from django import template

from ..models import Menu

register = template.Library()

@register.simple_tag()
def get_menu(slug):
    try:
        return Menu.objects.get(slug=slug)
    except Menu.DoesNotExist:
        return Menu.objects.none()

@register.simple_tag()
def is_active(request, item):
    if item.link == '/' and request:
        return request.path == '/'
    elif isinstance(request, str) and request == '':
        return False
    return request.path.startswith(item.link)


