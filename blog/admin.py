import inspect
from wagtail.contrib.modeladmin.options import (
    ModelAdmin,
    ModelAdminGroup,
    modeladmin_register
)
from .models import Profile, BlogPostPage, PostCategoryPage
from .views import ProfileCreateView


@modeladmin_register
class ProfileAdmin(ModelAdmin):
    model = Profile
    create_view_class = ProfileCreateView
    menu_label = "Profiles"
    menu_icon = 'user'
    menu_order = 600
    add_to_settings_menu = False
    exclude_from_explorer = False
    list_display = ('user', 'company', 'location')
    list_filter = ('company', 'location')
    search_fields = ('user', 'company') 

    def get_queryset(self, request):
        qs = super().get_queryset(request)
        if request.user.is_superuser:
            return qs
        else:
            if request.user.groups.all()[0].name == "Blog Post Creators" and len(request.user.groups.all()) == 1:
                qs = qs.filter(user=request.user)
        return qs


class BlogPostPageAdmin(ModelAdmin):
    model = BlogPostPage
    menu_label = "Posts"
    menu_icon = 'doc-empty-inverse'
    menu_order = 100
    list_display = ('post_title', 'author', 'created', 'last_published_at')
    list_filter = ('category', 'live')
    search_fields = ('post_title', 'author', 'created', 'last_published_at') 

    def get_queryset(self, request):
        qs = super().get_queryset(request)
        if request.user.is_superuser:
            return qs
        else:
            if request.user.groups.all()[0].name == "Blog Post Creators" and len(request.user.groups.all()) == 1:
                qs = qs.filter(owner=request.user.id)
        return qs


class PostCategoryPageAdmin(ModelAdmin):
    model = PostCategoryPage
    menu_label = "Categories"
    menu_icon = 'list-ul'
    menu_order = 200
    list_display = ('category_title',)
    search_fields = ('category_title',) 
    empty_value = 'No category'


@modeladmin_register
class BlogGroup(ModelAdminGroup):
    menu_label = 'Blog'
    menu_icon = 'folder-open-inverse'
    menu_order = 150  
    items = (BlogPostPageAdmin, PostCategoryPageAdmin)