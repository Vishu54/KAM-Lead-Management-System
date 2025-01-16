from typing import List, Optional
from models.restaurant import Restaurant
from repository.restaurant import RestaurantRepository


class RestaurantService:
    def __init__(self, restaurant_repository: RestaurantRepository):
        self.restaurant_repository = restaurant_repository

    async def create_restaurant(self, restaurant_data: dict) -> Restaurant:
        """Create a new restaurant."""
        return await self.restaurant_repository.create(**restaurant_data)

    async def get_restaurant_by_id(self, restaurant_id: int) -> Optional[Restaurant]:
        """Get a restaurant by its ID."""
        return await self.restaurant_repository.get_by_id(restaurant_id)

    async def get_all_restaurants(self) -> List[Restaurant]:
        """Get all restaurants."""
        return await self.restaurant_repository.get_all()

    async def update_restaurant(self, restaurant_id: int, restaurant_data: dict) -> Optional[Restaurant]:
        """Update a restaurant by its ID."""
        return await self.restaurant_repository.update(restaurant_id, restaurant_data)

    async def update_restaurant_status(self, restaurant_id: int, status: str) -> Optional[Restaurant]:
        """Update a restaurant status by its ID."""
        return await self.restaurant_repository.update_status(restaurant_id, status)

    async def delete_restaurant(self, restaurant_id: int) -> bool:
        """Delete a restaurant by its ID."""
        return await self.restaurant_repository.delete(restaurant_id)
