from datetime import datetime

from pydantic import BaseModel


class InsulinDoseResponse(BaseModel):
    insulin_type: str
    timestamp: datetime
    dose: float
    glucose_val: int
    glucose_val: int | None = None
