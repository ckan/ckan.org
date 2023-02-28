from django.urls import path
from .views import activate_subscription
from django.views.generic import TemplateView


urlpatterns = [
    path('subscription', 
         TemplateView.as_view(template_name='contact/subscription_page.html'), name='subscription_page'),
    path(r'subscription/activate/<eidb64>/<token>', activate_subscription, name='subscription-activate'), 
]