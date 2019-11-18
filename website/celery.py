from __future__ import absolute_import, unicode_literals
import os
from datetime import timedelta

from celery import Celery, platforms
from celery.schedules import crontab


os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'website.settings')
app = Celery('website')
app.config_from_object('django.conf:settings', namespace='CELERY')
app.autodiscover_tasks()
app.conf.update(
    CELERYBEAT_SCHEDULE={
        'sum-task': {
            'task': 'deploy.tasks.add',
            'schedule': timedelta(seconds=20),
            'args': (5, 6)
        },
        'send-report': {
            'task': 'deploy.tasks.report',
            'schedule': crontab(hour=4, minute=30, day_of_week=1)
        }
    }
)
platforms.C_FORCE_ROOT = True


@app.task(bind=True)
def debug_task(self):
    print(f'Request: {self.request}')


