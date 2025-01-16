from pydantic import BaseModel, Field
from typing import Optional, List
from datetime import datetime
import uuid


class RestaurantBase(BaseModel):
    name: str = Field(..., min_length=1, max_length=100)
    address: str = Field(..., min_length=5, max_length=200)
    email: str = Field(..., min_length=5, max_length=100)
    phone: str = Field(..., pattern=r"^\+?1?\d{9,15}$")


class RestaurantCreate(RestaurantBase):
    pass


class RestaurantUpdate(BaseModel):
    name: Optional[str] = Field(None, min_length=1, max_length=100)
    address: Optional[str] = Field(None, min_length=5, max_length=200)
    phone: Optional[str] = Field(None, pattern=r"^\+?1?\d{9,15}$")
    email: str = Field(..., min_length=5, max_length=100)
    status: Optional[str] = Field(None)


class RestaurantInDB(RestaurantBase):
    restaurant_id: uuid.UUID = Field(default_factory=uuid.uuid4)
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True


class RestaurantResponse(RestaurantInDB):
    pass


class RestaurantListResponse(BaseModel):
    total: int
    restaurants: List[RestaurantResponse]
