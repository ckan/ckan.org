from django.contrib.auth.models import User
from django.views.generic.list import ListView

from .models import BlogPostPage

class UsersBlogPostListView(ListView):

    model = BlogPostPage

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        author = self.kwargs.get('username', '')
        author_id = User.objects.get(username=author).id
        context['posts'] = BlogPostPage.objects.filter(owner=author_id)
        context['author'] = author
        return context
