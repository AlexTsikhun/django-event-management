import os

from celery import Celery

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "event_management.settings")

application = Celery("event_management")

application.config_from_object("django.conf:settings", namespace="CELERY")

application.autodiscover_tasks()
