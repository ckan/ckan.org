from django.views.generic.list import ListView
from .models import SoftwareEngineers


class SoftwareEngineersListView(ListView):

    model = SoftwareEngineers
    template_name = "ckan_pages/former_members_page.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['engineers'] = SoftwareEngineers.objects.filter(developer__active=False)
        return context