from django.utils.safestring import mark_safe
from django.conf import settings
from django.core.files import File
from django.forms import Media

from wagtail.admin.models import Page
from wagtail import hooks

MODERATORS = 'Moderators'
EDITORS = 'Editors'


class QuickLinksPanel:
    order = 100

    def __init__(self, request):
        self.request = request
        self.media = Media()

    def render(self):
        path = '/ckanorg/templates/snippets/admin_home_quick_links_block.html'
        user = self.request.user
        if not user.is_superuser:
            user_groups = [x.name for x in user.groups.all()]
            if MODERATORS in user_groups:
                pass
            elif EDITORS in user_groups:
                path = '/ckanorg/templates/snippets/editor_home_quick_links_block.html'
            else:
                path = '/ckanorg/templates/snippets/blogger_home_quick_links_block.html'
        raw = File(open(
            settings.BASE_DIR + path))
        html = raw.read()
        blog_page_id = Page.objects.get(title="Blog").id
        contact_us_page_id = Page.objects.get(title="Contact Us").id
        return mark_safe(html.format(blog_page_id, contact_us_page_id))

@hooks.register('construct_homepage_panels')
def add_another_welcome_panel(request, panels):
    panels.append(QuickLinksPanel(request))

@hooks.register('construct_explorer_page_queryset')
def show_authors_only_their_articles(parent_page, pages, request):
    user_group = request.user.groups.filter(name='Blog Post Creators').exists()
    if user_group:
        pages = pages.filter(owner=request.user)
    return pages

@hooks.register('construct_reports_menu')
def hide_site_history_from_blogger(request, menu_items):
    user_groups = [x.name for x in request.user.groups.all()]
    if MODERATORS not in user_groups and EDITORS not in user_groups:
        menu_items[:] = [item for item in menu_items if item.name != 'site-history']

@hooks.register('construct_main_menu')
def hide_events_from_editor(request, menu_items):
    user_groups = [x.name for x in request.user.groups.all()]
    if not request.user.is_superuser and MODERATORS not in user_groups:
        menu_items[:] = [item for item in menu_items if item.name != 'events']
