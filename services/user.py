import logging
from typing import Optional, List, Dict

from models.user import User
from repository.user import UserRepository
from security.auth_controller import AuthController
from passlib.context import CryptContext


logger = logging.getLogger(__name__)


class UserService:
    def __init__(self, repository: UserRepository):
        self.repository = repository

    async def create_user(self, user_data: Dict) -> User:
        """Create a new user"""
        try:
            return await self.repository.create(**user_data)
        except Exception as e:
            logger.error(f"Error in create_user service: {str(e)}")
            raise

    async def get_user_by_id(self, user_id: str) -> Optional[User]:
        """Get a user by ID"""
        try:
            return await self.repository.get_by_id(user_id)
        except Exception as e:
            logger.error(f"Error in get_user_by_id service: {str(e)}")
            raise

    async def get_all_users(self) -> List[User]:
        """Get all users"""
        try:
            return await self.repository.get_all()
        except Exception as e:
            logger.error(f"Error in get_all_users service: {str(e)}")
            raise

    async def get_users_by_restaurant(self, restaurant_id: str) -> List[User]:
        """Get all users by restaurant"""
        try:
            return await self.repository.get_by_restaurant(restaurant_id)
        except Exception as e:
            logger.error(f"Error in get_users_by_restaurant service: {str(e)}")
            raise

    async def update_user(self, user_id: str, user_data: Dict) -> Optional[User]:
        """Update a user"""
        try:
            return await self.repository.update(user_id, user_data)
        except Exception as e:
            logger.error(f"Error in update_user service: {str(e)}")
            raise

    async def delete_user(self, user_id: str) -> bool:
        """Delete a user"""
        try:
            return await self.repository.delete(user_id)
        except Exception as e:
            logger.error(f"Error in delete_user service: {str(e)}")
            raise
