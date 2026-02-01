from sqlalchemy.orm import Session
from datetime import date, timedelta

from app.core.database import SessionLocal
from app.subscriptions.models import Subscription
from app.alerts.service import send_admin_alert

def subscription_expiry_reminders():
    db: Session = SessionLocal()

    try:
        today = date.today()

        targets = {
            "EXPIRY_3_DAYS": today + timedelta(days=3),
            "EXPIRY_1_DAY": today + timedelta(days=1),
            "EXPIRY_TODAY": today,
        }

        for alert_type, target_date in targets.items():
            subs = db.query(Subscription).filter(
                Subscription.expiry_date == target_date
            ).all()

            for sub in subs:
                send_admin_alert(
                    alert_type,
                    {
                        "Customer": sub.name,
                        "Plan": sub.plan,
                        "Ends On": str(sub.expiry_date),
                        "Phone": sub.phone
                    }
                )
    finally:
        db.close()
