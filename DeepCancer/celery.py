from __future__ import absolute_import

import celery
import os

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'DeepCancer.settings')


app = celery.Celery('DeepCancer')

app.config_from_object('django.conf:settings', namespace='CELERY')
app.autodiscover_tasks()
