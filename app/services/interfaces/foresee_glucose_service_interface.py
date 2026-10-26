from abc import ABC, abstractmethod
from datetime import datetime

from app.models.poly_result import PolyResult


class IForeseeGlucoseService(ABC):
    @abstractmethod
    def interpolate(self, start_time: datetime, end_time: datetime, user_id: str) -> PolyResult:
        pass