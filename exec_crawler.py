from config import Config
from StockStatus import StockStatusBot
from celery import Celery
from celery.schedules import crontab
import os

app = Celery('tasks', broker='redis://localhost:6379/0')


@app.on_after_configure.connect
def setup_periodic_tasks(sender, **kwargs):
    """
    Function will execute the crawler every at every hours
    command for a help: celery -A exec_crawler worker -l info -B
    """
    sender.add_periodic_task(crontab(minute='*/60'), run_crawler.s(), name='call every first minute of every hour')

@app.task
def run_crawler():
    bet = StockStatusBot(Config())
