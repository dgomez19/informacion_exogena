from django.conf.urls import include
from django.urls import path
from django.conf.urls.static import static
from django.conf import settings


urlpatterns = [
    path('api/v1/core/', include('apps.core.urls')),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
