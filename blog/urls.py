from django.urls import path
from .views import UsersBlogPostListView, TagsBlogPostListView


urlpatterns = [
    path('author/<username>', UsersBlogPostListView.as_view(), name='user_post_list'),
    path('tag/<tag>', TagsBlogPostListView.as_view(), name='tag_post_list'),
]
