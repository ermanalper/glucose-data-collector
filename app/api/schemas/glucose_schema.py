from pydantic import BaseModel
from datetime import datetime


class GlucoseResponse(BaseModel):
    value: int
    timestamp: datetime
    trend: str
    source: str

    # auto read orm objects (pydantic v2 setting)
    model_config = {"from_attributes": True}