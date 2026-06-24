from django.urls import path
from .views import subscribe_story_notifications, submit_story

urlpatterns = [
    path("notify/subscribe/", subscribe_story_notifications, name="stories-notify-subscribe"),
    path("submit/", submit_story, name="stories-submit"),
]
