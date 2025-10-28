from django.urls import path
from .models import OpenDataPortalPage

urlpatterns = [
    path('autocomplete/', OpenDataPortalPage.autocomplete_view, name='portal_autocomplete'),
]
