from django.templatetags.static import static
from django.utils.html import format_html

from wagtail import hooks
from wagtail.snippets.models import register_snippet
from wagtail.snippets.views.snippets import SnippetViewSet

from .models import Menu


@register_snippet
class MenuAdmin(SnippetViewSet):
    model = Menu
    menu_label = "Menus"
    icon = "list-ul"
    menu_order = 200
    add_to_settings_menu = True
    list_display = (
        "title",
        "slug"
    )


@hooks.register("insert_global_admin_css", order=100)
def global_admin_css():
    return format_html("<link rel='stylesheet' href='{}'>", static("css/admin.css"))
