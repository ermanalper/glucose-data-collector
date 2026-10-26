from abc import ABC, abstractmethod
from datetime import datetime

from app.models.poly_result import PolyResult


class IInterpolationRepository(ABC):
    @abstractmethod
    def save_interpolation(self, poly: PolyResult, timestamp: datetime):
        pass