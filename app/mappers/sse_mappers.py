from app.models.glucose import Glucose
from app.models.alarm import Alarm

def map_glucose_to_sse_payload(glucose_data: Glucose) -> dict:
    return {
        "value": glucose_data.value,
        "timestamp": glucose_data.timestamp.isoformat(),
        "trend": glucose_data.trend.value,
        "source": glucose_data.source,
        "status": glucose_data.status.value,
    }

def map_alarm_to_sse_payload(alarm_data: Alarm) -> dict:
    return {
        "id": str(alarm_data.id) if alarm_data.id else None,
        "level": alarm_data.level,
        "message": alarm_data.message,
        "timestamp": alarm_data.timestamp.isoformat(),
        "user_id": alarm_data.user_id
    }