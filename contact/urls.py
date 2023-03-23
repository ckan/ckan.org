from django.urls import path
from .views import activate_subscription, SubscriptionPage


urlpatterns = [
    path('subscription/', SubscriptionPage.as_view(), name='subscription_page'),
    path('subscription/activate/<eidb64>/<token>', activate_subscription, name='subscription_activate'), 
]