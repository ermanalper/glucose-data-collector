from abc import abstractmethod, ABC

from app.models.insulin import Insulin
from app.models.insulin_dose import InsulinDose


class IInsulinRepository(ABC):
    @abstractmethod
    def add_insulin(self, insulin: Insulin):
        pass

    @abstractmethod
    def enter_insulin_dose(self, dose: InsulinDose):
        pass