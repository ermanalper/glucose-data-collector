from datetime import datetime, timezone
from fastapi import APIRouter, Depends, Query
from app.api.schemas.glucose_schema import GlucoseResponse
from app.api.schemas.timestamp_schema import TimestampResponse
from app.core.exceptions import ResourceNotFoundException
from app.core.dependencies import get_current_user_id, get_glucose_service
from fastapi import APIRouter, Depends, Request
from sse_starlette.sse import EventSourceResponse
from app.core.dependencies import get_sse_broadcaster
from app.infrastructure.interfaces.glucose_service_interface import IGlucoseService
from app.infrastructure.interfaces.sse_broadcaster_interface import ISSEBroadcaster
router = APIRouter(prefix="/api/v1/glucose", tags=["Glucose Data"])


@router.get("/latest", response_model=GlucoseResponse)
async def get_latest_glucose(
        current_user_id: str = Depends(get_current_user_id),
        service: IGlucoseService = Depends(get_glucose_service)
):
    latest_data = service.get_latest_glucose(user_id=current_user_id)
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
        service: IGlucoseService = Depends(get_glucose_service)
):
    historical_data = service.get_latest_n_readings(user_id=current_user_id, n=limit, offset=offset)


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
        service: IGlucoseService = Depends(get_glucose_service)
):
    historical_data = service.get_glucose_by_time_interval(
        user_id=current_user_id,
        start=start_time,
        end=end_time
    )

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
        service: IGlucoseService = Depends(get_glucose_service)):
    first_entry_date = service.get_first_glucose_entry_date(current_user_id)
    return TimestampResponse(timestamp=first_entry_date)

@router.get("/stream", description="Glucose data tunnel to frontends")
async def stream_glucose(
    request: Request,
    service: IGlucoseService = Depends(get_glucose_service)
):
    return EventSourceResponse(service.subscribe_to_glucose_stream())