from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from datetime import date

from app.core.database import SessionLocal
from app.subscriptions.models import Subscription
from app.auth.deps import get_current_user
from app.alerts.service import send_admin_alert
from pydantic import BaseModel

router = APIRouter(prefix="/subscriptions", tags=["Subscriptions"])

# =========================
# DB Dependency
# =========================
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


# =========================
# REQUEST SCHEMA
# =========================
class CreateSubscriptionRequest(BaseModel):
    name: str
    plan: str
    community: str
    floor: str
    flat: str
    address: str


# =========================
# CREATE SUBSCRIPTION
# =========================
@router.post("/", status_code=status.HTTP_201_CREATED)
def create_subscription(
    payload: CreateSubscriptionRequest,
    user=Depends(get_current_user),
    db: Session = Depends(get_db),
):
    # Prevent duplicate active subscription
    existing = (
        db.query(Subscription)
        .filter(
            Subscription.phone == user["sub"],
            Subscription.is_active == True
        )
        .first()
    )

    if existing:
        raise HTTPException(
            status_code=400,
            detail="Active subscription already exists"
        )

    sub = Subscription(
        phone=user["sub"],
        name=payload.name,
        plan=payload.plan,
        community=payload.community,
        floor=payload.floor,
        flat=payload.flat,
        address=payload.address,
        start_date=date.today(),
    )

    sub.set_expiry(months=1)

    db.add(sub)
    db.commit()
    db.refresh(sub)

    # 🔔 ALERT 1 — NEW SUBSCRIPTION
    send_admin_alert(
        "NEW_SUBSCRIPTION",
        {
            "Name": sub.name,
            "Plan": sub.plan,
            "Community": sub.community,
            "Phone": sub.phone,
            "Start Date": str(sub.start_date),
        },
    )

    return {
        "message": "Subscription created successfully",
        "subscription_id": sub.id,
    }


# =========================
# PAUSE SUBSCRIPTION
# =========================
@router.patch("/{sub_id}/pause")
def pause_subscription(
    sub_id: int,
    user=Depends(get_current_user),
    db: Session = Depends(get_db),
):
    sub = (
        db.query(Subscription)
        .filter(
            Subscription.id == sub_id,
            Subscription.phone == user["sub"]
        )
        .first()
    )

    if not sub:
        raise HTTPException(status_code=404, detail="Subscription not found")

    if sub.is_paused:
        raise HTTPException(status_code=400, detail="Subscription already paused")

    sub.is_paused = True
    db.commit()

    # 🔔 ALERT 4 — PAUSED
    send_admin_alert(
        "SUBSCRIPTION_PAUSED",
        {
            "Customer": sub.name,
            "Community": sub.community,
            "Effective From": "Tomorrow",
        },
    )

    return {"message": "Subscription paused successfully"}


# =========================
# RESUME SUBSCRIPTION
# =========================
@router.patch("/{sub_id}/resume")
def resume_subscription(
    sub_id: int,
    user=Depends(get_current_user),
    db: Session = Depends(get_db),
):
    sub = (
        db.query(Subscription)
        .filter(
            Subscription.id == sub_id,
            Subscription.phone == user["sub"]
        )
        .first()
    )

    if not sub:
        raise HTTPException(status_code=404, detail="Subscription not found")

    if not sub.is_paused:
        raise HTTPException(status_code=400, detail="Subscription is not paused")

    sub.is_paused = False
    db.commit()

    # 🔔 ALERT 5 — RESUMED
    send_admin_alert(
        "SUBSCRIPTION_RESUMED",
        {
            "Customer": sub.name,
            "Delivery Starts": "Tomorrow",
        },
    )

    return {"message": "Subscription resumed successfully"}
