from django.urls import path

from apps.core import views

urlpatterns = [
    path(
        'files/',
        views. FileCreateAPIView.as_view(),
        name='core-file-api'
    ),

    path(
        'files/<uuid:uuid>/',
        views.FileRetrieveUpdateDestroyAPIView.as_view(),
        name='core-file-api'
    )
]
