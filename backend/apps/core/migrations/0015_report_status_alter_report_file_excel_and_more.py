# Generated by Django 5.0.8 on 2025-01-08 17:47

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0014_report_alter_file_versioning'),
    ]

    operations = [
        migrations.AddField(
            model_name='report',
            name='status',
            field=models.PositiveSmallIntegerField(choices=[(1, 'PENDIENTE'), (2, 'EN PROCESO'), (3, 'TERMINADO EXITOSAMENTE'), (4, 'TERMINADO CON ERRORES')], default=1, verbose_name='Estado del archivo'),
        ),
        migrations.AlterField(
            model_name='report',
            name='file_excel',
            field=models.FileField(max_length=200, null=True, upload_to='reports'),
        ),
        migrations.AlterField(
            model_name='report',
            name='file_pdf',
            field=models.FileField(max_length=200, null=True, upload_to='reports'),
        ),
    ]
