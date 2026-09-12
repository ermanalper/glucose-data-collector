from datetime import datetime

from pydantic import BaseModel


class InsulinDoseResponse(BaseModel):
    insuline_type: str
    timestamp: datetime
    dose: float

