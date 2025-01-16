from sqlalchemy import Column, String, Integer, ForeignKey, Date
from datetime import datetime, date
import uuid

from models.base_model import Base


class CallPlan(Base):
    __tablename__ = "call_plan"

    call_plan_id = Column(String, primary_key=True, default=uuid.uuid4)
    restaurant_id = Column(String, ForeignKey("restaurant.restaurant_id"), nullable=False)
    user_id = Column(String, ForeignKey("user.user_id"), nullable=False)
    frequency_days = Column(Integer, nullable=False)  # Number of days between calls
    last_call_date = Column(Date, nullable=True)
    next_call_date = Column(Date, nullable=False)
    notes = Column(String, nullable=True)
    created_at = Column(String, nullable=False, default=datetime.now)
    updated_at = Column(String, nullable=False, default=datetime.now)

    def __repr__(self):
        return f"<CallPlan {self.call_plan_id}>"
