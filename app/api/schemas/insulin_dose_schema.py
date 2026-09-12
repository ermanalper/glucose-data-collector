from datetime import datetime

from pydantic import BaseModel


class InsulinDoseResponse(BaseModel):
    message: str
