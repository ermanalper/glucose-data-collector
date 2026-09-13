from datetime import datetime

from pydantic import Field, BaseModel



class InsulinResponse(BaseModel):
    id: int
    type: str
