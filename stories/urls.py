from django.urls import path
from .views import subscribe_story_notifications

urlpatterns = [
    path("notify/subscribe/", subscribe_story_notifications, name="stories-notify-subscribe"),
]
