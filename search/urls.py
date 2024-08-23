from django.urls import path

from search import views as search_views
from .views import search_autocomplete


urlpatterns = [
    path('', search_views.search, name='search'),
    path("ajax", search_autocomplete, name="ajax_search"),
]
