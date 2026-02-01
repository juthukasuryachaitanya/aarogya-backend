from sqlalchemy import Column, Integer, String, Date, Float
from datetime import date
from app.core.database import Base

class Expense(Base):
    __tablename__ = "expenses"

    id = Column(Integer, primary_key=True)
    date = Column(Date, default=date.today)
    category = Column(String)
    notes = Column(String)
    amount = Column(Float)
