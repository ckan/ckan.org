from django.urls import path, re_path
from .views import activate_subscription, SubscriptionPage


urlpatterns = [
    re_path(r'subscription/?$', SubscriptionPage.as_view(), name='subscription_page'),
    path('subscription/activate/<eidb64>/<token>', activate_subscription, name='subscription_activate'), 
]