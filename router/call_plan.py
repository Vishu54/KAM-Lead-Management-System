from fastapi import APIRouter, Depends, HTTPException, Query, status
from datetime import date
from typing import Optional

from fastapi.security import OAuth2PasswordBearer

from services.call_plan import CallPlanService
from repository.call_plan import CallPlanRepository
from schema.call_plan import CallPlanCreate, CallPlanResponse, CallPlanListResponse

router = APIRouter(prefix="/call-plans", tags=["call-plans"])

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/v1/auth/login")


def get_call_plan_service() -> CallPlanService:
    repository = CallPlanRepository()
    return CallPlanService(repository)


@router.post("/", response_model=CallPlanResponse, status_code=status.HTTP_201_CREATED)
async def create_call_plan(call_plan: CallPlanCreate, service: CallPlanService = Depends(get_call_plan_service), token: str = Depends(oauth2_scheme)):
    """Create a new call plan"""
    return await service.create_call_plan(call_plan.model_dump())


@router.get("/due-calls", response_model=CallPlanListResponse)
async def get_due_calls(
    due_date: Optional[date] = Query(default=None, description="Date to check for due calls (YYYY-MM-DD). Defaults to today if not provided.", examples="2024-12-23"),
    service: CallPlanService = Depends(get_call_plan_service),
    token: str = Depends(oauth2_scheme),
):
    """Get all calls due by the specified date"""
    calls = await service.get_due_calls(due_date)
    return CallPlanListResponse(total=len(calls), call_plans=calls)


@router.post("/{call_plan_id}/record-call")
async def record_call(
    call_plan_id: str,
    call_date: Optional[date] = Query(
        default=None,
        description="Date the call was made (YYYY-MM-DD). Defaults to today if not provided.",
        examples="2024-12-23",
    ),
    service: CallPlanService = Depends(get_call_plan_service),
    token: str = Depends(oauth2_scheme),
):
    """Record that a call was made"""
    updated_plan = await service.record_call_made(call_plan_id, call_date)
    if not updated_plan:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Call plan not found")
    return updated_plan
