from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
from django.urls import include, path
from django.views.generic.base import TemplateView

from wagtail import urls as wagtail_urls
from wagtail.admin import urls as wagtailadmin_urls
from wagtail.documents import urls as wagtaildocs_urls

from contact.views import ajax_email, ajax_unsubscribe
from home.views import csrf
from . import views as ckanorg_views

urlpatterns = [
    path("django-admin/", admin.site.urls),
    path("admin/", include(wagtailadmin_urls)),
    path("documents/", include(wagtaildocs_urls)),
    path("search/", include("search.urls")),
    path("ajax-posting/", ajax_email, name="ajax_email"), # type: ignore
    path("ajax-unsubscribe/", ajax_unsubscribe, name="ajax_unsubscribe"),
    path("newsletter/", include("contact.urls")),
    path("csrf/", csrf, name="csrf"),
    path("404/", ckanorg_views.not_found, name="not_found"),
    path("500/", ckanorg_views.server_error, name="server_error"),
    path("accounts/", include("allauth.urls")),
    path("blog/", include("blog.urls")),
    path("ckan/", include("ckan_pages.urls")),
    path("events/", include("events.urls")),
    path("portals/", include("portals.urls")),
    path("robots.txt", TemplateView.as_view(template_name="robots.txt", content_type="text/plain")),
    path("20-years-of-ckan/", include("anniversary.urls")),
]

# Serve static and media files
urlpatterns += staticfiles_urlpatterns()
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

urlpatterns = urlpatterns + [
    path("", include(wagtail_urls)),
]
