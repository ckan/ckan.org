from wagtail.contrib.modeladmin.options import (
    ModelAdmin,
    modeladmin_register
)

from .models import Manager

@modeladmin_register
class ManagerAdmin(ModelAdmin):
    model = Manager
    menu_label = 'Managers'
    menu_icon = 'group'
    menu_order = 290
    add_to_settings_menu = False
    exclude_from_explorer = False
    list_display = ['name', 'email']
    search_fields = ['name', 'email']
