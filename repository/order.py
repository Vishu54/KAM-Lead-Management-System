import logging
from typing import Optional, List

from models.order import Order
from core.custom_exception import handle_exception
from core.database import managed_transaction, DbConnector
from repository.base_repository import BaseRepository

logger = logging.getLogger(__name__)


class OrderRepository(BaseRepository):
    @managed_transaction
    async def create(self, restaurant_id: str, user_id: str, interaction_id: str, amount: int, created_at: str, updated_at: str, db: Optional[DbConnector] = None) -> Order:
        try:
            order = Order(restaurant_id=restaurant_id, user_id=user_id, interaction_id=interaction_id, amount=amount, created_at=created_at, updated_at=updated_at)
            db.Session.add(order)
            return order
        except Exception as e:
            logger.error(f"Error creating order: {str(e)}")
            handle_exception(message="Failed to create order")

    @managed_transaction
    async def get_all(self, db: Optional[DbConnector] = None) -> List[Order]:
        try:
            query = db.Session.query(Order).all()
            return query
        except Exception as e:
            logger.error(f"Error fetching all orders: {str(e)}")
            handle_exception(message="Failed to fetch orders")

    @managed_transaction
    async def get_by_id(self, order_id: str, db: Optional[DbConnector] = None) -> Optional[Order]:
        try:
            query = db.Session.query(Order).filter(Order.order_id == order_id).first()
            return query
        except Exception as e:
            logger.error(f"Error fetching order by id: {str(e)}")
            handle_exception(message="Failed to fetch order")

    @managed_transaction
    async def get_by_restaurant(self, restaurant_id: str, db: Optional[DbConnector] = None) -> List[Order]:
        try:
            query = db.Session.query(Order).filter(Order.restaurant_id == restaurant_id).all()
            return query
        except Exception as e:
            logger.error(f"Error fetching orders by restaurant: {str(e)}")
            handle_exception(message="Failed to fetch orders")

    @managed_transaction
    async def get_by_contact(self, user_id: str, db: Optional[DbConnector] = None) -> List[Order]:
        try:
            query = db.Session.query(Order).filter(Order.user_id == user_id).all()
            return query
        except Exception as e:
            logger.error(f"Error fetching orders by contact: {str(e)}")
            handle_exception(message="Failed to fetch orders")

    @managed_transaction
    async def update(self, order_id: str, order_data: dict, db: Optional[DbConnector] = None) -> Optional[Order]:
        try:
            if order_data:
                db.Session.query(Order).filter(Order.order_id == order_id).update(order_data)
                return await self.get_by_id(order_id, db=db)
            return None
        except Exception as e:
            logger.error(f"Error updating order: {str(e)}")
            handle_exception(message="Failed to update order")

    @managed_transaction
    async def delete(self, order_id: str, db: Optional[DbConnector] = None) -> bool:
        try:
            order = await self.get_by_id(order_id, db=db)
            if order:
                db.Session.delete(order)
                return True
            return False
        except Exception as e:
            logger.error(f"Error deleting order: {str(e)}")
            handle_exception(message="Failed to delete order")
