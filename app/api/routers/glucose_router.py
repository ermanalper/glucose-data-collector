from datetime import datetime, timezone
from fastapi import APIRouter, Depends, Query
from app.api.schemas.glucose_schema import GlucoseResponse
from app.api.schemas.timestamp_schema import TimestampResponse
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
        source=latest_data.source,
        status=latest_data.status
    )


@router.get("/history", response_model=list[GlucoseResponse])
async def get_glucose_history_data_count_offset(
        limit: int = Query(default=10, ge=1, le=100, description="Number of latest readings to be fetched"),
        offset: int = Query(default=0, ge=0, description="Number of latest readiangs to skip"),
        current_user_id: str = Depends(get_current_user_id),
        repo: IGlucoseRepository = Depends(get_glucose_repository)
):
    historical_data = repo.get_latest_n(user_id=current_user_id, n=limit, offset=offset)

    if not historical_data:
        raise ResourceNotFoundException("No glucose data found for this user.")

    return [
        GlucoseResponse(
            value=data.value,
            timestamp=data.timestamp,
            trend=data.trend.value,
            source=data.source,
            status=data.status
        )
        for data in historical_data
    ]

@router.get("/history/by-time", response_model=list[GlucoseResponse])
async def get_glucose_history_time_interval(
        start_time: datetime = Query(..., description="Start time (e.g.: 2026-08-28T10:00:00)"),
        end_time: datetime = Query(default_factory=lambda: datetime.now(timezone.utc), description="End time (Default: UTC now)"),
        current_user_id: str = Depends(get_current_user_id),
        repo: IGlucoseRepository = Depends(get_glucose_repository)
):
    historical_data = repo.get_by_time_interval(
        user_id=current_user_id,
        start=start_time,
        end=end_time
    )

    if not historical_data:
        raise ResourceNotFoundException("No glucose data found for this time interval.")

    return [
        GlucoseResponse(
            value=data.value,
            timestamp=data.timestamp,
            trend=data.trend.value,
            source=data.source,
            status=data.status
        )
        for data in historical_data
    ]

@router.get("/first-data-date", response_model=TimestampResponse)
async def get_first_data_date(
        current_user_id: str = Depends(get_current_user_id),
        repo: IGlucoseRepository = Depends(get_glucose_repository)):
    first_entry_date = repo.get_first_entry_date(current_user_id)
    return TimestampResponse(timestamp=first_entry_date)