from typing import List
from uuid import UUID

from fastapi import APIRouter, Depends

from app.api.schemas.alarm_schema import AlarmResponse, AlarmRequest
from app.core.dependencies import get_current_user_id, get_alarm_service
from app.infrastructure.interfaces.alarms.alarm_service_interface import IAlarmService

router = APIRouter(prefix="/api/v1/alarm", tags=["Alarm Data"])

# this is for test concerns. normally alarms are set automatically
@router.post("/set-alarm")
def set_alarm(payload: AlarmRequest,
              user_id: str = Depends(get_current_user_id),
              service: IAlarmService = Depends(get_alarm_service)):
    service.set_alarm(user_id=user_id, message=payload.message, level=payload.level)


@router.get("/active-alarms", response_model=List[AlarmResponse])
def get_active_alarms(user_id: str = Depends(get_current_user_id),
                      service: IAlarmService = Depends(get_alarm_service)):
    active_alarms = service.get_active_alarms(user_id)
    return [
        AlarmResponse(
            level=alarm.level,
            message=alarm.message,
            timestamp=alarm.timestamp,
            id=alarm.id
        ) for alarm in active_alarms
    ]

@router.patch("/ack-alarm")
def ack_active_alarm(alarm_id: UUID,
                     #user_id: str = Depends(get_current_user_id), You might want to see if the user trying to
                     #                                              acknowledge the alarm is actually the owner of the alarm
                     service: IAlarmService = Depends(get_alarm_service)):
    service.reset_alarm(alarm_id)
