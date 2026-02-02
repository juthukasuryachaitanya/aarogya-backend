from datetime import date
from sqlalchemy.orm import Session
from app.core.database import SessionLocal
from app.subscriptions.models import Subscription
from app.alerts.service import send_admin_alert

def daily_delivery_summary():
    db: Session = SessionLocal()
    try:
        count = (
            db.query(Subscription)
            .filter(Subscription.is_paused == False)
            .count()
        )

        send_admin_alert(
            "DAILY_SUMMARY",
            {
                "date": date.today().isoformat(),
                "count": count,
            },
        )
    finally:
        db.close()
