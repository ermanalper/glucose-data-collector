'''
PUSH CLIENTS:
    A push client gets the data posted to this backend using the relevant endpoint,
    and then publishes the new glucose data event
    !!! UNLIKE PULL CLIENTS

PUSH CLIENTS:
    A push client gets the data posted to this backend using the relevant endpoint,
    and then publishes the new glucose data event
'''
from datetime import datetime

from app.events.events import new_glucose_data_event
from app.infrastructure.interfaces.glucose_provider_interface import IGlucoseProvider
from app.models.glucose import TrendState, Glucose

TREND_MAP = {
    "↑↑": TrendState.DOUBLE_UP,
    "↑": TrendState.SINGLE_UP,
    "↗": TrendState.FORTY_FIVE_UP,
    "->": TrendState.FLAT,
    "↘": TrendState.FORTY_FIVE_DOWN,
    "↓": TrendState.SINGLE_DOWN,
    "↓↓": TrendState.DOUBLE_DOWN,

    "Steady": TrendState.FLAT,
    "Slowly Rising": TrendState.FORTY_FIVE_UP,
    "Rising": TrendState.SINGLE_UP,
    "Rapidly Rising": TrendState.DOUBLE_UP,
    "Slowly Falling": TrendState.FORTY_FIVE_DOWN,
    "Falling": TrendState.SINGLE_DOWN,
    "Rapidly Falling": TrendState.DOUBLE_DOWN,

    "Rising Slowly": TrendState.FORTY_FIVE_UP,
    "Rising Rapidly": TrendState.DOUBLE_UP,
    "Falling Slowly": TrendState.FORTY_FIVE_DOWN,
    "Falling Rapidly": TrendState.DOUBLE_DOWN,

    "Flat": TrendState.FLAT,
    "Rising slightly": TrendState.FORTY_FIVE_UP,
    "Rising rapidly": TrendState.DOUBLE_UP,
    "Falling slightly": TrendState.FORTY_FIVE_DOWN,
    "Falling rapidly": TrendState.DOUBLE_DOWN
}

class PushClient(IGlucoseProvider):
    def process_pushed_data(self, value: int, trend_symbol: str, timestamp_ms: int, **kwargs):
        dt_object = datetime.fromtimestamp(timestamp_ms / 1000.0)
        mapped_trend = TREND_MAP.get(trend_symbol, TrendState.UNKNOWN)

        glucose_obj = Glucose(
            value=value,
            timestamp=dt_object,
            trend=mapped_trend,
            source="Push_Client",
            raw_metadata={"original_symbol": trend_symbol}
        )
        new_glucose_data_event.send(self, glucose_data=glucose_obj)
