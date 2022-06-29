from wagtail.contrib.modeladmin.options import (
    ModelAdmin,
    modeladmin_register
)
from .models import Profile


@modeladmin_register
class ProfileAdmin(ModelAdmin):
    model = Profile
    menu_label = "Users profiles"
    menu_icon = 'user'
    menu_order = 600
    add_to_settings_menu = True
    exclude_from_explorer = True
    list_display = ('user', 'company', 'location')
    list_filter = ('company', 'location')
    search_fields = ('user', 'company') 
