from datetime import date, timedelta
from sqlalchemy.orm import Session
from app.core.database import SessionLocal
from app.subscriptions.models import Subscription
from app.alerts.service import send_admin_alert

def expiry_reminder_job():
    db: Session = SessionLocal()
    try:
        target_date = date.today() + timedelta(days=2)

        subs = (
            db.query(Subscription)
            .filter(Subscription.expiry_date == target_date)
            .all()
        )

        for sub in subs:
            send_admin_alert(
                "EXPIRY_REMINDER",
                {
                    "name": sub.name,
                    "expiry": sub.expiry_date.isoformat(),
                },
            )
    finally:
        db.close()
