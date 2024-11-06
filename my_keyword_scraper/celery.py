from __future__ import absolute_import, unicode_literals
import os
from celery import Celery
from django.conf import settings


os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'my_keyword_scraper.settings')

app = Celery('my_keyword_scraper')
app.config_from_object(settings, namespace='CELERY')
app.conf.enable_utc = False
app.autodiscover_tasks()

@app.task(bind=True)
def debug_task(self):
    print(f'Request: {self.request!r}')
