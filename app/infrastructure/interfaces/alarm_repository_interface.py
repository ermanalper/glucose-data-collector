from abc import ABC, abstractmethod

from app.models.alarm import Alarm


class IAlarmRepository(ABC):
    @abstractmethod
    def set_alarm(self, alarm: Alarm):
        pass

    @abstractmethod
    def reset_alarm(self, alarm: Alarm):
        pass