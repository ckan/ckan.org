from django.urls import path
# from django.views.generic import TemplateView
from .views import SoftwareEngineersListView


urlpatterns = [
    path('former-members/', SoftwareEngineersListView.as_view(), name='former_members'),
]