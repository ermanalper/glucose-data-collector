from app.core.dependencies import get_sse_broadcaster, get_serializer
from app.events.events import run_test_client_protocol_event


@run_test_client_protocol_event.connect
def push_reset_alarm_to_sse(sender, client_name: str, **kwargs):
    broadcaster = get_sse_broadcaster()
    serializer = get_serializer()

    serialized_data = serializer.serialize(client_name)

    broadcaster.broadcast(
        event_name="run_client_test_protocol",
        data=serialized_data
    )