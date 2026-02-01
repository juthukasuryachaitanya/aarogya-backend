from apscheduler.schedulers.background import BackgroundScheduler
from apscheduler.triggers.cron import CronTrigger
from pytz import timezone

scheduler = BackgroundScheduler(
    timezone=timezone("Asia/Kolkata")
)

