from abc import ABC, abstractmethod
from typing import Optional, AsyncGenerator

from app.models.glucose import Glucose


class IGlucoseService(ABC):
    @abstractmethod
    def get_latest_glucose(self, user_id: str) -> Optional[Glucose]:
        pass
    
    @abstractmethod
    def get_latest_n_readings(self, user_id, n, offset) -> list[Glucose]:
        pass

    @abstractmethod
    def get_glucose_by_time_interval(self, user_id, start, end) -> list[Glucose]:
        pass

    @abstractmethod
    def get_first_glucose_entry_date(self, current_user_id):
        pass

    @abstractmethod
    def subscribe_to_glucose_stream(self) -> AsyncGenerator[dict, None]:
        pass