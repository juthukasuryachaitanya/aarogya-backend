
from apscheduler.schedulers.background import BackgroundScheduler
from pytz import timezone

from app.jobs.daily_summary import daily_delivery_summary

# -------------------------------------------------
# Scheduler Configuration
# -------------------------------------------------
scheduler = BackgroundScheduler(
    timezone=timezone("Asia/Kolkata")
)

# -------------------------------------------------
# DAILY DELIVERY SUMMARY (ADMIN LOG ONLY)
# Runs every day at 7:00 AM IST
# -------------------------------------------------
scheduler.add_job(
    daily_delivery_summary,
    trigger="cron",
    hour=7,
    minute=0,
    id="daily_delivery_summary",
    replace_existing=True
)