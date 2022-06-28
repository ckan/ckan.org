from django.contrib.auth.models import User
from django.views.generic.list import ListView
from .models import BlogPostPage


class UsersBlogPostListView(ListView):

    model = BlogPostPage

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user_name = self.kwargs.get('username', '')
        author = User.objects.get(username=user_name)
        context['posts'] = BlogPostPage.objects.filter(owner=author.id)
        context['author'] = author
        return context


class TagsBlogPostListView(ListView):

    model = BlogPostPage

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        tag = self.kwargs.get('tag', '')
        context['posts'] = BlogPostPage.objects.filter(tags__name=tag)
        context['tag'] = tag
        return context
