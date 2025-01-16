from datetime import date, timedelta
from typing import List, Dict
from fastapi import HTTPException
from collections import defaultdict

from repository.performance import PerformanceRepository
from models.performance_metric import PerformanceMetric


class PerformanceService:
    def __init__(self, repository: PerformanceRepository):
        self.repository = repository

    async def generate_monthly_metrics(self, restaurant_id: str, year: int, month: int) -> PerformanceMetric:
        """Generate performance metrics for a specific month"""
        try:
            start_date = date(year, month, 1)
            if month == 12:
                end_date = date(year + 1, 1, 1) - timedelta(days=1)
            else:
                end_date = date(year, month + 1, 1) - timedelta(days=1)

            return await self.repository.calculate_metrics(restaurant_id, start_date, end_date)
        except Exception as e:
            raise HTTPException(status_code=500, detail=f"Failed to generate metrics: {str(e)}")

    async def get_restaurant_performance(self, restaurant_id: str) -> List[PerformanceMetric]:
        """Get all performance metrics for a restaurant"""
        try:
            return await self.repository.get_restaurant_metrics(restaurant_id)
        except Exception as e:
            raise HTTPException(status_code=500, detail=f"Failed to fetch metrics: {str(e)}")

    async def analyze_restaurant_trends(self, restaurant_id: str, months: int) -> Dict:
        """Analyze performance trends for a restaurant"""
        try:
            end_date = date.today()
            start_date = end_date - timedelta(days=months * 30)

            metrics = await self.repository.get_metrics_by_period(restaurant_id, start_date, end_date)
            if not metrics:
                raise HTTPException(status_code=404, detail="No metrics found for this period")

            # Ensure metrics are sorted by period_start for correct trend calculation
            metrics.sort(key=lambda m: m.period_start)

            # Calculate trends
            trends = {
                "orders": self._calculate_trend([m.total_orders for m in metrics]),
                "revenue": self._calculate_trend([m.total_amount for m in metrics]),
                "avg_order_value": self._calculate_trend([m.average_order_value for m in metrics]),
                "order_frequency": self._calculate_trend([m.order_frequency for m in metrics]),
            }

            return {"trends": trends, "metrics": metrics}
        except Exception as e:
            raise HTTPException(status_code=500, detail=f"Failed to analyze trends: {str(e)}")

    async def get_restaurant_rankings(self, metric: str, limit: int) -> List[Dict]:
        """Get restaurant rankings by specified metric"""
        try:
            # Get last month's metrics for all restaurants
            end_date = date.today()
            start_date = end_date - timedelta(days=30)

            metrics = await self.repository.get_all_restaurant_metrics(start_date, end_date)

            # Sort by specified metric
            sorted_metrics = sorted(metrics, key=lambda x: getattr(x, metric), reverse=True)[:limit]

            return [{"restaurant_id": m.restaurant_id, "metric_value": getattr(m, metric)} for m in sorted_metrics]
        except Exception as e:
            raise HTTPException(status_code=500, detail=f"Failed to get rankings: {str(e)}")

    def _calculate_trend(self, values: List[float]) -> float:
        """Calculate trend percentage change"""
        if len(values) < 2:
            return 0
        first, last = values[0], values[-1]
        return ((last - first) / first) * 100 if first != 0 else 0
