from abc import abstractmethod, ABC
from typing import List

from app.models.insulin import Insulin
from app.models.insulin_dose import InsulinDose


class IInsulinRepository(ABC):
    @abstractmethod
    def add_insulin(self, insulin: Insulin):
        pass

    @abstractmethod
    def enter_insulin_dose(self, dose: InsulinDose):
        pass

    @abstractmethod
    def get_insulin_history_by_time_interval(self, start_time, end_time, user_id):
        pass

    @abstractmethod
    def get_insulin_types(self) -> List[Insulin]:
        pass