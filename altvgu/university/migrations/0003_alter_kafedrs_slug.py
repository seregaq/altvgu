# Generated by Django 4.2.1 on 2025-03-18 04:35

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('university', '0002_alter_kafedrs_options_kafedrs_slug_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='kafedrs',
            name='slug',
            field=models.SlugField(max_length=255, unique=True),
        ),
    ]
