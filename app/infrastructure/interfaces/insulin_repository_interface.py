from abc import abstractmethod, ABC

from app.models.insulin import Insulin


class IInsulinRepository(ABC):
    @abstractmethod
    def add_insulin(self, insulin: Insulin):
        pass