from celery import Celery
import os
from celery.schedules import crontab
import time
celery_app = Celery(
    'celery_web',
    broker = os.environ.get("CELERY_BROKER_URL"),
    backend = os.environ.get("CELERY_RESULT_BACKEND"),
    include = ['src.apps.celery.tasks']
)


@celery_app.task(name="create_task")
def add(a, b):
    return a + b


celery_app.conf.timezone = 'Asia/Kolkata'

celery_app.conf.beat_schedule = {
    # Executes every Monday morning at 7:30 a.m.
    'add-every-evening-night-morning': {
        'task': 'create_task',
        'schedule':crontab(hour='8,6,9,13,14,20,21',minute=0,day_of_week="mon,tue,wed,thu,fri,sat,sun"),
        'args': (16, 16),
    },
}
