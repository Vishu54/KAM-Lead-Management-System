import logging
from typing import Optional, List
from datetime import datetime

from models.interaction import Interaction
from repository.interaction import InteractionRepository
from core.custom_exception import handle_exception

logger = logging.getLogger(__name__)


class InteractionService:
    def __init__(self, repository: InteractionRepository):
        self.repository = repository

    async def create_interaction(self, interaction_data) -> Interaction:
        try:
            interaction_date = datetime.now().isoformat()
            return await self.repository.create(**interaction_data, interaction_date=interaction_date)
        except Exception as e:
            logger.error(f"Error in create_interaction service: {str(e)}")
            handle_exception(message="Failed to create interaction")

    async def get_all_interactions(self) -> List[Interaction]:
        try:
            return await self.repository.get_all()
        except Exception as e:
            logger.error(f"Error in get_all_interactions service: {str(e)}")
            handle_exception(message="Failed to fetch interactions")

    async def get_interaction_by_id(self, interaction_id: str) -> Optional[Interaction]:
        try:
            return await self.repository.get_by_id(interaction_id)
        except Exception as e:
            logger.error(f"Error in get_interaction_by_id service: {str(e)}")
            handle_exception(message="Failed to fetch interaction")

    async def get_interactions_by_restaurant(self, restaurant_id: str) -> List[Interaction]:
        try:
            return await self.repository.get_by_restaurant(restaurant_id)
        except Exception as e:
            logger.error(f"Error in get_interactions_by_restaurant service: {str(e)}")
            handle_exception(message="Failed to fetch interactions")

    async def get_interactions_by_contact(self, user_id: str) -> List[Interaction]:
        try:
            return await self.repository.get_by_contact(user_id)

        except Exception as e:
            logger.error(f"Error in get_interactions_by_contact service: {str(e)}")
            handle_exception(message="Failed to fetch interactions")

    async def update_interaction(self, interaction_id: str, interaction_data: dict) -> Optional[Interaction]:
        try:
            return await self.repository.update(interaction_id, interaction_data)
        except Exception as e:
            logger.error(f"Error in update_interaction service: {str(e)}")
            handle_exception(message="Failed to update interaction")

    async def delete_interaction(self, interaction_id: str) -> bool:
        try:
            return await self.repository.delete(interaction_id)
        except Exception as e:
            logger.error(f"Error in delete_interaction service: {str(e)}")
            handle_exception(message="Failed to delete interaction")
