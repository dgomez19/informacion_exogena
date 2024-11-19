# Generated by Django 5.0.8 on 2024-11-18 13:30

import django.utils.timezone
import model_utils.fields
import uuid
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='File',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created', model_utils.fields.AutoCreatedField(default=django.utils.timezone.now, editable=False, verbose_name='created')),
                ('modified', model_utils.fields.AutoLastModifiedField(default=django.utils.timezone.now, editable=False, verbose_name='modified')),
                ('uuid', models.UUIDField(default=uuid.uuid4, editable=False, unique=True)),
                ('number_records', models.IntegerField(verbose_name='Número de registros del archivo')),
                ('status', models.PositiveSmallIntegerField(choices=[(1, 'PENDIENTE'), (2, 'EN PROCESO'), (3, 'TERMINADO EXITOSAMENTE'), (4, 'TERMINADO CON ERRORES')], default=1, verbose_name='Estado del archivo')),
                ('name', models.IntegerField(verbose_name='Nombre del archivo')),
                ('file_date', models.DateTimeField(verbose_name='Fecha del archivo')),
            ],
            options={
                'abstract': False,
            },
        ),
    ]
