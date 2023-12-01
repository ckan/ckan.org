from wagtail.snippets.models import register_snippet
from wagtail.snippets.views.snippets import SnippetViewSet

from .models import Email


@register_snippet
class EmailAdmin(SnippetViewSet):
    model = Email
    menu_label = "Emails"
    icon = "mail"
    menu_order = 290
    add_to_settings_menu = False
    exclude_from_explorer = False
    list_display = ["submitted", "form_name", "address"]
    list_filter = ["form_name", "submitted"]
    search_fields = ["submitted", "form_name", "address"]
