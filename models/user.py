from sqlalchemy import Column, ForeignKey, String, Enum
from datetime import datetime
import uuid
from enum import Enum as PyEnum

from models.base_model import Base


class UserRole(PyEnum):
    ADMIN = "Admin"
    MANAGER = "Manager"
    STAFF = "Staff"
    OWNER = "Owner"


class User(Base):
    __tablename__ = "user"

    user_id = Column(String, primary_key=True, default=uuid.uuid4)
    name = Column(String, nullable=False)
    email = Column(String, nullable=False)
    phone = Column(String, nullable=False)
    role = Column(Enum(UserRole), default=UserRole.STAFF)
    hashed_password = Column(String, nullable=False)
    restaurant_id = Column(String, ForeignKey("restaurant.restaurant_id"), nullable=False)
    created_at = Column(String, nullable=False, default=datetime.now)
    updated_at = Column(String, nullable=False, default=datetime.now)

    def __repr__(self):
        return f"<Contact {self.name}>"
