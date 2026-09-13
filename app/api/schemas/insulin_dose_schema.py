from datetime import datetime, timezone

from pydantic import BaseModel, Field


class InsulinDoseRequest(BaseModel):
    insulin_id: int = Field(..., description="ID of the insulin type")
    dose: float = Field(..., gt=0, description="Dose of the insulin")
    timestamp: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))

class InsulinDoseResponse(BaseModel):
    insulin_type: str
    timestamp: datetime
    dose: float
    glucose_val: int
    glucose_val: int | None = None
