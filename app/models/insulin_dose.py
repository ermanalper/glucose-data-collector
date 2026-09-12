import datetime
from dataclasses import dataclass

from app.models.insulin import Insulin


@dataclass(slots=True)
class InsulinDose:
    user_id: str
    insulin_type: Insulin
    dose: float
    timestamp: datetime
    glucose_value: int # the glucose value when the dose is shot