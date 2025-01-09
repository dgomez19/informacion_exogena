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
    ),

    path(
        'file-detail/',
        views.FileDetailListAPIView.as_view(),
        name='core-file-detail-api'
    ),

    path(
        'report-file-detail/',
        views.ReportFileDetailExcelListAPIView.as_view(),
        name='core-report-file-detail-api'
    ),

    path(
        'versioning/',
        views.VersioningListCreateAPIView.as_view(),
        name='core-versioning-api'
    ),

    path(
        'versioning/<uuid:uuid>/',
        views.VersioningRetrieveUpdateDestroyAPIView.as_view(),
        name='core-versioning-api'
    ),

    path(
        'report/',
        views.ReportListAPIView.as_view(),
        name='core-report-api'
    )
]
