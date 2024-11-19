from rest_framework import serializers

from apps.core.models import (
    File
)

from django.utils import timezone

from django.conf import settings

from apps.core.tasks import (
    upload_file,
)

class FileCreateSerializer(serializers.ModelSerializer):

    class Meta:
        model = File
        fields = [
            'number_records',
            'status',
            'name',
            'file_date',
            'file_route'
        ]

    def create(self, validated_data):
        upload_file()
        # upload_file.delay()
        return File.objects.create(**validated_data)


class FileListSerializer(serializers.ModelSerializer):

    status = serializers.SerializerMethodField()

    class Meta:
        model = File
        fields = [
            'number_records',
            'status',
            'name',
            'file_date',
            'file_route'
        ]

    def get_status(self, obj):
        return {'code': obj.status, 'description': obj.get_status_display()}
