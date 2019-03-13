from __future__ import absolute_import, unicode_literals
import os
import django
from django.conf import settings

from celery import Celery
from django.apps import apps


# set the default Django settings module for the 'celery' program.
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'test1.settings')
django.setup()  # This is key

app = Celery('test1',
             # backend = settings.CELERY.get('backend'),
             # broker = settings.CELERY.get('broker'),
             include = ['product.tasks'])

# Using a string here means the worker don't have to serialize
# the configuration object to child processes.
# - namespace='CELERY' means all celery-related configuration keys
#   should have a `CELERY_` prefix.
# app.config_from_object('django.conf:settings')
app.config_from_object(settings)

# Load task modules from all registered Django app configs.
# app.autodiscover_tasks()
# app.autodiscover_tasks(lambda: [n.name for n in apps.get_app_configs()])
app.autodiscover_tasks(lambda: settings.INSTALLED_APPS, force=True)

@app.task(bind=True)
def debug_task(self):
    print('Request: {0!r}'.format(self.request))
