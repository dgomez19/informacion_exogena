from rest_framework import generics, filters, status

from apps.core.models import (
    File,
    FileDetail
)

from rest_framework.generics import ListAPIView

from apps.core import serializers

from django_filters.rest_framework import DjangoFilterBackend

from config.mixins import ProtectedForeignKeyDeleteMixin

from config.renderers import ExcelRenderer

from datetime import datetime


class FileCreateAPIView(generics.ListCreateAPIView):

    authentication_classes = []
    permission_classes = []

    queryset = File.objects.all()

    filter_backends = (DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter)

    serializer_class = serializers.FileListSerializer

    search_fields = ('name',)

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

    search_fields = ('social_reason', 'number_document')

    queryset = FileDetail.objects.all()
    ordering = ('-id',)
    serializer_class = serializers.FileDetailListSerializer
    lookup_field = 'uuid'

    def get_queryset(self):
        qs = super().get_queryset()

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

    renderer_classes = [ExcelRenderer]

    pagination_class = None

    filename = 'reporte_terceros{today}.xlsx'

    queryset = FileDetail.objects.all()

    serializer_class = serializers.FileDetailExcelSerializer

    search_fields = ()

    filterset_fields = {}

    column_header = {
        'titles': ['TIPO DE DOCUMENTO', 'NÚMERO DE DOCUMENTO', 'RAZÓN SOCIAL', 'APELLIDOS', 'DIRECCIÓN', 'DIRECICÓN COMPUESTA', 'CORREO', 'DEPARTAMENTO', 'MUNICIPIO', 'PAIS', 'TELÉFONO', 'CELULAR', 'DIRECCIÓN DE NOTIFICACIÓN'],
        'height': 30,
        'style': {
            'alignment': {
                'horizontal': 'center',
                'vertical': 'center',
                'wrapText': True,
                'shrink_to_fit': False,
            },
            'font': {
                'name': 'Arial',
                'size': 11,
                'bold': True,
                'color': 'FF000000',
            },
        },
    }

    body = {
        'height': 15,
        'style': {
            'alignment': {
                'horizontal': 'center',
                'vertical': 'center',
                'wrapText': False,
                'shrink_to_fit': False,
            },
            'font': {
                'name': 'Arial',
                'size': 10,
                'bold': False,
                'color': 'FF000000',
            }
        },
    }

    def get_queryset(self):
        qs = super().get_queryset()
        return qs

    def transform_data(self, data):
        last_row = {}

        return [*data, {}, last_row]
