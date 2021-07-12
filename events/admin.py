from wagtail.contrib.modeladmin.options import (
    ModelAdmin,
    modeladmin_register
)

from .models import EventPostPage

@modeladmin_register
class EventPostPageAdmin(ModelAdmin):
    model = EventPostPage
    menu_label = 'Events'
    menu_order = 290
    list_display = ['created', 'post_title', 'event_type', 'start_date', 'end_date']
    list_filter = ['created', 'event_type', 'start_date', 'end_date']
    search_fields = ['created', 'event_type', 'start_date', 'end_date']
