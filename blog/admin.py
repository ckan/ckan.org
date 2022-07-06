from wagtail.contrib.modeladmin.options import (
    ModelAdmin,
    modeladmin_register
)
from .models import Profile


@modeladmin_register
class ProfileAdmin(ModelAdmin):
    model = Profile
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
        print(request.user.groups.all())
        if request.user.groups.all()[0].name == "Blog Post Creators" and len(request.user.groups.all()) == 1:
            qs = qs.filter(user=request.user)
        return qs
