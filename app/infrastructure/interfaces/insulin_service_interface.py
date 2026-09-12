import datetime
from abc import ABC, abstractmethod
from typing import List

from app.models.insulin_dose import InsulinDose


class IInsulinService(ABC):
    @abstractmethod
    def add_new_insulin_type(self, brand: str):
        pass

    @abstractmethod
    def enter_insulin_dose(self, user_id: str, insulin_id: int, dose: float, timestamp: datetime):
        pass

    @abstractmethod
    def get_insulin_history_by_time_interval(self, start_time: datetime, end_time: datetime, user_id: str) -> List[InsulinDose]:
        pass

