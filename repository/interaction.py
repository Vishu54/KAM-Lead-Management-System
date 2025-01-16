import logging
from typing import Optional, List

from models.interaction import Interaction, InteractionType
from core.custom_exception import handle_exception
from core.database import managed_transaction, DbConnector
from repository.base_repository import BaseRepository

logger = logging.getLogger(__name__)


class InteractionRepository(BaseRepository):
    @managed_transaction
    async def create(
        self, user_id: str, restaurant_id: str, interaction_type: InteractionType, interaction_date: str, notes: Optional[str] = None, db: Optional[DbConnector] = None
    ) -> Interaction:
        try:
            interaction = Interaction(user_id=user_id, restaurant_id=restaurant_id, interaction_type=interaction_type, interaction_date=interaction_date, notes=notes)
            db.Session.add(interaction)
            return interaction
        except Exception as e:
            logger.error(f"Error creating interaction: {str(e)}")
            handle_exception(message="Failed to create interaction")

    @managed_transaction
    async def get_all(self, db: Optional[DbConnector] = None) -> List[Interaction]:
        try:
            query = db.Session.query(Interaction).all()
            return query
        except Exception as e:
            logger.error(f"Error fetching all interactions: {str(e)}")
            handle_exception(message="Failed to fetch interactions")

    @managed_transaction
    async def get_by_id(self, interaction_id: str, db: Optional[DbConnector] = None) -> Optional[Interaction]:
        try:
            query = db.Session.query(Interaction).filter(Interaction.interaction_id == interaction_id).first()
            return query
        except Exception as e:
            logger.error(f"Error fetching interaction by id: {str(e)}")
            handle_exception(message="Failed to fetch interaction")

    @managed_transaction
    async def get_by_restaurant(self, restaurant_id: str, db: Optional[DbConnector] = None) -> List[Interaction]:
        try:
            query = db.Session.query(Interaction).filter(Interaction.restaurant_id == restaurant_id).all()
            return query
        except Exception as e:
            logger.error(f"Error fetching interactions by restaurant: {str(e)}")
            handle_exception(message="Failed to fetch interactions")

    @managed_transaction
    async def get_by_contact(self, user_id: str, db: Optional[DbConnector] = None) -> List[Interaction]:
        try:
            query = db.Session.query(Interaction).filter(Interaction.user_id == user_id).all()
            return query
        except Exception as e:
            logger.error(f"Error fetching interactions by contact: {str(e)}")
            handle_exception(message="Failed to fetch interactions")

    @managed_transaction
    async def update(self, interaction_id: str, interaction_data: dict, db: Optional[DbConnector] = None) -> Optional[Interaction]:
        try:
            if interaction_data:
                db.Session.query(Interaction).filter(Interaction.interaction_id == interaction_id).update(interaction_data)
                return await self.get_by_id(interaction_id, db=db)
            return None
        except Exception as e:
            logger.error(f"Error updating interaction: {str(e)}")
            handle_exception(message="Failed to update interaction")

    @managed_transaction
    async def delete(self, interaction_id: str, db: Optional[DbConnector] = None) -> bool:
        try:
            interaction = await self.get_by_id(interaction_id, db=db)
            if interaction:
                db.Session.delete(interaction)
                return True
            return False
        except Exception as e:
            logger.error(f"Error deleting interaction: {str(e)}")
            handle_exception(message="Failed to delete interaction")
