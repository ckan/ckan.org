from django.contrib import admin

from wagtail.contrib.modeladmin.options import ModelAdmin, ModelAdminGroup, modeladmin_register

from .models import FaqCategoryPage, FaqQuestionPage


class FaqCategoryPageAdmin(ModelAdmin):
    model = FaqCategoryPage
    menu_label = "Categories"
    menu_icon = 'list-ul'
    menu_order = 100
    list_display = ('name', )
    search_fields = ('name',) 


class FaqQuestionPageAdmin(ModelAdmin):
    model = FaqQuestionPage
    menu_label = "Questions"
    menu_icon = 'help'
    menu_order = 200
    list_display = ('question', 'category')
    list_filter = ('category',)
    search_fields = ('question',) 
    empty_value = 'No category'


@modeladmin_register
class FaqGroup(ModelAdminGroup):
    menu_label = 'FAQ'
    menu_icon = 'folder-open-inverse'
    menu_order = 200  
    items = (FaqCategoryPageAdmin, FaqQuestionPageAdmin)
