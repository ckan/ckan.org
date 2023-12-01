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
