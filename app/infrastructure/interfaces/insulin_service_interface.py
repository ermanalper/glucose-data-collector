import datetime
from abc import ABC, abstractmethod


class IInsulinService(ABC):
    @abstractmethod
    def add_new_insulin_type(self, brand: str):
        pass

    @abstractmethod
    def enter_insulin_dose(self, user_id: str, insulin_id: int, dose: float, timestamp: datetime):
        pass

