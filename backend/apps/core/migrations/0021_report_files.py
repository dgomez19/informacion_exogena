# Generated by Django 5.0.8 on 2025-01-20 13:20

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0020_report_columns_report_grouped_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='report',
            name='files',
            field=models.CharField(null=True, verbose_name='Archivos'),
        ),
    ]
