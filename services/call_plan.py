import logging
from typing import Optional, List
from datetime import date, timedelta

from models.call_plan import CallPlan
from repository.call_plan import CallPlanRepository
from core.custom_exception import handle_exception

logger = logging.getLogger(__name__)


class CallPlanService:
    def __init__(self, repository: CallPlanRepository):
        self.repository = repository

    async def create_call_plan(self, call_plan_data: dict) -> CallPlan:
        try:
            next_call_date = date.today() + timedelta(days=call_plan_data["frequency_days"])
            return await self.repository.create(**call_plan_data, next_call_date=next_call_date)
        except Exception as e:
            logger.error(f"Error in create_call_plan service: {str(e)}")
            handle_exception(message="Failed to create call plan")

    async def get_due_calls(self, due_date: Optional[date] = None) -> List[CallPlan]:
        try:
            if due_date is None:
                due_date = date.today()
            return await self.repository.get_due_calls(due_date)
        except Exception as e:
            logger.error(f"Error in get_due_calls service: {str(e)}")
            handle_exception(message="Failed to fetch due calls")

    async def record_call_made(self, call_plan_id: str, call_date: Optional[date] = None) -> Optional[CallPlan]:
        try:
            if call_date is None:
                call_date = date.today()
            return await self.repository.update_after_call(call_plan_id, call_date)
        except Exception as e:
            logger.error(f"Error in record_call_made service: {str(e)}")
            handle_exception(message="Failed to record call")
