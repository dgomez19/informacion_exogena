import uuid

import random

import string

from django.db import models, transaction

from rest_framework import exceptions

from model_utils.models import TimeStampedModel

from datetime import datetime, timedelta

from django.conf import settings

from django.core.files import File

from django.apps import apps

from django.db.models import Q

from .utils import (
    file_path,
)

from django.core import validators


class File(TimeStampedModel):
    """
    Almacena la informacion del archivo en excel cargado
    """
    PENDING = 1
    IN_PROGRESS = 2
    SUCCESSFULLY_COMPLETED = 3
    FINISHED_ERRORS = 4

    CHOICE_STATUS = (
        (PENDING, 'PENDIENTE'),
        (IN_PROGRESS, 'EN PROCESO'),
        (SUCCESSFULLY_COMPLETED, 'TERMINADO EXITOSAMENTE'),
        (FINISHED_ERRORS, 'TERMINADO CON ERRORES')
    )

    uuid = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)

    number_records = models.IntegerField(
        verbose_name='Número de registros del archivo'
    )

    status = models.PositiveSmallIntegerField(
        verbose_name="Estado del archivo",
        choices=CHOICE_STATUS,
        default=PENDING
    )

    name = models.CharField(
        verbose_name='Nombre del archivo'
    )

    file_route = models.FileField(
        upload_to='file_path',
        max_length=128,
        validators=[validators.FileExtensionValidator(['xls', 'xlsx', 'csv'])]
    )

    file_date = models.DateTimeField(
        verbose_name='Fecha del archivo',
        null=True
    )

    type = models.CharField(
        verbose_name="Tipo",
    )


class FileDetail(TimeStampedModel):

    TYPE_DOCUMENT_CC = 1

    CHOICE_TYPE_DOCUMENT = (
        (TYPE_DOCUMENT_CC, 'PENDIENTE'),
    )

    uuid = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)

    file = models.ForeignKey('core.File', on_delete=models.PROTECT)

    type_document = models.PositiveSmallIntegerField(
        verbose_name="Tipo de documento",
        choices=CHOICE_TYPE_DOCUMENT,
        default=TYPE_DOCUMENT_CC
    )

    number_document = models.CharField(
        verbose_name='Número de documento'
    )

    social_reason = models.CharField(
        verbose_name='Número de documento',
    )

    surnames = models.CharField(
        verbose_name='Número de documento',
        blank=True
    )

    address = models.CharField(
        verbose_name='Dirección',
        blank=True
    )

    compound_address = models.CharField(
        verbose_name='Dirección compuesta',
        blank=True
    )

    email = models.EmailField(blank=True)

    department = models.CharField(
        verbose_name='Departamento',
        blank=True
    )

    municipality = models.CharField(
        verbose_name='Municipio',
        blank=True
    )

    country = models.CharField(
        verbose_name='País',
        blank=True
    )

    phone = models.CharField(
        verbose_name='Teléfono',
        blank=True
    )

    cell_phone = models.CharField(
        verbose_name='Celular',
        blank=True
    )

    notification_address = models.CharField(
        verbose_name='Dirección de notificación',
        blank=True
    )
