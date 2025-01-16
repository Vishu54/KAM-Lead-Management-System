import uuid
from sqlalchemy import Column, String, Enum, ForeignKey
from enum import Enum as PyEnum

from models.base_model import Base


class InteractionType(PyEnum):
    EMAIL = "Email"
    CALL = "Call"
    MEETING = "Meeting"
    ORDER = "Order"
    OTHER = "Other"


class Interaction(Base):
    __tablename__ = "interaction"

    interaction_id = Column(String, primary_key=True, default=uuid.uuid4)
    user_id = Column(String, ForeignKey("user.user_id"), nullable=False, index=True)
    restaurant_id = Column(String, ForeignKey("restaurant.restaurant_id"), nullable=False, index=True)
    interaction_type = Column(Enum(InteractionType, values_callable=lambda x: [e.value for e in x]), nullable=False)
    interaction_date = Column(String, nullable=False)
    notes = Column(String, nullable=True)

    def __repr__(self):
        return f"<Interaction {self.interaction_id}>"
