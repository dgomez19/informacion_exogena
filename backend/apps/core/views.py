from rest_framework import generics, filters, status

from apps.core.models import (
    File,
    FileDetail,
    Versioning,
    Report
)

from rest_framework.generics import ListAPIView

from apps.core import serializers

from django_filters.rest_framework import DjangoFilterBackend

from config.mixins import ProtectedForeignKeyDeleteMixin

from config.renderers import ExcelRenderer

from datetime import datetime

from apps.core.tasks import (
    generate_excel_report
)

from rest_framework.response import Response

from django.db.models import Count


class FileCreateAPIView(generics.ListCreateAPIView):

    authentication_classes = []

    permission_classes = []

    queryset = File.objects.all().order_by('-id')

    filter_backends = (DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter)

    serializer_class = serializers.FileListSerializer

    search_fields = ('name',)

    filterset_fields = [
        'versioning__uuid',
        'status'
    ]

    ordering = ('-id',)

    def get_serializer_class(self):
        if self.request.method == "POST":
            return serializers.FileCreateSerializer
        return serializers.FileListSerializer


class FileRetrieveUpdateDestroyAPIView(
    ProtectedForeignKeyDeleteMixin,
    generics.RetrieveUpdateDestroyAPIView
):
    authentication_classes = []
    permission_classes = []

    queryset = File.objects.all()

    lookup_field = 'uuid'

    serializer_class = serializers.FileListSerializer

    def get_serializer_class(self):
        if self.request.method in ["PUT", "PATCH"]:
            return serializers.FileCreateSerializer
        return serializers.FileListSerializer


class FileDetailListAPIView(ListAPIView):
    authentication_classes = []

    permission_classes = []

    filter_backends = (DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter)

    # search_fields = ('social_reason', 'number_document')

    filterset_fields = {
        'file__uuid': ['in'],
        'file__versioning__uuid': ['exact']
    }

    queryset = FileDetail.objects.all()

    ordering = ('-id',)

    serializer_class = serializers.FileDetailListSerializer

    lookup_field = 'uuid'

    def get_serializer_class(self):
        if self.request.GET.get('grouped'):
            return serializers.FileDetailListGrouped
        return serializers.FileDetailListSerializer

    def get_queryset(self):
        qs = super().get_queryset()

        column = list()

        if self.request.GET.get('columns__in'):
            column = self.request.GET.get('columns__in').split(',')

        if self.request.GET.get('search'):
            qs = qs.filter(number_document__in=self.request.GET.get('search').split(" "))

        column.append('number_document')

        if self.request.GET.get('grouped'):
            qs = qs.values(
                *column
            ).annotate(
                count=Count('number_document')
            ).order_by(
                'number_document'
            )

            return qs

        if 'created' in self.request.GET:
            fechas = self.request.GET['created'].split(':')
            try:
                de = datetime.strptime(fechas[0], '%Y-%m-%d').date()
                hasta = datetime.strptime(fechas[1], '%Y-%m-%d').date()
            except ValueError:
                return Response({"detail": "El formato de las fechas no es correcto, debe ser YYYY-MM-DD."},
                                status=status.HTTP_400_BAD_REQUEST)

            qs = qs.filter(created__date__range=(de, hasta)).order_by('-id')

        return qs


class ReportFileDetailExcelListAPIView(ListAPIView):
    authentication_classes = []

    permission_classes = []

    def get(self, request, *args, **kwargs):
        versioning = None

        if self.request.GET.get('versioning'):
            versioning = Versioning.objects.filter(uuid=self.request.GET.get('versioning')).first()

        report = Report.objects.create(
            file_excel=None,
            file_pdf=None,
            document=self.request.GET.get('number_document'),
            columns=self.request.GET.get('columns__in'),
            grouped=self.request.GET.get('grouped'),
            files=str(self.request.GET.get('file__uuid__in')) if self.request.GET.get('file__uuid__in') else None,
            versioning=versioning,
            status=File.PENDING
        )

        # generate_excel_report(report.id)
        generate_excel_report.delay(report.id)
        return Response("Done", status=status.HTTP_200_OK)



class VersioningListCreateAPIView(generics.ListCreateAPIView):

    authentication_classes = []

    permission_classes = []

    queryset = Versioning.objects.all()

    filter_backends = (DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter)

    serializer_class = serializers.VersioningListSerializer

    search_fields = ('name',)

    ordering = ('-id',)

    def get_serializer_class(self):
        if self.request.method == "POST":
            return serializers.VersioningCreateSerializer
        return serializers.VersioningListSerializer


class VersioningRetrieveUpdateDestroyAPIView(
    ProtectedForeignKeyDeleteMixin,
    generics.RetrieveUpdateDestroyAPIView
):
    authentication_classes = []

    permission_classes = []

    queryset = Versioning.objects.all()

    lookup_field = 'uuid'

    serializer_class = serializers.VersioningListSerializer

    def get_serializer_class(self):
        if self.request.method in ["PUT", "PATCH"]:
            return serializers.VersioningCreateSerializer
        return serializers.VersioningListSerializer


class ReportListAPIView(ListAPIView):
    authentication_classes = []

    permission_classes = []

    filter_backends = (DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter)

    queryset = Report.objects.all()

    ordering = ('-id',)

    serializer_class = serializers.ReportListSerializer

    lookup_field = 'uuid'
