from apscheduler.schedulers.background import BackgroundScheduler
from apscheduler.triggers.cron import CronTrigger
from pytz import timezone
from app.jobs.daily_summary import daily_delivery_summary
from app.jobs.expiry_reminder import expiry_reminder_job
scheduler = BackgroundScheduler(
    timezone=timezone("Asia/Kolkata")
)

scheduler.add_job(
    daily_delivery_summary,
    "cron",
    hour=7,
    minute=0,
)

scheduler.add_job(
    expiry_reminder_job,
    "cron",
    hour=9,
    minute=0,
)