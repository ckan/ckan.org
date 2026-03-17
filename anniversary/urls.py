from django.urls import path
from .views import  AnniversaryView


urlpatterns = [
    path("", AnniversaryView.as_view(), name="anniversary_page"),
]
