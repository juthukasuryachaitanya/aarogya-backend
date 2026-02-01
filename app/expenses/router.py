from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.core.database import SessionLocal
from app.expenses.models import Expense
from app.auth.deps import admin_only
from app.core.logger import logger

router = APIRouter(prefix="/admin/expenses", tags=["Admin Expenses"])

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
# ADD EXPENSE
# -------------------------
@router.post("/")
def add_expense(
    data: dict,
    db: Session = Depends(get_db),
    admin=Depends(admin_only),
):
    exp = Expense(
        category=data["category"],
        notes=data.get("notes"),
        amount=data["amount"],
    )
    db.add(exp)
    db.commit()
    db.refresh(exp)

    # 🧾 LOG — EXPENSE ADDED
    logger.info(
        f"Expense added | amount={exp.amount} | category={exp.category}"
    )

    return {"message": "Expense added successfully"}

# -------------------------
# LIST EXPENSES
# -------------------------
@router.get("/")
def list_expenses(
    db: Session = Depends(get_db),
    admin=Depends(admin_only),
):
    expenses = db.query(Expense).all()

    # 🧾 LOG — EXPENSES VIEWED
    logger.info("Admin viewed expenses list")

    return expenses
