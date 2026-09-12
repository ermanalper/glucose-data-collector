import datetime
from dataclasses import dataclass

from app.models.insulin import Insulin


@dataclass(slots=True)
class InsulinDose:
    user_id: str
    insulin_type: Insulin
    dose: float
    timestamp: datetime