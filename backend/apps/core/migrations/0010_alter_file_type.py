# Generated by Django 5.0.8 on 2024-11-20 08:35

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0009_file_type'),
    ]

    operations = [
        migrations.AlterField(
            model_name='file',
            name='type',
            field=models.CharField(verbose_name='Tipo'),
        ),
    ]
