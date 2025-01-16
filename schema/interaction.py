from typing import Optional
from pydantic import BaseModel, Field
import uuid

from models.interaction import InteractionType


class InteractionBase(BaseModel):
    user_id: str = Field(..., description="ID of the contact associated with this interaction")
    restaurant_id: str = Field(..., description="ID of the restaurant associated with this interaction")
    interaction_type: InteractionType = Field(default=InteractionType, description="Type of interaction")
    notes: Optional[str] = Field(None, description="Optional notes about the interaction")


class InteractionCreate(InteractionBase):
    pass


class InteractionResponse(InteractionBase):
    interaction_id: uuid.UUID = Field(..., description="Unique identifier for the interaction", default_factory=uuid.uuid4)
    interaction_date: str = Field(..., description="Date and time of the interaction")

    class Config:
        from_attributes = True


class InteractionListResponse(BaseModel):
    total: int = Field(..., description="Total number of interactions")
    interactions: list[InteractionResponse] = Field(..., description="List of interactions")
