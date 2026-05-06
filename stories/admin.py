from wagtail.admin.ui.tables import BooleanColumn
from wagtail.snippets.models import register_snippet
from wagtail.snippets.views.snippets import SnippetViewSet, SnippetViewSetGroup

from stories.models import StoriesNotificationEmail, StoryItem


class StoryItemAdmin(SnippetViewSet):
    model = StoryItem
    menu_label = "Stories" # type: ignore
    icon = "doc-empty-inverse" # type: ignore
    menu_order = 100 # type: ignore
    list_display: tuple[str, ...] = ( # type: ignore
        "title",
        "org",
        "region",
        "portal",
        "created",
    )
    list_export: tuple[str, ...] = ( # type: ignore
        "title",
        "org",
        "region",
        "portal",
        "created",
    )
    ordering: str = "-created"
    list_filter: tuple[str, ...] = ( # type: ignore
        "region",
        "created",
    )
    search_fields: tuple[str, ...] = ( # type: ignore
        "title",
        "org"
    )


class StoriesNotificationEmailAdmin(SnippetViewSet):
    model = StoriesNotificationEmail
    menu_label = "Emails" # type: ignore
    icon = "mail" # type: ignore
    menu_order = 260 # type: ignore
    list_display = (
        "email",
        "created",
        BooleanColumn("subscribed"),
    ) # type: ignore
    ordering: str = "-created"
    list_export: tuple[str, ...] = ("email", "created", "subscribed") # type: ignore
    list_filter: tuple[str, ...] = ("created", "subscribed") # type: ignore
    search_fields: tuple[str, ...] = ("email",) # type: ignore


@register_snippet
class StoriesGroup(SnippetViewSetGroup):
    menu_label = "Stories" # type: ignore
    icon = "folder-open-inverse"
    menu_order = 150
    items = (StoryItemAdmin, StoriesNotificationEmailAdmin)
