from django.urls import path

from .views import EventVideoPageView, get_events_data


urlpatterns = [
    path("<slug>/video/<timelog>", EventVideoPageView.as_view(), name="event_video_page"),
    path("ajax", get_events_data, name="ajax_events"),
]
