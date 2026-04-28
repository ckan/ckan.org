from django.urls import path
from .views import  StoriesView


urlpatterns = [
    path("", StoriesView.as_view(), name="stories_page"),
]
