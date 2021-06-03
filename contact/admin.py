from wagtail.contrib.modeladmin.options import (
    ModelAdmin,
    modeladmin_register
)

from .models import Email

@modeladmin_register
class EmailAdmin(ModelAdmin):
    model = Email
    menu_label = 'Emails'
    menu_icon = 'mail'
    menu_order = 290
    add_to_settings_menu = False
    exclude_from_explorer = False
    list_display = ['submitted', 'form_name', 'address']
    list_filter = ['form_name', 'submitted']
    search_fields = ['submitted', 'form_name', 'address']

