from app.infrastructure.interfaces.alarm_service_interface import IAlarmService
from app.models.alarm import Alarm


class AlarmServiceImpl(IAlarmService):
    def set_alarm(self, alarm: Alarm):
        pass

    def reset_alarm(self, alarm: Alarm):
        pass