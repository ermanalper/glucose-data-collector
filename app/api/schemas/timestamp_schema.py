from datetime import datetime

from pydantic import BaseModel


class TimestampResponse(BaseModel):
    timestamp: datetime