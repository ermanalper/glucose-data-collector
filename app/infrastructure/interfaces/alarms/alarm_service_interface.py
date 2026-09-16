from abc import ABC, abstractmethod
from typing import List
from uuid import UUID

from app.models.alarm import Alarm
from app.models.glucose import Glucose


class IAlarmService(ABC):
    @abstractmethod
    def set_alarm(self, user_id: str, message: str, level: int):
        pass

    @abstractmethod
    def reset_alarm(self, alarm_id: UUID):
        pass

    @abstractmethod
    def _handle_new_glucose_data(self, sender, glucose_data: Glucose, **kwargs):
        pass

    @abstractmethod
    def get_active_alarms(self, user_id: str) -> List[Alarm]:
        pass