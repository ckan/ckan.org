from django.shortcuts import render
from wagtailcache.cache import nocache_page


@nocache_page
def csrf(request):
    return render(request, "snippets/csrf.html")
