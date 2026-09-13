import datetime
from abc import ABC, abstractmethod
from typing import List

from app.models.meal_shortcut import MealShortcut


class IMealService(ABC):
    @abstractmethod
    def add_meal(self, user_id: str, desc: str, timestamp: datetime):
        pass

    @abstractmethod
    def save_meal_shortcut(self, user_id: str, title: str, desc: str):
        pass

    @abstractmethod
    def get_meal_shortcuts(self, user_id: str) -> List[MealShortcut]:
        pass