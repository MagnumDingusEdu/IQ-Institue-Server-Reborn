from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from django.conf.urls import url

urlpatterns = [
    path("admin/", admin.site.urls),
    path("api-auth/", include("rest_framework.urls", namespace="rest_framework")),
    path("lectures/", include("lectures.urls")),
    path("users/", include("users.urls")),
    url(
        r"^users/password_reset/",
        include("django_rest_passwordreset.urls", namespace="password_reset"),
    ),
]

if settings.DEBUG:
    # Add urls for the debug toolbar
    import debug_toolbar

    urlpatterns += [path("__debug__", include(debug_toolbar.urls))]

    # Static and media serving
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
