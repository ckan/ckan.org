from django.urls import path
from .views import (
    UsersBlogPostListView,
    TagsBlogPostListView,
    CategoriesBlogPostListView,
    SearchBlogPostListView
)


urlpatterns = [
    path('author/<username>', UsersBlogPostListView.as_view(), name='user_post_list'),
    path('tag/<tag>', TagsBlogPostListView.as_view(), name='tag_post_list'),
    path('category/<cat_id>', CategoriesBlogPostListView.as_view(), name='category_post_list'),
    path('search', SearchBlogPostListView.as_view(), name='search_post_list'),
]
