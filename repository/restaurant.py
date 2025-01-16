import logging
from typing import Optional, List

from models.restaurant import Restaurant, RestaurantStatus
from core.custom_exception import handle_exception
from core.database import managed_transaction, DbConnector
from repository.base_repository import BaseRepository

logger = logging.getLogger(__name__)


class RestaurantRepository(BaseRepository):

    @managed_transaction
    async def create(self, name: str, address: str, phone: str, email: str, db: Optional[DbConnector] = None) -> Restaurant:
        try:
            restaurant = Restaurant(name=name, address=address, phone=phone, email=email)
            db.Session.add(restaurant)
            return restaurant
        except Exception as e:
            logger.error(f"Error creating restaurant: {str(e)}")
            handle_exception(message="Failed to create restaurant")

    @managed_transaction
    async def get_all(self, db: Optional[DbConnector] = None) -> List[Restaurant]:
        try:
            query = db.Session.query(Restaurant).all()
            return query
        except Exception as e:
            logger.error(f"Error fetching all restaurants: {str(e)}")
            handle_exception(message="Failed to fetch restaurants")

    @managed_transaction
    async def get_by_id(self, restaurant_id: str, db: Optional[DbConnector] = None) -> Optional[Restaurant]:
        try:
            query = db.Session.query(Restaurant).filter(Restaurant.restaurant_id == restaurant_id).first()
            return query
        except Exception as e:
            logger.error(f"Error fetching restaurant by id: {str(e)}")
            handle_exception(message="Failed to fetch restaurant")

    @managed_transaction
    async def get_by_owner(self, owner_id: str, db: Optional[DbConnector] = None) -> List[Restaurant]:
        try:
            query = db.Session.query(Restaurant).filter(Restaurant.owner_id == owner_id).all()
            return query
        except Exception as e:
            logger.error(f"Error fetching restaurants by owner: {str(e)}")
            handle_exception(message="Failed to fetch restaurants")

    @managed_transaction
    async def update_status(self, restaurant_id: str, status: RestaurantStatus, db: Optional[DbConnector] = None) -> Optional[Restaurant]:
        try:
            restaurant = await self.get_by_id(restaurant_id, db=db)
            if restaurant:
                restaurant.status = status
                return restaurant
            return None
        except Exception as e:
            logger.error(f"Error updating restaurant status: {str(e)}")
            handle_exception(message="Failed to update restaurant status")

    @managed_transaction
    async def update(self, restaurant_id: str, restaurant_update: dict, db: Optional[DbConnector] = None) -> Optional[Restaurant]:
        try:
            if restaurant_update:
                db.Session.query(Restaurant).filter(Restaurant.restaurant_id == restaurant_id).update(restaurant_update)
                return await self.get_by_id(restaurant_id, db=db)
            return None
        except Exception as e:
            logger.error(f"Error updating restaurant: {str(e)}")
            handle_exception(message="Failed to update restaurant")

    @managed_transaction
    async def delete(self, restaurant_id: str, db: Optional[DbConnector] = None) -> bool:
        try:
            restaurant = await self.get_by_id(restaurant_id, db=db)
            if restaurant:
                db.Session.delete(restaurant)
                return True
            return False
        except Exception as e:
            logger.error(f"Error deleting restaurant: {str(e)}")
            handle_exception(message="Failed to delete restaurant")
