from django.utils.safestring import mark_safe
from django.conf import settings
from django.core.files import File
from wagtail.admin.models import Page

from wagtail.core import hooks

class QuickLinksPanel:
    order = 100

    def render(self):
        raw = File(open(
            settings.BASE_DIR + '/ckanorg/templates/snippets/admin_home_quick_links_block.html'))
        html = raw.read()
        blog_page_id = Page.objects.get(title="Blog").id
        contact_us_page_id = Page.objects.get(title="Contact Us").id
        return mark_safe(html.format(blog_page_id, contact_us_page_id))

@hooks.register('construct_homepage_panels')
def add_another_welcome_panel(request, panels):
    panels.append(QuickLinksPanel())
