from app.api.schemas.alarm_schema import AlarmResponse
from app.core.dependencies import get_sse_broadcaster, get_serializer
from app.events.events import alarm_triggered_event
from app.models.alarm import Alarm


@alarm_triggered_event.connect
def push_alarm_to_sse(sender, alarm_data: Alarm, **kwargs):
    broadcaster = get_sse_broadcaster()
    serializer = get_serializer()

    payload_dict = AlarmResponse.model_validate(alarm_data).model_dump()

    serialized_data = serializer.serialize(payload_dict)

    broadcaster.broadcast(
        event_name="alarm",
        data=serialized_data
    )