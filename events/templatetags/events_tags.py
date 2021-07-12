from django import template

register = template.Library()


@register.simple_tag()
def event_start(start_date):
    return start_date.strftime("%d %B %Y - %H:%M")

@register.simple_tag()
def event_start_date(start_date):
    return start_date.strftime("%d %B %Y")

