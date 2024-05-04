from django.contrib import admin
from django.urls import path, include
from django.conf.urls.static import static

from . import settings

from drf_yasg import openapi
from drf_yasg.views import get_schema_view as swagger_get_schema_view


schema_view = swagger_get_schema_view(
    openapi.Info(
        title="Forme API",
        default_version="v1",
        description="Forme API documentation",
    ),
    public=True,
)

urlpatterns = [
    path("admin/", admin.site.urls),
    path(
        "api/v1/",
        schema_view.with_ui("swagger", cache_timeout=0),
        name="swagger-schema",
    ),
    path("auth/", include("authentication.urls")),
    path("clubs/", include("clubs.urls")),
    path("social-auth/", include("social_auth.urls")),
    path("trainings/", include("trainings.urls")),
]

if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += [
        path("__debug__/", include("debug_toolbar.urls")),  # <-- Updated!
    ]
