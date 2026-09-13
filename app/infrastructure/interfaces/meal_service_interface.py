import datetime
from abc import ABC, abstractmethod


class IMealService(ABC):
    @abstractmethod
    def add_meal(self, user_id: str, desc: str, timestamp: datetime):
        pass
