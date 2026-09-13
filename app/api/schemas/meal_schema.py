from datetime import datetime, timezone
from pydantic import BaseModel, Field

class MealRequest(BaseModel):
    desc: str = Field(..., description="Description of the meal")
    timestamp: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))

class MealShortcutRequest(BaseModel):
    title: str = Field(..., description="Title of the meal")
    desc: str = Field(..., description="Description of the meal")

class MealResponse(BaseModel):
    id: int
    desc: str
    timestamp: datetime

class MealShortcutResponse(BaseModel):
    title: str
    desc: str