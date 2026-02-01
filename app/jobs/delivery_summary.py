from sqlalchemy.orm import Session
from app.core.database import SessionLocal
from app.subscriptions.models import Subscription
from app.alerts.service import send_admin_alert
from datetime import date

def daily_delivery_summary():
    db: Session = SessionLocal()

    try:
        total = db.query(Subscription).count()
        paused = db.query(Subscription).filter(
            Subscription.is_paused == True
        ).count()

        active = total - paused

        communities = db.query(
            Subscription.community
        ).distinct().count()

        send_admin_alert(
            "DAILY_DELIVERY_SUMMARY",
            {
                "Total Deliveries": total,
                "Active": active,
                "Paused": paused,
                "Communities": communities,
                "Date": str(date.today())
            }
        )
    finally:
        db.close()
