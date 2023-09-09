from django.contrib import admin
from django.urls import path, include
from django.urls import re_path as url
from django.conf import settings
from django.conf.urls.static import static
from django.views.static import serve
from django.views.generic import RedirectView
from django.views.generic import TemplateView

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include("api.urls")),
    path('backend/', include("backend.urls")),
    path('', include("frontend.urls")),
    #static files setup
    url(r'^favicon\.ico$',RedirectView.as_view(url='/static/assets/favicon.ico')),
    path('robots.txt', TemplateView.as_view(template_name="robots.txt", content_type='text/plain')),
    url(r'^media/(?P<path>.*)$', serve,{'document_root': settings.MEDIA_ROOT}),
    url(r'^static/(?P<path>.*)$', serve,{'document_root': settings.STATIC_ROOT}),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)