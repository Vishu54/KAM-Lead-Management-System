from pydantic import BaseModel, Field
from typing import List, Optional
from datetime import date, datetime
import uuid


class CallPlanBase(BaseModel):
    """Base schema for call plan data"""

    restaurant_id: str = Field(..., description="ID of the restaurant to be called")
    user_id: str = Field(..., description="ID of the contact to be called")
    frequency_days: int = Field(..., description="Number of days between calls", ge=1, le=365)
    notes: Optional[str] = Field(None, description="Optional notes about the call plan")


class CallPlanCreate(CallPlanBase):
    """Schema for creating a new call plan"""

    pass


class CallPlanResponse(CallPlanBase):
    """Schema for call plan response"""

    call_plan_id: uuid.UUID = Field(..., description="Unique identifier for the call plan")
    last_call_date: Optional[date] = Field(None, description="Date of the last call made")
    next_call_date: date = Field(..., description="Date of the next scheduled call")
    created_at: datetime = Field(..., description="Timestamp when the call plan was created")
    updated_at: datetime = Field(..., description="Timestamp when the call plan was last updated")

    class Config:
        from_attributes = True


class CallPlanListResponse(BaseModel):
    """Schema for list of call plans response"""

    total: int = Field(..., description="Total number of call plans")
    call_plans: List[CallPlanResponse] = Field(..., description="List of call plans")
