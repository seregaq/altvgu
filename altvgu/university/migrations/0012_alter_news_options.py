# Generated by Django 5.1.7 on 2025-05-27 10:18

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('university', '0011_news_visibility'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='news',
            options={'permissions': [('can_publish', 'Может публиковать новости'), ('can_edit', 'Может редактировать новости')], 'verbose_name': 'Новость', 'verbose_name_plural': 'Новости'},
        ),
    ]
