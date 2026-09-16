'''
PUSH CLIENTS:
    A push client gets the data posted to this backend using the relevant endpoint,
    and then publishes the new glucose data event
    !!! UNLIKE PULL CLIENTS

PUSH CLIENTS:
    A push client gets the data posted to this backend using the relevant endpoint,
    and then publishes the new glucose data event
'''
'''
The same thins could have been done without the 'PushClient' term.
Just use an endpoint to push new glucose data (to the database), and write a 'PullClient' to fetch
from the database. But the real reason behind Push Clients is to avoid ambiguous dependency injections.
i.e. If a pull client is being used, the backend will raise an error when the webhook is used 
'''

from datetime import datetime

from app.events.events import new_glucose_data_event
from app.infrastructure.interfaces.glucose_provider_interface import IGlucoseProvider, IPushClient
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

class PushClient(IPushClient):
    def __init__(self, user_id:str="default_user"):
        self._user_id = user_id
    def process_pushed_data(self, value: int, trend_symbol: str, timestamp_ms: int, **kwargs):
        dt_object = datetime.fromtimestamp(timestamp_ms / 1000.0)
        mapped_trend = TREND_MAP.get(trend_symbol, TrendState.UNKNOWN)

        glucose_obj = Glucose(
            value=value,
            timestamp=dt_object,
            trend=mapped_trend,
            source="Push_Client",
            raw_metadata={"original_symbol": trend_symbol},
            user_id=self._user_id
        )
        return glucose_obj
