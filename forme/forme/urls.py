from django.contrib import admin
from django.urls import path, include
from django.conf.urls.static import static

from . import settings


urlpatterns = [
    path("admin/", admin.site.urls),
    path("account/", include("account.urls")),
    path("auth/", include("authentication.urls")),
    path("clubs/", include("clubs.urls")),
    path("trainings/", include("trainings.urls")),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
