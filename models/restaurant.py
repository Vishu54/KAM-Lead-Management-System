from sqlalchemy import Column, ForeignKey, String, Enum
from datetime import datetime
import uuid
from enum import Enum as PyEnum

from models.base_model import Base


class RestaurantStatus(PyEnum):
    NEW = "New"
    CONTACTED = "Contacted"
    IN_PROGRESS = "In Progress"
    CONVERTED = "Converted"
    CLOSED = "Closed"


class Restaurant(Base):
    __tablename__ = "restaurant"

    restaurant_id = Column(String, primary_key=True, default=uuid.uuid4)
    name = Column(String, nullable=False)
    address = Column(String, nullable=False)
    phone = Column(String, nullable=False)
    email = Column(String, nullable=False)
    status = Column(Enum(RestaurantStatus), default=RestaurantStatus.NEW)
    created_at = Column(String, nullable=False, default=datetime.now)
    updated_at = Column(String, nullable=False, default=datetime.now)

    def __repr__(self):
        return f"<Restaurant {self.name}>"
