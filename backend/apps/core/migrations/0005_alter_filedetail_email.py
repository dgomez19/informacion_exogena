# Generated by Django 5.0.8 on 2024-11-18 16:46

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0004_alter_file_file_route_filedetail'),
    ]

    operations = [
        migrations.AlterField(
            model_name='filedetail',
            name='email',
            field=models.EmailField(blank=True, max_length=254),
        ),
    ]
