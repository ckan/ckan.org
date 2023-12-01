from wagtail.snippets.models import register_snippet
from wagtail.snippets.views.snippets import SnippetViewSet, SnippetViewSetGroup

from .models import Profile, BlogPostPage, PostCategoryPage
from .views import ProfileCreateView


@register_snippet
class ProfileAdmin(SnippetViewSet):
    model = Profile
    create_view_class = ProfileCreateView
    menu_label = "Profiles"
    icon = "user"
    menu_order = 600
    add_to_settings_menu = True
    list_display = ("user", "company", "location")
    list_filter = ("company", "location")
    search_fields = ("user", "company")

    def get_queryset(self, request):
        qs = super().get_queryset(request)
        if request.user.is_superuser:
            return qs
        else:
            if (
                request.user.groups.all()[0].name == "Blog Post Creators"
                and len(request.user.groups.all()) == 1
            ):
                qs = qs.filter(user=request.user)
        return qs


class BlogPostPageAdmin(SnippetViewSet):
    model = BlogPostPage
    menu_label = "Posts"
    icon = "doc-empty-inverse"
    menu_order = 100
    list_display = ("post_title", "author", "created", "first_published_at", "last_published_at")
    list_export = ("post_title", "author", "created", "first_published_at", "last_published_at")
    ordering = "-first_published_at"
    list_filter = ("category", "live", "created", "last_published_at")
    search_fields = ("post_title", "author")

    def get_queryset(self, request):
        qs = super().get_queryset(request)
        if request.user.is_superuser:
            return qs
        else:
            if (
                request.user.groups.all()[0].name == "Blog Post Creators"
                and len(request.user.groups.all()) == 1
            ):
                qs = qs.filter(owner=request.user.id)
        return qs


class PostCategoryPageAdmin(SnippetViewSet):
    model = PostCategoryPage
    menu_label = "Categories"
    icon = "list-ul"
    menu_order = 200
    list_display = ("category_title",)
    search_fields = ("category_title",)
    empty_value = "No category"


@register_snippet
class BlogGroup(SnippetViewSetGroup):
    menu_label = "Blog"
    icon = "folder-open-inverse"
    menu_order = 150
    items = (BlogPostPageAdmin, PostCategoryPageAdmin)
