from datetime import datetime, timezone
from uuid import UUID

from app.core.exceptions import WTF, FalseArgumentException
from app.events.events import new_glucose_data_event, alarm_set_event, alarm_reset_event, reset_alarms_of_user_event
from app.infrastructure.interfaces.alarms.alarm_repository_interface import IAlarmRepository
from app.infrastructure.interfaces.alarms.alarm_service_interface import IAlarmService
from app.models.alarm import Alarm
from app.models.glucose import Glucose, GlucoseStatus


class AlarmServiceImpl(IAlarmService):
    def __init__(self, repo : IAlarmRepository):
        new_glucose_data_event.connect(self._handle_new_glucose_data)
        self._repo = repo
        self._lvl = 0

    def _handle_new_glucose_data(self, sender, glucose_data: Glucose, **kwargs):
        prev_lvl = self._lvl
        status = glucose_data.status
        if not isinstance(status, GlucoseStatus):
            raise FalseArgumentException(message="glucose_data.status must be an instance of GlucoseStatus")
        if status in [GlucoseStatus.CRITICAL, GlucoseStatus.WARNING]:
            msg=""
            if status is GlucoseStatus.WARNING:
                msg = "Warning Alarm"
                self._lvl = 1
            elif status is GlucoseStatus.CRITICAL:
                msg = "CRITICAL ALARM"
                self._lvl = 2
            else:
                raise WTF("WTF???")
            if self._lvl > prev_lvl:
                self.set_alarm(user_id=glucose_data.user_id, message=msg, level=self._lvl)
        else:
            self._lvl = 0
            print('Everything is normal')

    # usually this should be a private function because alarms are not set manually, but automatically
    # but for test concerns, this can be called from an endpoint
    def set_alarm(self, user_id: str, message: str, level: int):
        alarm = Alarm(user_id=user_id, level=level, message=message, timestamp = datetime.now(timezone.utc), id=None)
        alarm_id = self._repo.set_alarm(alarm)
        alarm.id = alarm_id
        alarm_set_event.send(self, alarm_data=alarm)


    def reset_alarm(self, alarm_id: UUID):
        self._repo.reset_alarm(alarm_id)
        alarm_reset_event.send(self, alarm_id=alarm_id)

    def get_active_alarms(self, user_id: str):
        active_alarms = self._repo.get_active_alarms(user_id)
        return active_alarms

    def reset_all_alarms_of_user(self, user_id: str):
        self._repo.reset_all_alarms_of_user(user_id)
        reset_alarms_of_user_event.send(user_id=user_id)