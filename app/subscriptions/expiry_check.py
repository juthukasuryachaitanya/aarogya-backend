from datetime import date, timedelta
from sqlalchemy.orm import Session
from app.subscriptions.models import Subscription
from app.alerts.service import send_admin_alert

def check_expiring_subscriptions(db: Session):
    today = date.today()

    targets = [
        today + timedelta(days=3),
        today + timedelta(days=1),
        today,
    ]

    subs = db.query(Subscription).filter(
        Subscription.end_date.in_(targets)
    ).all()

    for sub in subs:
        send_admin_alert("SUBSCRIPTION_EXPIRY", {
            "Customer": sub.name,
            "Plan": sub.plan,
            "Ends On": sub.end_date,
        })
