from django.apps import AppConfig


class UniversityConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'university'

class WomenConfig(AppConfig):
    name = 'news'
    verbose_name = 'Новости универа'