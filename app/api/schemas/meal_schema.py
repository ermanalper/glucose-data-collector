from datetime import datetime, timezone
from pydantic import BaseModel, Field

class MealRequest(BaseModel):
    desc: str = Field(..., description="Description of the meal")
    timestamp: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))

