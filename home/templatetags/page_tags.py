from django import template
from django.conf import settings
import requests, requests_cache, json
from wagtail.models import Page

requests_cache.install_cache(cache_name='{}/github_cache'.format(settings.GITHUB_CACHE_DIR), backend="sqlite", expire_after=86400)

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


def _repo_info(key):
    url = "https://api.github.com/repos/ckan/ckan"
    res = requests.get(url)
    if res.ok:
        data = json.loads(res.text)
        return data.get(key, None)
    return None

def _get_number(n):
    raw = round(n/1000, 1)
    if raw.is_integer():
        return f'{int(raw)}k'
    return f'{raw}k'


@register.simple_tag()
def stars_count():
    stars = _repo_info('stargazers_count')
    if stars:
        return _get_number(stars)
    return '3k'

@register.simple_tag()
def forks_count():
    forks = _repo_info('forks_count')
    if forks:
        return _get_number(forks)
    return '1.6k'

@register.simple_tag()
def add_blog_post_url():
    blog_listing_page_id = Page.objects.get(slug='blog').id
    return f'/admin/pages/{blog_listing_page_id}/add_subpage/'

@register.simple_tag()
def is_editor_or_stronger(request):
    return request.user.has_perms('editor')
