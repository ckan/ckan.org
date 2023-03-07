from wagtail.contrib.modeladmin.options import ModelAdmin, ModelAdminGroup, modeladmin_register

from .models import Email, ContactPage


class EmailAdmin(ModelAdmin):
    model = Email
    menu_label = 'Emails'
    menu_icon = 'mail'
    menu_order = 290
    add_to_settings_menu = False
    exclude_from_explorer = False
    list_display = ['submitted', 'form_name', 'address', 'full_name']
    list_filter = ['form_name', 'submitted']
    search_fields = ['submitted', 'form_name', 'address', 'full_name']


class ContactPageAdmin(ModelAdmin):
    model = ContactPage
    menu_label = "Forms"
    menu_icon = 'form'
    menu_order = 200
    list_display = ('title',)
    empty_value = 'No category'


@modeladmin_register
class ContactGroup(ModelAdminGroup):
    menu_label = 'Contacts'
    menu_icon = 'folder-open-inverse'
    menu_order = 170  
    items = (ContactPageAdmin, EmailAdmin)
