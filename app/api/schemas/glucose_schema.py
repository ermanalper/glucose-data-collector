from pydantic import BaseModel
from datetime import datetime


class GlucoseResponse(BaseModel):
    value: int
    timestamp: datetime
    trend: str
    source: str
    status: str #estimation of current status
    # auto read orm objects (pydantic v2 setting)
    model_config = {"from_attributes": True}

class PushGlucosePayload(BaseModel):
    value: int
    trend_symbol: str
    timestamp_ms: int
