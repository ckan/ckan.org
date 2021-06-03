
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
    if item.link == '/':
        return request.path == '/'
    return request.path.startswith(item.link)


