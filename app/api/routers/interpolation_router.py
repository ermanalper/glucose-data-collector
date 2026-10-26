from datetime import datetime, timezone

from fastapi import APIRouter, Query, Depends

from app.api.schemas.poly_schema import PolyResponse
from app.core.dependencies import get_foresee_glucose_service, get_current_user_id
from app.models.poly_result import PolyResult
from app.services.interfaces.foresee_glucose_service_interface import IForeseeGlucoseService

router = APIRouter(prefix="/api/v1/foresee-glucose", tags=["Foresee Glucose Data"])

@router.get("/interpolate", response_model=PolyResponse)
def get_glucose_data_interpolation(
            start_time: datetime = Query(..., description="Start time (e.g.: 2026-08-28T10:00:00)"),
            end_time: datetime = Query(default_factory=lambda: datetime.now(timezone.utc),
                                       description="End time (Default: UTC now)"),
            current_user_id: str = Depends(get_current_user_id),
            service: IForeseeGlucoseService = Depends(get_foresee_glucose_service)
):
    poly : PolyResult = service.interpolate(start_time=start_time, end_time=end_time, user_id=current_user_id)
    return PolyResponse(
        coefficients=poly.coefficients,
        degree=poly.degree
    )