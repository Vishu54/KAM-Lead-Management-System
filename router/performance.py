from fastapi import APIRouter, Depends, Query
from datetime import date
from typing import Optional

from fastapi.security import OAuth2PasswordBearer

from services.performance import PerformanceService
from repository.performance import PerformanceRepository
from schema.performance import PerformanceMetricResponse, PerformanceMetricListResponse

router = APIRouter(prefix="/performance", tags=["performance"])

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/v1/auth/login")


def get_performance_service() -> PerformanceService:
    repository = PerformanceRepository()
    return PerformanceService(repository)


@router.post("/restaurants/{restaurant_id}/metrics")
async def generate_metrics(
    restaurant_id: str,
    year: int = Query(..., description="Year to generate metrics for"),
    month: int = Query(..., description="Month to generate metrics for (1-12)"),
    service: PerformanceService = Depends(get_performance_service),
    token: str = Depends(oauth2_scheme),
):
    """Generate performance metrics for a restaurant for a specific month"""
    return await service.generate_monthly_metrics(restaurant_id, year, month)


@router.get("/restaurants/{restaurant_id}/metrics")
async def get_restaurant_metrics(restaurant_id: str, service: PerformanceService = Depends(get_performance_service), token: str = Depends(oauth2_scheme)):
    """Get all performance metrics for a restaurant"""
    metrics = await service.get_restaurant_performance(restaurant_id)
    return PerformanceMetricListResponse(total=len(metrics), metrics=metrics)


@router.get("/restaurants/{restaurant_id}/trends")
async def get_restaurant_trends(
    restaurant_id: str,
    months: int = Query(default=3, ge=1, le=12, description="Number of months to analyze"),
    service: PerformanceService = Depends(get_performance_service),
    token: str = Depends(oauth2_scheme),
):
    """Get performance trends for a restaurant"""
    return await service.analyze_restaurant_trends(restaurant_id, months)


@router.get("/restaurants/rankings")
async def get_restaurant_rankings(
    metric: str = Query(default="total_orders", enum=["total_orders", "total_amount", "average_order_value", "order_frequency"], description="Metric to rank by"),
    limit: int = Query(default=10, ge=1, le=100, description="Number of restaurants to return"),
    service: PerformanceService = Depends(get_performance_service),
    token: str = Depends(oauth2_scheme),
):
    """Get top performing restaurants by specified metric"""
    return await service.get_restaurant_rankings(metric, limit)
