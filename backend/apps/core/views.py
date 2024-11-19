from rest_framework import generics, filters

from apps.core.models import (
    File,
)

from apps.core import serializers

from django_filters.rest_framework import DjangoFilterBackend

from config.mixins import ProtectedForeignKeyDeleteMixin


class FileCreateAPIView(generics.ListCreateAPIView):

    authentication_classes = []
    permission_classes = []

    queryset = File.objects.all()

    filter_backends = (DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter)

    serializer_class = serializers.FileListSerializer

    search_fields = ('number_records__unaccent', 'name__unaccent')

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
