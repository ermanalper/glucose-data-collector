from fastapi import APIRouter, Depends

from app.api.schemas.meal_schema import MealRequest
from app.core.dependencies import get_current_user_id, get_meal_service
from app.infrastructure.interfaces.meal_service_interface import IMealService

router = APIRouter(prefix="/api/v1/meal", tags=["Meal Data"])

@router.post("/add-meal", response_model=bool)
async def add_meal(
        payload: MealRequest,
        user_id: str = Depends(get_current_user_id),
        service: IMealService = Depends(get_meal_service)
):
    service.add_meal(
        user_id=user_id,
        desc=payload.desc,
        timestamp=payload.timestamp)
    return True
