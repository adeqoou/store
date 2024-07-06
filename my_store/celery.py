import os
from celery import Celery
from celery.schedules import crontab

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'my_store.settings')

app = Celery('my_store')
app.config_from_object('django.conf:settings', namespace='CELERY')
app.autodiscover_tasks()

app.conf.beat_schedule = {
    'send-email-every-5-minutes': {
        'task': 'poll.tasks.send_beat_email',
        'schedule': crontab(minute='*/5'),
    }
}
