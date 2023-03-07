from wagtail.contrib.modeladmin.options import ModelAdmin, ModelAdminGroup, modeladmin_register

from .models import Email, ContactPage, Message


class EmailAdmin(ModelAdmin):
    model = Email
    menu_label = 'Emails'
    menu_icon = 'mail'
    menu_order = 290
    add_to_settings_menu = False
    exclude_from_explorer = False
    list_display = ['submitted', 'form_name', 'address', 'full_name', 'updated', 'subscribed']
    list_filter = ['form_name', 'submitted', 'subscribed']
    search_fields = ['submitted', 'form_name', 'address']


class ContactPageAdmin(ModelAdmin):
    model = ContactPage
    menu_label = "Forms"
    menu_icon = 'form'
    menu_order = 200
    list_display = ('title',)
    empty_value = 'No category'


class MessageAdmin(ModelAdmin):
    model = Message
    menu_label = "Messages"
    menu_icon = 'list-ul'
    menu_order = 292
    list_display = ('title', 'slug', 'type')
    list_filter = ('type',)
    empty_value = 'No category'



@modeladmin_register
class ContactGroup(ModelAdminGroup):
    menu_label = 'Contacts'
    menu_icon = 'folder-open-inverse'
    menu_order = 170  
    items = (ContactPageAdmin, EmailAdmin, MessageAdmin)
