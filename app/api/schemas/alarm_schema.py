from datetime import datetime

from pydantic import BaseModel, ConfigDict


class AlarmResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    level: int
    message: str
    timestamp: datetime