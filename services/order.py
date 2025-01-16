from datetime import datetime
from typing import List, Optional
from fastapi import HTTPException
import logging

from models.order import Order, OrderStatus
from repository.order import OrderRepository
from services.interaction import InteractionService
from models.interaction import InteractionType


logger = logging.getLogger(__name__)


class OrderService:
    def __init__(self, repository: OrderRepository, interaction_service: InteractionService):
        self.repository = repository
        self.interaction_service = interaction_service

    async def place_order(self, order_data: dict) -> Order:
        """Place a new order"""
        try:
            current_time = datetime.now().isoformat()

            # Create interaction record for the order
            interaction = await self.interaction_service.create_interaction(
                {
                    "restaurant_id": order_data["restaurant_id"],
                    "user_id": order_data["user_id"],
                    "interaction_type": InteractionType.ORDER.value,
                    "notes": order_data.get("notes"),
                }
            )

            # Create the order
            order = await self.repository.create(
                restaurant_id=order_data["restaurant_id"],
                user_id=order_data["user_id"],
                interaction_id=interaction.interaction_id,
                amount=order_data["amount"],
                created_at=current_time,
                updated_at=current_time,
            )
            return order

        except Exception as e:
            logger.error(f"Error in place_order service: {str(e)}")
            raise HTTPException(status_code=500, detail="Failed to place order")

    async def update_order_status(self, order_id: str, new_status: OrderStatus) -> Order:
        """Update the status of an order"""
        try:
            order = await self.repository.get_by_id(order_id)
            if not order:
                raise HTTPException(status_code=404, detail="Order not found")

            current_time = datetime.now().isoformat()
            updated_order = await self.repository.update(order_id, {"status": new_status, "updated_at": current_time})
            return updated_order

        except HTTPException:
            raise
        except Exception as e:
            logger.error(f"Error in update_order_status service: {str(e)}")
            raise HTTPException(status_code=500, detail="Failed to update order status")

    async def get_restaurant_orders(self, restaurant_id: str) -> List[Order]:
        """Get all orders for a restaurant"""
        try:
            return await self.repository.get_by_restaurant(restaurant_id)
        except Exception as e:
            logger.error(f"Error in get_restaurant_orders service: {str(e)}")
            raise HTTPException(status_code=500, detail="Failed to fetch restaurant orders")
