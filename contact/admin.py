from wagtail.snippets.models import register_snippet
from wagtail.snippets.views.snippets import SnippetViewSet, SnippetViewSetGroup
from wagtail.admin.ui.tables import BooleanColumn

from .models import Email, Message


class EmailAdmin(SnippetViewSet):
    model = Email
    menu_label = "Emails"
    icon = "mail"
    menu_order = 260
    list_display = (
        "form_name",
        "address",
        "full_name",
        "submitted",
        "updated",
        BooleanColumn("subscribed"),
    )
    ordering = "-updated"
    list_export = ["full_name", "address"]
    list_filter = ["form_name", "submitted", "subscribed"]
    search_fields = ["address", "full_name"]


class MessageAdmin(SnippetViewSet):
    model = Message
    menu_label = "Messages"
    icon = "list-ul"
    menu_order = 292
    list_display = ("title", "slug", "type")
    list_filter = ("type",)
    empty_value = "No category"


@register_snippet
class ContactGroup(SnippetViewSetGroup):
    items = (EmailAdmin, MessageAdmin)
    icon = "folder-open-inverse"
    menu_label = "Contacts"
    menu_name = "contacts"
    menu_order = 170
