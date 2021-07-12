from django.urls import path

from .views import UsersBlogPostListView

urlpatterns = [
    path('author/<username>', UsersBlogPostListView.as_view(), name='user_post_list'),
]
