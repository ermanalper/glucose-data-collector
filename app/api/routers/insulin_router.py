from fastapi import APIRouter, Depends

from app.core.dependencies import get_current_user_id, get_insulin_repository
from app.infrastructure.interfaces.insulin_repository_interface import IInsulinRepository

#from app.services.insulin_service import InsulinService
#from app.core.dependencies import get_insulin_service

router = APIRouter(prefix="/api/v1/insulin", tags=["Insulin Data"])


@router.post("/add-new-insulin", response_model=bool)
async def add_new_insulin(
        insulin_name: str,
        current_user_id: str = Depends(get_current_user_id),
        service: IInsulinService
):

    return True