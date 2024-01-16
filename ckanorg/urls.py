from django.conf import settings
from django.urls import include, path
from django.contrib import admin

from wagtail.admin import urls as wagtailadmin_urls
from wagtail import urls as wagtail_urls
from wagtail.documents import urls as wagtaildocs_urls

from search import views as search_views

from contact.views import ajax_email, ajax_unsubscribe
from home.views import csrf
from . import views as ckanorg_views

urlpatterns = [
    path('django-admin/', admin.site.urls),

    path('admin/', include(wagtailadmin_urls)),
    path('documents/', include(wagtaildocs_urls)),

    path('search/', search_views.search, name='search'),

    path('ajax-posting/', ajax_email, name='ajax_email'),
    path('ajax-unsubscribe/', ajax_unsubscribe, name='ajax_unsubscribe'),
    path('newsletter/', include('contact.urls')),
    path('csrf/', csrf, name='csrf'),
    path('404/', ckanorg_views.not_found, name='not_found'),
    path('500/', ckanorg_views.server_error, name='server_error'),
    path('accounts/', include('allauth.urls')),
    path('blog/', include('blog.urls')),
    path('ckan/', include('ckan_pages.urls')),
    path('captcha/', include('captcha.urls')),
]

if settings.DEBUG:
    from django.conf.urls.static import static
    from django.contrib.staticfiles.urls import staticfiles_urlpatterns

    # Serve static and media files from development server
    urlpatterns += staticfiles_urlpatterns()
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

urlpatterns = urlpatterns + [
    path("", include(wagtail_urls)),
]
