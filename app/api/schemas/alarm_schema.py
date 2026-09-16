from datetime import datetime
from uuid import UUID

from pydantic import BaseModel, ConfigDict


class AlarmResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    level: int
    message: str
    timestamp: datetime
    id: UUID | None = None

class AlarmRequest(BaseModel):
    level: int
    message: str

