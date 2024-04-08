from django.contrib import admin
from django.urls import path, include
from .yasg import urlpatterns as doc_ts
from django.conf import settings
from django.conf.urls.static import static


urlpatterns = [
    path('admin/', admin.site.urls),
    path("auth/", include("accounts.urls")),
]


urlpatterns += doc_ts

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
