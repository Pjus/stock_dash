from datetime import datetime
from apscheduler.schedulers.background import BackgroundScheduler
from django.conf import settings
from apscheduler.executors.pool import ProcessPoolExecutor, ThreadPoolExecutor
from django_apscheduler.jobstores import register_events, DjangoJobStore
import time
from .modules import get_index, get_finviz_news, get_calender, get_currency, update_company_infos, update_company_price
from .models import CompanyPrice, FinNews, FinancialEvent, Currency, StockCompany, SendMail
from django.db.models import Q

def start():
    scheduler=BackgroundScheduler()
    scheduler.add_jobstore(DjangoJobStore(), 'djangojobstore')
    register_events(scheduler)
    @scheduler.scheduled_job('cron', hour='9', minute = '5', name = 'auto_get_index')
    def auto_get_index():
        print("Index")
        nasdaq = "^IXIC"
        dow = "^DJI"
        snp = "^GSPC"
        CompanyPrice.objects.filter(
                            Q(ticker=nasdaq)|
                            Q(ticker=dow)|
                            Q(ticker=snp)
                            ).delete()
        get_index(nasdaq)
        get_index(dow)
        get_index(snp)
    
    @scheduler.scheduled_job('cron', hour='10', minute = '50', name = 'auto_get_news')
    def auto_get_news():
        print("News")
        FinNews.objects.all().delete()
        get_finviz_news()

    @scheduler.scheduled_job('cron', hour='8', minute = '55', name = 'auto_get_calender')
    def auto_get_calender():
        print("Calender")
        FinancialEvent.objects.all().delete()
        get_calender()

    @scheduler.scheduled_job('cron', hour='9', minute = '45', name = 'auto_get_currency')
    def auto_get_currency():
        print("Currency")
        Currency.objects.all().delete()
        get_currency()

    @scheduler.scheduled_job('cron', hour='9', minute = '10', name = 'auto_update_stock_infos')
    def auto_update_stock_infos():
        not_update = ["^IXIC", "^DJI", "^GSPC"]
        print("Update Stocks Infos")

        all_company = StockCompany.objects.filter()
        for company in all_company:
            if company.ticker not in not_update:
                update_company_infos(company.ticker, company)


    @scheduler.scheduled_job('cron', hour='23,0,1,2,3,4,5', minute = '*/1', name = 'auto_update_stock_price')
    def auto_update_stock_price():
        not_update = ["^IXIC", "^DJI", "^GSPC"]
        print("Update Stocks Price")

        all_company = StockCompany.objects.filter()
        for company in all_company:
            if company.ticker not in not_update:
                update_company_price(company.ticker, company)


    @scheduler.scheduled_job('cron', hour='18', minute = '0', name = 'auto_send_email')
    def auto_send_email():
        all_mail_user = SendMail.objects.filter()
        



    scheduler.start()