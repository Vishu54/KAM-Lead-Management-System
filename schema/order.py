from pydantic import BaseModel, Field
from typing import Optional
from datetime import datetime
from models.order import OrderStatus
import uuid


class OrderCreate(BaseModel):
    restaurant_id: str = Field(..., description="ID of the restaurant placing the order")
    user_id: str = Field(..., description="ID of the contact placing the order")
    amount: int = Field(..., gt=0, description="Order amount in cents")
    notes: Optional[str] = Field(None, description="Optional notes for the order")


class OrderResponse(BaseModel):
    order_id: uuid.UUID = Field(..., description="Unique identifier for the order")
    restaurant_id: uuid.UUID = Field(..., description="ID of the restaurant that placed the order")
    user_id: uuid.UUID = Field(..., description="ID of the contact that placed the order")
    interaction_id: uuid.UUID = Field(..., description="ID of the interaction associated with this order")
    status: OrderStatus = Field(..., description="Current status of the order")
    amount: int = Field(..., description="Order amount in cents")
    created_at: datetime = Field(..., description="Timestamp when the order was created")
    updated_at: datetime = Field(..., description="Timestamp when the order was last updated")
    notes: Optional[str] = Field(None, description="Optional notes about the order")

    class Config:
        from_attributes = True


class OrderListResponse(BaseModel):
    total: int
    orders: list[OrderResponse]
