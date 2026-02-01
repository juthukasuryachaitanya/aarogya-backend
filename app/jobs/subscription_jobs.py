from datetime import date, timedelta
from app.subscriptions.models import Subscription

def check_expiring_subscriptions(db):
    target = date.today() + timedelta(days=3)
    expiring = db.query(Subscription).filter(
        Subscription.end_date == target
    ).all()

    for sub in expiring:
        print(f"ALERT: Subscription expiring for {sub.name}")
