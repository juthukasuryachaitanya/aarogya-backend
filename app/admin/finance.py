from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.auth.deps import admin_only
from app.core.database import SessionLocal
from app.expenses.models import Expense
from app.subscriptions.models import Subscription

router = APIRouter(prefix="/admin/finance", tags=["Admin"])

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.get("/")
def finance_summary(
    db: Session = Depends(get_db),
    admin=Depends(admin_only),
):
    total_expense = sum(e.amount for e in db.query(Expense).all())
    active_subs = db.query(Subscription).filter(
        Subscription.is_paused == False
    ).count()

    revenue_estimate = active_subs * 2000  # avg estimate

    return {
        "active_subscriptions": active_subs,
        "estimated_revenue": revenue_estimate,
        "total_expenses": total_expense,
        "profit_estimate": revenue_estimate - total_expense,
    }
