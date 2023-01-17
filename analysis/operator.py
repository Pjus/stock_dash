from datetime import datetime
from apscheduler.schedulers.background import BackgroundScheduler
from django.conf import settings
from apscheduler.executors.pool import ProcessPoolExecutor, ThreadPoolExecutor
from django_apscheduler.jobstores import register_events, DjangoJobStore
import time
from .modules import get_index
from .models import CompanyPrice


def start():
    scheduler=BackgroundScheduler()
    scheduler.add_jobstore(DjangoJobStore(), 'djangojobstore')
    register_events(scheduler)
    @scheduler.scheduled_job('cron', hour='9', minute = '5', name = 'auto_get_index')
    def auto_get_index():
        print("Schedule")
        nasdaq = "^IXIC"
        dow = "^DJI"
        snp = "^GSPC"
        CompanyPrice.objects.all().delete()
        get_index(nasdaq)
        get_index(dow)
        get_index(snp)
    scheduler.start()