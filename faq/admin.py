from wagtail.snippets.models import register_snippet
from wagtail.snippets.views.snippets import SnippetViewSet, SnippetViewSetGroup

from .models import FaqCategoryPage, FaqQuestionPage
from .views import FaqCreateView


class FaqCategoryPageAdmin(SnippetViewSet):
    model = FaqCategoryPage
    menu_label = "Categories"
    icon = "list-ul"
    menu_order = 100
    list_display = ("name",)
    search_fields = ("name",)
    add_view_class = FaqCreateView


class FaqQuestionPageAdmin(SnippetViewSet):
    model = FaqQuestionPage
    menu_label = "Questions"
    icon = "help"
    menu_order = 200
    list_display = ("question", "category")
    list_filter = ("category",)
    search_fields = ("question",)
    empty_value = "No category"
    add_view_class = FaqCreateView


@register_snippet
class FaqGroup(SnippetViewSetGroup):
    menu_label = "FAQ"
    icon = "folder-open-inverse"
    menu_order = 160
    items = (FaqCategoryPageAdmin, FaqQuestionPageAdmin)
