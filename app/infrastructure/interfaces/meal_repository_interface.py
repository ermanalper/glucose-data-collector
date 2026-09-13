from abc import ABC, abstractmethod

from app.models.meal import Meal


class IMealRepository(ABC):
    @abstractmethod
    def save_meal(self, meal: Meal):
        pass