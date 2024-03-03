"""
В этом файле будут Celery-задачи
"""
from time import sleep
from typing import Optional, List
import os

from celery import Celery, chord, chain, group
from celery.schedules import crontab

import redis

from image import blur_image
from mail import send_email, newsletter
from functions import get_emails_from_csv, archiving_files
from config import MAILING_LIST_FILE, ARCHIVE_NAME


r = redis.Redis(host='localhost', port=6379, decode_responses=True)


celery_app = Celery(
    'celery',
    broker='redis://localhost:6379/0',
    backend='redis://localhost:6379/0',
)

celery_app.conf.timezone = 'Europe/Moscow'


@celery_app.task
def process_image(src_filename: str, dst_filename: Optional[str] = None):
    if os.path.isfile(src_filename):
        sleep(30)
        dst_filename = blur_image(src_filename, dst_filename)
        print('process_image ' + dst_filename)
        return dst_filename
    else:
        raise FileNotFoundError


@celery_app.task(bind=True)
def archiving_and_send_email_results(self, files, email):
    archive_name = archiving_files(files=files, task_id=self.request.id)
    sleep(20)
    send_email(order_id=self.request.id, receiver=email, filename=archive_name)


@celery_app.on_after_configure.connect
def setup_periodic_tasks(sender, **kwargs):
    sender.add_periodic_task(
        crontab(hour='10', minute='30', day_of_week='6'),
        weekly_newsletter.s()
    )


@celery_app.task
def weekly_newsletter():
    emails = get_emails_from_csv(MAILING_LIST_FILE)
    newsletter(emails)
