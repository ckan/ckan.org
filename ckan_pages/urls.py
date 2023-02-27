from django.urls import path
# from django.views.generic import TemplateView
from .views import SoftwareEngineersListView, SubscribePageView


urlpatterns = [
    path('former-members/', SoftwareEngineersListView.as_view(), name='former_members'),
    path('email-newsletter-sign-up', SubscribePageView.as_view(), name='subscribe_page'),
]