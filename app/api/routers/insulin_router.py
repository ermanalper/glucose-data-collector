from fastapi import APIRouter, Depends

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


@router.post("/enter-insulin-dose", response_model=InsulinDoseResponse)
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