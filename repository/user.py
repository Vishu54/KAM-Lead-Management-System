import logging
from typing import Optional, List

from models.user import User
from core.custom_exception import handle_exception
from core.database import managed_transaction, DbConnector
from repository.base_repository import BaseRepository

logger = logging.getLogger(__name__)


class UserRepository(BaseRepository):
    @managed_transaction
    async def create(self, name: str, email: str, phone: str, role: str, restaurant_id: str, password: str, db: Optional[DbConnector] = None) -> User:
        try:
            contact = User(name=name, email=email, phone=phone, role=role, restaurant_id=restaurant_id, hashed_password=password)
            db.Session.add(contact)
            return contact
        except Exception as e:
            logger.error(f"Error creating contact: {str(e)}")
            handle_exception(message="Failed to create contact")

    @managed_transaction
    async def get_all(self, db: Optional[DbConnector] = None) -> List[User]:
        try:
            query = db.Session.query(User).all()
            return query
        except Exception as e:
            logger.error(f"Error fetching all contacts: {str(e)}")
            handle_exception(message="Failed to fetch contacts")

    @managed_transaction
    async def get_by_id(self, user_id: str, db: Optional[DbConnector] = None) -> Optional[User]:
        try:
            query = db.Session.query(User).filter(User.user_id == user_id).first()
            return query
        except Exception as e:
            logger.error(f"Error fetching contact by id: {str(e)}")
            handle_exception(message="Failed to fetch contact")

    @managed_transaction
    async def get_by_email(self, email: str, db: Optional[DbConnector] = None) -> Optional[User]:
        try:
            query = db.Session.query(User).filter(User.email == email).first()
            return query
        except Exception as e:
            logger.error(f"Error fetching contact by email: {str(e)}")
            handle_exception(message="Failed to fetch contact")

    @managed_transaction
    async def get_by_restaurant(self, restaurant_id: str, db: Optional[DbConnector] = None) -> List[User]:
        try:
            query = db.Session.query(User).filter(User.restaurant_id == restaurant_id).all()
            return query
        except Exception as e:
            logger.error(f"Error fetching contacts by restaurant: {str(e)}")
            handle_exception(message="Failed to fetch contacts")

    @managed_transaction
    async def update(self, user_id: str, contact_data: dict, db: Optional[DbConnector] = None) -> Optional[User]:
        try:
            if contact_data:
                db.Session.query(User).filter(User.user_id == user_id).update(contact_data)
                return await self.get_by_id(user_id, db=db)
            return None
        except Exception as e:
            logger.error(f"Error updating contact: {str(e)}")
            handle_exception(message="Failed to update contact")

    @managed_transaction
    async def delete(self, user_id: str, db: Optional[DbConnector] = None) -> bool:
        try:
            contact = await self.get_by_id(user_id, db=db)
            if contact:
                db.Session.delete(contact)
                return True
            return False
        except Exception as e:
            logger.error(f"Error deleting contact: {str(e)}")
            handle_exception(message="Failed to delete contact")
