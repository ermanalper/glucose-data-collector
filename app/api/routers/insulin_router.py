from datetime import datetime, timezone
from typing import List

from fastapi import APIRouter, Depends, Query

from app.api.schemas.insulin_dose_schema import InsulinDoseResponse
from app.api.schemas.insulin_schema import InsulinDoseRequest
from app.core.dependencies import get_current_user_id, get_insulin_service
from app.infrastructure.interfaces.insulin_service_interface import IInsulinService


router = APIRouter(prefix="/api/v1/insulin", tags=["Insulin Data"])


@router.post("/add-new-insulin", response_model=bool)
async def add_new_insulin(
        insulin_name: str,
        service: IInsulinService = Depends(get_insulin_service)
):
    service.add_new_insulin_type(insulin_name)
    return True


@router.post("/enter-insulin-dose", response_model=str)
async def enter_insulin_dose(
        payload: InsulinDoseRequest,
        current_user_id: str = Depends(get_current_user_id),
        service: IInsulinService = Depends(get_insulin_service)
):
    result = service.enter_insulin_dose(
        user_id=current_user_id,
        insulin_id=payload.insulin_id,
        dose=payload.dose,
        timestamp=payload.timestamp
    )

    return result

@router.get("/history/by-time", response_model=List[InsulinDoseResponse])
async def get_insulin_dose_history_time_interval(
            start_time: datetime = Query(..., description="Start time (e.g.: 2026-08-28T10:00:00)"),
            end_time: datetime = Query(default_factory=lambda: datetime.now(timezone.utc),
                                       description="End time (Default: UTC now)"),
            current_user_id: str = Depends(get_current_user_id),
            service: IInsulinService = Depends(get_insulin_service)
):
   dose_history = service.get_insulin_history_by_time_interval(start_time=start_time, end_time=end_time, user_id=current_user_id)
   return [
       InsulinDoseResponse(
           insulin_type=insulin_dose.insulin_type.name,
           dose=insulin_dose.dose,
           timestamp=insulin_dose.timestamp,
           glucose_val=insulin_dose.glucose_value
       )
       for insulin_dose in dose_history
   ]