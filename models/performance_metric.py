from sqlalchemy import Column, String, Integer, Float, ForeignKey, Date
from datetime import datetime
import uuid

from models.base_model import Base


class PerformanceMetric(Base):
    __tablename__ = "performance_metric"

    metric_id = Column(String, primary_key=True, default=uuid.uuid4)
    restaurant_id = Column(String, ForeignKey("restaurant.restaurant_id"), nullable=False, index=True)
    period_start = Column(Date, nullable=False)
    period_end = Column(Date, nullable=False)
    total_orders = Column(Integer, default=0)
    total_amount = Column(Float, default=0.0)
    average_order_value = Column(Float, default=0.0)
    order_frequency = Column(Float, default=0.0)  # Average days between orders
    created_at = Column(String, nullable=False, default=datetime.now)
    updated_at = Column(String, nullable=False, default=datetime.now)

    def __repr__(self):
        return f"<PerformanceMetric {self.restaurant_id} {self.period_start}-{self.period_end}>"
