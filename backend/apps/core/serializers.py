from rest_framework import serializers

from apps.core.models import (
    File,
    FileDetail,
    Versioning,
    Report
)

from django.utils import timezone

from django.conf import settings

from apps.core.tasks import (
    upload_file,
)

from datetime import datetime

import csv


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
        request = self.context.get("request")

        versioning = Versioning.objects.filter(
            uuid=request.POST.get('versioning')
        ).first()

        for file in request.FILES.getlist('file_route'):
            validated_data['file_route'] = file

            validated_data['versioning'] = versioning

            type = file.name.split('_')

            validated_data['name'] = file.name

            try:
                validated_data['type'] = type[0]
            except Exception:
                validated_data['type'] = 0

            try:
                validated_data['file_date'] = datetime.strptime(str(type[len(type) - 1].split('.')[0]), "%Y%m%d%H%M")
            except Exception:
                validated_data['file_date'] = timezone.now()

            File.objects.create(
                **validated_data
            )

        upload_file()
        # upload_file.delay()
        return File()


class FileDetailExcelSerializer(serializers.ModelSerializer):

    class Meta:
        model = FileDetail
        fields = [
            'type_document',
            'number_document',
            'social_reason',
            'surnames',
            'address',
            'compound_address',
            'email',
            'department',
            'municipality',
            'country',
            'phone',
            'cell_phone',
            'notification_address'
        ]


class VersioningCreateSerializer(serializers.ModelSerializer):

    class Meta:
        model = Versioning
        fields = [
            'name',
            'close'
        ]


class VersioningListSerializer(serializers.ModelSerializer):

    created = serializers.SerializerMethodField()

    class Meta:
        model = Versioning
        fields = [
            'id',
            'uuid',
            'name',
            'close',
            'created',
            'get_files'
        ]

    def get_created(self, obj):
        return obj.created.strftime(settings.FORMATO_FECHA)



class FileListSerializer(serializers.ModelSerializer):

    status = serializers.SerializerMethodField()

    name = serializers.SerializerMethodField()

    versioning = VersioningListSerializer()

    class Meta:
        model = File
        fields = [
            'uuid',
            'number_records',
            'type',
            'status',
            'name',
            'file_date',
            'file_route',
            'created',
            'versioning'
        ]

    def get_status(self, obj):
        return {'code': obj.status, 'description': obj.get_status_display()}

    def get_name(self, obj):
        try:
            return obj.file_route.name.split('/')[1]
        except Exception:
            return obj.file_route


class FileDetailListSerializer(serializers.ModelSerializer):

    type_document = serializers.SerializerMethodField()

    file = FileListSerializer()

    class Meta:
        model = FileDetail
        fields = [
            'uuid',
            'file',
            'type_document',
            'number_document',
            'social_reason',
            'surnames',
            'address',
            'compound_address',
            'email',
            'department',
            'municipality',
            'country',
            'phone',
            'cell_phone',
            'notification_address'
        ]

    def get_type_document(self, obj):
        return {'code': obj.type_document, 'description': obj.get_type_document_display()}


class ReportListSerializer(serializers.ModelSerializer):

    # versioning = VersioningListSerializer()
    status = serializers.SerializerMethodField()

    class Meta:
        model = Report
        fields = [
            'uuid',
            'file_excel',
            'file_pdf',
            'document',
            'versioning',
            'created',
            'status',
            'number_records',
            'phone',
            'cell_phone',
            'address',
            'email'
        ]

    def get_status(self, obj):
        return {
            'code': obj.status,
            'description': obj.get_status_display()
        }
