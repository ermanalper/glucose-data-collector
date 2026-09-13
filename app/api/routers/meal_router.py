from typing import List

from fastapi import APIRouter, Depends

from app.api.schemas.meal_schema import MealRequest, MealShortcutRequest, MealShortcutResponse
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

@router.post("/add-meal-shortcut", response_model=bool)
async def add_meal_shortcut(
        payload: MealShortcutRequest,
        user_id: str = Depends(get_current_user_id),
        service: IMealService = Depends(get_meal_service)
):
    service.save_meal_shortcut(user_id=user_id,
                               title=payload.title,
                               desc=payload.desc)
    return True

@router.get("/meal-shortcuts", response_model=List[MealShortcutResponse])
async def get_meal_shortcuts(
        user_id: str = Depends(get_current_user_id),
        service: IMealService = Depends(get_meal_service)
):
    meal_shortcuts = service.get_meal_shortcuts(user_id)
    return [
        MealShortcutResponse(
            title=shortcut.title,
            desc=shortcut.desc
        )
        for shortcut in meal_shortcuts
    ]