from django.conf import settings
from django.apps import AppConfig


class AnalysisConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'analysis'

    def ready(self):
        if settings.SCHEDULER_DEFAULT:
            from . import operator
            operator.start()