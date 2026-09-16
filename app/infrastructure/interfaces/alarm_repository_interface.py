from abc import ABC, abstractmethod
from typing import List

from app.models.alarm import Alarm


class IAlarmRepository(ABC):
    @abstractmethod
    def set_alarm(self, alarm: Alarm):
        pass

    @abstractmethod
    def reset_alarm(self, alarm_id: UUID):
        pass

    @abstractmethod
    def get_active_alarms(self, user_id: str) -> List[Alarm]:
        pass