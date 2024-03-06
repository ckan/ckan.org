from django.urls import path
from .views import SoftwareEngineersListView


urlpatterns = [
    path("former-members/", SoftwareEngineersListView.as_view(), name="former_members"),
]
