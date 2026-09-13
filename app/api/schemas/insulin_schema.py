from datetime import datetime

from pydantic import Field, BaseModel


class InsulinDoseRequest(BaseModel):
    insulin_id: int = Field(..., description="ID of the insulin type")
    dose: float = Field(..., gt=0, description="Dose of the insulin")
    timestamp: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))

class InsulinResponse(BaseModel):
    id: int
    type: str
