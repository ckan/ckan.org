from wagtail.snippets.models import register_snippet
from wagtail.snippets.views.snippets import SnippetViewSet

from .models import Manager


@register_snippet
class ManagerAdmin(SnippetViewSet):
    model = Manager
    menu_label = "Managers"
    icon = "group"
    menu_order = 290
    add_to_settings_menu = True
    list_display = ["name", "email"]
    search_fields = ["name", "email"]
