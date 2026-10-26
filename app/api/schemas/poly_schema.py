from pydantic import BaseModel


class PolyResponse(BaseModel):
    coefficients : list[float] #highest degree first
    degree: int
