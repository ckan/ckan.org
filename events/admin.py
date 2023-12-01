from wagtail.snippets.models import register_snippet
from wagtail.snippets.views.snippets import SnippetViewSet

from .models import EventPostPage


@register_snippet
class EventPostPageAdmin(SnippetViewSet):
    model = EventPostPage
    menu_label = 'Events'
    icon = 'date'
    menu_order = 290
    add_to_admin_menu = True
    list_display = ['created', 'post_title', 'event_type', 'start_date', 'end_date']
    list_export = ['created', 'post_title', 'event_type', 'start_date', 'end_date']
    ordering = "-start_date"
    list_filter = ['created', 'event_type', 'start_date', 'end_date']
    search_fields = ['post_title', 'event_type']
