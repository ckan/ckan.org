from django import template

register = template.Library()

@register.filter
def rng(value):
    return range(value)

@register.filter
def split_images(items, n):
    n = int(n)
    return [items[i:i + n] for i in range(0, len(items), n)]

@register.filter
def split_string(string, n):
    n = int(n)
    lst = string.split()
    out = [lst[i:i + n] for i in range(0, len(lst), n)]
    return [' '.join(i) for i in out]

@register.filter
def tags_to_string(tags):
    return ', '.join([i.name for i in tags])

@register.filter
def get_working_group_members(working_group):
    out = []
    for i in range(1, 4):
        out.append(
            dict(
                image = getattr(working_group, 'member_{}_image'.format(i)),
                description = getattr(working_group, 'member_{}_description'.format(i)),
                url = getattr(working_group, 'member_{}_url'.format(i))
            )
        )
    return out

@register.filter
def dirs(value):
    return str(dir(value))
