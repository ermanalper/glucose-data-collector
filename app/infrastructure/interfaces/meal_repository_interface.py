from abc import ABC, abstractmethod

from app.models.meal import Meal
from app.models.meal_shortcut import MealShortcut


class IMealRepository(ABC):
    @abstractmethod
    def save_meal(self, meal: Meal):
        pass

    @abstractmethod
    def save_meal_shortcut(self, meal_shortcut: MealShortcut):
        pass