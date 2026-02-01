from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.auth.deps import admin_only
from app.core.database import SessionLocal
from app.subscriptions.models import Subscription

router = APIRouter(prefix="/admin/customers", tags=["Admin"])

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.get("/")
def list_customers(
    db: Session = Depends(get_db),
    admin=Depends(admin_only),
):
    subs = db.query(Subscription).all()

    return [
        {
            "name": s.name,
            "phone": s.phone,
            "plan": s.plan,
            "community": s.community,
            "floor": s.floor,
            "flat": s.flat,
            "address": s.address,
            "active": s.is_active,
            "paused": s.is_paused,
        }
        for s in subs
    ]
