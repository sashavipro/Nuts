"""mysite/celery.py."""

import os
import logging
from celery import Celery

logger = logging.getLogger(__name__)

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "mysite.settings.dev")

app = Celery("mysite")

app.config_from_object("django.conf:settings", namespace="CELERY")

app.autodiscover_tasks()


@app.task(bind=True)
def debug_task(self):
    """
    Debug task to verify Celery worker status.

    It dumps the request context to the logs.
    """
    logger.info("Debug task executed. Request: %r", self.request)
