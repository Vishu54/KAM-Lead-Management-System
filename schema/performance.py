from pydantic import BaseModel, Field
from typing import List
from datetime import date
import uuid


class PerformanceMetricBase(BaseModel):
    """Base schema for performance metric data"""

    restaurant_id: str = Field(..., description="ID of the restaurant being measured")
    period_start: date = Field(..., description="Start date of the measurement period")
    period_end: date = Field(..., description="End date of the measurement period")
    total_orders: int = Field(..., description="Total number of orders in the period")
    total_amount: float = Field(..., description="Total monetary value of orders in the period")
    average_order_value: float = Field(..., description="Average value per order")
    order_frequency: float = Field(..., description="Average days between orders")


class PerformanceMetricResponse(PerformanceMetricBase):
    """Schema for performance metric response"""

    metric_id: uuid.UUID = Field(..., description="Unique identifier for the performance metric")
    created_at: str = Field(..., description="Timestamp when the metric was created")
    updated_at: str = Field(..., description="Timestamp when the metric was last updated")

    class Config:
        from_attributes = True


class PerformanceMetricListResponse(BaseModel):
    """Schema for list of performance metrics"""

    total: int = Field(..., description="Total number of metrics")
    metrics: List[PerformanceMetricResponse] = Field(..., description="List of performance metrics")
