from django import template

register = template.Library()

@register.filter()
def endswith(value, arg):
    """
    Checks if a string ends with the specified suffix.
    Usage: {{ my_string|endswith:"suffix" }}
    """
    return str(value).endswith(str(arg))
