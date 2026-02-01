from sqlalchemy import Column, Integer, String, Date, Boolean
from app.core.database import Base
from datetime import date, timedelta

class Subscription(Base):
    __tablename__ = "subscriptions"

    id = Column(Integer, primary_key=True, index=True)

    phone = Column(String, index=True)           # customer identifier
    name = Column(String)
    plan = Column(String)

    community = Column(String)
    floor = Column(String)
    flat = Column(String)
    address = Column(String)

    start_date = Column(Date, default=date.today)
    end_date = Column(Date)

    is_active = Column(Boolean, default=True)
    is_paused = Column(Boolean, default=False)

    def set_expiry(self, months: int = 1):
        self.end_date = self.start_date + timedelta(days=30 * months)
