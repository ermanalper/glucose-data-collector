import datetime
from abc import ABC, abstractmethod


class IMealService(ABC):
    @abstractmethod
    def add_meal(self, user_id: str, desc: str, timestamp: datetime):
        pass

    @abstractmethod
    def save_meal_shortcut(self, user_id: str, title: str, desc: str):
        pass