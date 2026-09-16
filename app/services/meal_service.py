import datetime
from typing import List

from app.core.exceptions import ResourceNotFoundException
from app.infrastructure.interfaces.glucose.glucose_service_interface import IGlucoseService
from app.infrastructure.interfaces.meals.meal_repository_interface import IMealRepository
from app.infrastructure.interfaces.meals.meal_service_interface import IMealService
from app.models.meal import Meal
from app.models.meal_shortcut import MealShortcut


class MealServiceImpl(IMealService):
    def __init__(self, repo: IMealRepository, glucose_service: IGlucoseService):
        self._repo = repo
        self._glucose_service = glucose_service

    def add_meal(self, user_id: str, desc: str, timestamp: datetime):
        glucose_val = self._glucose_service.get_glucose_value_at_time(user_id, timestamp)
        meal = Meal(user_id=user_id, desc=desc, timestamp=timestamp, glucose_value=glucose_val)
        self._repo.save_meal(meal)

    def save_meal_shortcut(self, user_id: str, title: str, desc: str):
        meal_shortcut = MealShortcut(user_id=user_id, title=title, desc=desc)
        self._repo.save_meal_shortcut(meal_shortcut)

    def get_meal_shortcuts(self, user_id: str) -> List[MealShortcut]:
        return self._repo.get_meal_shortcuts(user_id)


    def get_meal_history_by_time(self, user_id: str, start_time: datetime, end_time: datetime) -> List[Meal]:
        history = self._repo.get_meal_history_by_time_interval(start_time=start_time, end_time=end_time,
                                                                  user_id=user_id)
        if not history:
            raise ResourceNotFoundException("No meal data found for this time interval'.")
        return history