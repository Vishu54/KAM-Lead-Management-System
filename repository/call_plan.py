import logging
from typing import Optional, List
from datetime import date, timedelta

from models.call_plan import CallPlan
from core.custom_exception import handle_exception
from core.database import managed_transaction, DbConnector

logger = logging.getLogger(__name__)


class CallPlanRepository:
    @managed_transaction
    async def create(self, restaurant_id: str, user_id: str, frequency_days: int, next_call_date: date, notes: Optional[str] = None, db: Optional[DbConnector] = None) -> CallPlan:
        try:
            call_plan = CallPlan(restaurant_id=restaurant_id, user_id=user_id, frequency_days=frequency_days, next_call_date=next_call_date, notes=notes)
            db.Session.add(call_plan)
            return call_plan
        except Exception as e:
            logger.error(f"Error creating call plan: {str(e)}")
            handle_exception(message="Failed to create call plan")

    @managed_transaction
    async def get_due_calls(self, due_date: date, db: Optional[DbConnector] = None) -> List[CallPlan]:
        try:
            query = db.Session.query(CallPlan).filter(CallPlan.next_call_date <= due_date).all()
            return query
        except Exception as e:
            logger.error(f"Error fetching due calls: {str(e)}")
            handle_exception(message="Failed to fetch due calls")

    @managed_transaction
    async def update_after_call(self, call_plan_id: str, call_date: date, db: Optional[DbConnector] = None) -> Optional[CallPlan]:
        try:
            call_plan = db.Session.query(CallPlan).filter(CallPlan.call_plan_id == call_plan_id).first()
            if call_plan:
                call_plan.last_call_date = call_date
                call_plan.next_call_date = call_date + timedelta(days=call_plan.frequency_days)
                return call_plan
            return None
        except Exception as e:
            logger.error(f"Error updating call plan: {str(e)}")
            handle_exception(message="Failed to update call plan")
