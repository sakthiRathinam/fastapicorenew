from celery import Celery
import os
import asyncio
from asgiref.sync import async_to_sync
from celery.schedules import crontab
from src.config.mongo_conf import virtual_database as db
import time
celery_app = Celery(
    'celery_web',
    broker = os.environ.get("CELERY_BROKER_URL"),
    backend = os.environ.get("CELERY_RESULT_BACKEND"),
    include = ['src.apps.celery.tasks']
)

async def get_db_data():
    ss = "sharma"
    print(ss)
    return ss



@celery_app.task(name="sync_task")
def sync_task():
    new_loop = asyncio.new_event_loop()
    new_loop.run_until_complete(get_db_data())

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
    'test-celery': {
        'task': 'sync_task',
        'schedule':5,
    },
    'add-every-evening-night-morning': {
        'task': 'create_task',
        'schedule':crontab(hour='8,6,9,13,14,20,21',minute=0,day_of_week="mon,tue,wed,thu,fri,sat,sun"),
        'args': (16, 16),
    },
}
