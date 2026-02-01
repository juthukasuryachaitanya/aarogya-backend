from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from datetime import date
from app.auth.deps import admin_only
from app.core.database import SessionLocal
from app.subscriptions.models import Subscription

router = APIRouter(prefix="/admin/deliveries", tags=["Admin"])

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.get("/")
def today_deliveries(
    db: Session = Depends(get_db),
    admin=Depends(admin_only),
):
    subs = db.query(Subscription).filter(
        Subscription.is_paused == False
    ).all()

    return {
        "total": len(subs),
        "deliveries": [
            {
                "name": s.name,
                "phone": s.phone,
                "community": s.community,
                "floor": s.floor,
                "flat": s.flat,
                "plan": s.plan,
            }
            for s in subs
        ]
    }
