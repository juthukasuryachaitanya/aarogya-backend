from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from datetime import date

from app.core.database import SessionLocal
from app.subscriptions.models import Subscription
from app.auth.deps import get_current_user
from app.alerts.service import send_admin_alert

router = APIRouter(prefix="/subscriptions", tags=["Subscriptions"])

# -------------------------
# DB Dependency
# -------------------------
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# -------------------------
# CREATE SUBSCRIPTION
# -------------------------
@router.post("/")
def create_subscription(
    data: dict,
    user=Depends(get_current_user),
    db: Session = Depends(get_db),
):
    sub = Subscription(
        phone=user["sub"],
        name=data.get("name"),
        plan=data.get("plan"),
        community=data.get("community"),
        floor=data.get("floor"),
        flat=data.get("flat"),
        address=data.get("address"),
        start_date=date.today(),
    )

    sub.set_expiry(months=1)
    db.add(sub)
    db.commit()
    db.refresh(sub)

    # 🔔 ALERT 1 — NEW SUBSCRIPTION
    send_admin_alert("NEW_SUBSCRIPTION", {
        "Name": sub.name,
        "Plan": sub.plan,
        "Community": sub.community,
        "Phone": sub.phone,
        "Start Date": sub.start_date,
    })

    return {"message": "Subscription created", "id": sub.id}

# -------------------------
# PAUSE SUBSCRIPTION
# -------------------------
@router.patch("/{sub_id}/pause")
def pause_subscription(
    sub_id: int,
    db: Session = Depends(get_db),
    user=Depends(get_current_user),
):
    sub = db.query(Subscription).filter_by(id=sub_id).first()
    if not sub:
        raise HTTPException(404, "Subscription not found")

    sub.is_paused = True
    db.commit()

    # 🔔 ALERT 4 — PAUSED
    send_admin_alert("SUBSCRIPTION_PAUSED", {
        "Customer": sub.name,
        "Community": sub.community,
        "Effective From": "Tomorrow",
    })

    return {"message": "Subscription paused"}

# -------------------------
# RESUME SUBSCRIPTION
# -------------------------
@router.patch("/{sub_id}/resume")
def resume_subscription(
    sub_id: int,
    db: Session = Depends(get_db),
    user=Depends(get_current_user),
):
    sub = db.query(Subscription).filter_by(id=sub_id).first()
    if not sub:
        raise HTTPException(404, "Subscription not found")

    sub.is_paused = False
    db.commit()

    # 🔔 ALERT 5 — RESUMED
    send_admin_alert("SUBSCRIPTION_RESUMED", {
        "Customer": sub.name,
        "Delivery Starts": "Tomorrow",
    })

    return {"message": "Subscription resumed"}
