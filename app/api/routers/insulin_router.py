from fastapi import APIRouter, Depends

from app.core.dependencies import get_current_user_id, get_insulin_service
from app.infrastructure.interfaces.insulin_service_interface import IInsulinService


router = APIRouter(prefix="/api/v1/insulin", tags=["Insulin Data"])


@router.post("/add-new-insulin", response_model=bool)
async def add_new_insulin(
        insulin_name: str,
        current_user_id: str = Depends(get_current_user_id),
        service: IInsulinService = Depends(get_insulin_service)
):
    service.add_new_insulin_type(current_user_id, insulin_name)
    return True