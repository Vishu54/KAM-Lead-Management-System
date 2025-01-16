import uuid
from sqlalchemy import Column, String, Enum, ForeignKey, Integer
from enum import Enum as PyEnum
from models.base_model import Base


class OrderStatus(PyEnum):
    NEW = "New"
    CONFIRMED = "Confirmed"
    PREPARING = "Preparing"
    READY = "Ready"
    DELIVERED = "Delivered"
    CANCELED = "Canceled"


class Order(Base):
    __tablename__ = "order"

    order_id = Column(String, primary_key=True, default=uuid.uuid4)
    restaurant_id = Column(String, ForeignKey("restaurant.restaurant_id"), nullable=False)
    user_id = Column(String, ForeignKey("user.user_id"), nullable=False)
    interaction_id = Column(String, ForeignKey("interaction.interaction_id"), nullable=False)
    status = Column(Enum(OrderStatus), default=OrderStatus.NEW)
    amount = Column(Integer, nullable=False)
    created_at = Column(String, nullable=False)
    updated_at = Column(String, nullable=False)

    def __repr__(self):
        return f"<Order {self.order_id}>"
