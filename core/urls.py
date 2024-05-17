from django.contrib import admin
from django.urls import path, include
from .yasg import urlpatterns as doc_ts
from django.conf import settings
from django.conf.urls.static import static


urlpatterns = [
    path('admin/', admin.site.urls),
    path("", include("apps.route")),
]

urlpatterns += doc_ts

if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
