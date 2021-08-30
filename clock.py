from apscheduler.schedulers.blocking import BlockingScheduler
import datetime 
import urllib
from urllib.request import urlopen

sched = BlockingScheduler()

@sched.scheduled_job('cron',hour = '0-12',minute='*/20')
def scheduled_job():
    print('========== APScheduler CRON =========')
    # 馬上讓我們瞧瞧
    print('This job runs 6am-0am every day */20 min.')
    # 利用datetime查詢時間
    print(f'{datetime.datetime.now().ctime()}')
    print('========== APScheduler CRON =========')


    url = "https://ben-app-blog.herokuapp.com/home"
    conn = urllib.request.urlopen(url)
        
    for key, value in conn.getheaders():
        print(key, value)

sched.start()