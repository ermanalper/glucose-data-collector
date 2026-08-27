from fastapi import APIRouter, Depends, HTTPException
from app.api.schemas.glucose_schema import GlucoseResponse
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
        raise HTTPException(status_code=404, detail="No glucose data")

    return GlucoseResponse(
        value=latest_data.value,
        timestamp=latest_data.timestamp,
        trend=latest_data.trend.value,
        source=latest_data.source
    )