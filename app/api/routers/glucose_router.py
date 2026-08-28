from fastapi import APIRouter, Depends, Query
from app.api.schemas.glucose_schema import GlucoseResponse
from app.core.exceptions import ResourceNotFoundException
from app.infrastructure.interfaces.glucose_repository_interface import IGlucoseRepository
from app.core.dependencies import get_glucose_repository, get_current_user_id

router = APIRouter(prefix="/api/v1/glucose", tags=["Glucose Data"])


@router.get("/latest", response_model=GlucoseResponse)
async def get_latest_glucose(
        current_user_id: str = Depends(get_current_user_id),
        repo: IGlucoseRepository = Depends(get_glucose_repository)
):
    latest_data = repo.get_latest(user_id=current_user_id)

    if not latest_data:
        raise ResourceNotFoundException("No glucose data found for this user.")

    return GlucoseResponse(
        value=latest_data.value,
        timestamp=latest_data.timestamp,
        trend=latest_data.trend.value,
        source=latest_data.source
    )


@router.get("/history", response_model=list[GlucoseResponse])
async def get_glucose_history(
        limit: int = Query(default=10, ge=1, le=100, description="Number of latest readings to be fetched"),
        current_user_id: str = Depends(get_current_user_id),
        repo: IGlucoseRepository = Depends(get_glucose_repository)
):
    historical_data = repo.get_latest_n(user_id=current_user_id, n=limit)

    if not historical_data:
        raise ResourceNotFoundException("No glucose data found for this user.")

    return [
        GlucoseResponse(
            value=data.value,
            timestamp=data.timestamp,
            trend=data.trend.value,
            source=data.source
        )
        for data in historical_data
    ]