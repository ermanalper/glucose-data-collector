from app.core.dependencies import get_sse_broadcaster, get_serializer
from app.events.events import new_glucose_data_event
from app.mappers.sse_mappers import map_glucose_to_sse_payload
from app.models.glucose import Glucose


@new_glucose_data_event.connect
def push_glucose_to_sse(sender, glucose_data: Glucose, **kwargs):
    broadcaster = get_sse_broadcaster()
    serializer = get_serializer()

    payload_dict = map_glucose_to_sse_payload(glucose_data)

    serialized_data = serializer.serialize(payload_dict)

    broadcaster.broadcast(
        event_name="new_glucose",
        data=serialized_data
    )