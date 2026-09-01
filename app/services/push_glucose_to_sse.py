from app.api.schemas.glucose_schema import GlucoseResponse
from app.core.dependencies import get_sse_broadcaster, get_serializer
from app.events.events import new_glucose_data_event
from app.models.glucose import Glucose


@new_glucose_data_event.connect
def push_glucose_to_sse(sender, glucose_data: Glucose, **kwargs):
    broadcaster = get_sse_broadcaster()
    serializer = get_serializer()

    payload_dict = GlucoseResponse.model_validate(glucose_data).model_dump()

    serialized_data = serializer.serialize(payload_dict)

    broadcaster.broadcast(
        event_name="new_glucose",
        data=serialized_data
    )