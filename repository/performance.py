import logging
from typing import Optional, List
from datetime import date
from sqlalchemy import func

from models.performance_metric import PerformanceMetric
from models.order import Order
from core.custom_exception import handle_exception
from core.database import managed_transaction, DbConnector

logger = logging.getLogger(__name__)


class PerformanceRepository:
    @managed_transaction
    async def calculate_metrics(self, restaurant_id: str, start_date: date, end_date: date, db: Optional[DbConnector] = None) -> PerformanceMetric:
        try:
            # Get orders for the period
            orders = db.Session.query(Order).filter(Order.restaurant_id == restaurant_id, func.date(Order.created_at) >= start_date, func.date(Order.created_at) <= end_date).all()

            total_orders = len(orders)
            total_amount = sum(order.amount for order in orders)
            avg_order_value = total_amount / total_orders if total_orders > 0 else 0

            # Calculate order frequency
            if total_orders > 1:
                date_diff = (end_date - start_date).days
                order_frequency = date_diff / total_orders
            else:
                order_frequency = 0

            metric = PerformanceMetric(
                restaurant_id=restaurant_id,
                period_start=start_date,
                period_end=end_date,
                total_orders=total_orders,
                total_amount=total_amount,
                average_order_value=avg_order_value,
                order_frequency=order_frequency,
            )

            db.Session.add(metric)
            return metric

        except Exception as e:
            logger.error(f"Error calculating performance metrics: {str(e)}")
            handle_exception(message="Failed to calculate performance metrics")

    @managed_transaction
    async def get_restaurant_metrics(self, restaurant_id: str, db: Optional[DbConnector] = None) -> List[PerformanceMetric]:
        try:
            return db.Session.query(PerformanceMetric).filter(PerformanceMetric.restaurant_id == restaurant_id).order_by(PerformanceMetric.period_start.desc()).all()
        except Exception as e:
            logger.error(f"Error fetching restaurant metrics: {str(e)}")
            handle_exception(message="Failed to fetch performance metrics")

    @managed_transaction
    async def get_metrics_by_period(self, restaurant_id: str, start_date: date, end_date: date, db: Optional[DbConnector] = None) -> List[PerformanceMetric]:
        try:
            metrics = (
                db.Session.query(PerformanceMetric)
                .filter(
                    PerformanceMetric.restaurant_id == restaurant_id, func.date(PerformanceMetric.created_at) >= start_date, func.date(PerformanceMetric.created_at) <= end_date
                )
                .order_by(PerformanceMetric.period_start.asc())
                .all()
            )
            return metrics
        except Exception as e:
            logger.error(f"Error fetching metrics by period: {str(e)}")
            handle_exception(message="Failed to fetch metrics")

    @managed_transaction
    async def get_all_restaurant_metrics(self, start_date: date, end_date: date, db: Optional[DbConnector] = None) -> List[PerformanceMetric]:
        try:
            return db.Session.query(PerformanceMetric).filter(PerformanceMetric.period_start >= start_date, PerformanceMetric.period_end <= end_date).all()
        except Exception as e:
            logger.error(f"Error fetching all restaurant metrics: {str(e)}")
            handle_exception(message="Failed to fetch metrics")
