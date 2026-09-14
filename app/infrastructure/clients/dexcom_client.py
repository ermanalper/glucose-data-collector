from typing import Optional
from pydexcom import Dexcom, Region


from app.core.config import settings
from app.core.exceptions import ClientError
from app.events.events import timer_ticked_event, new_glucose_data_event
from app.infrastructure.interfaces.glucose_provider_interface import IGlucoseProvider
from app.models.glucose import Glucose, TrendState

DEXCOM_TREND_MAP = {
    #these are just examples and never actually tried with Dexcom Share.
    #If Dexcom Share gives different  strings for trend, replace or add them.
    "DoubleUp": TrendState.DOUBLE_UP,
    "SingleUp": TrendState.SINGLE_UP,
    "FortyFiveUp": TrendState.FORTY_FIVE_UP,
    "Flat": TrendState.FLAT,
    "FortyFiveDown": TrendState.FORTY_FIVE_DOWN,
    "SingleDown": TrendState.SINGLE_DOWN,
    "DoubleDown": TrendState.DOUBLE_DOWN,

    "None": TrendState.UNKNOWN,
    "NotComputable": TrendState.UNKNOWN,
    "RateOutOfRange": TrendState.UNKNOWN
}

class DexcomShareClient(IGlucoseProvider):
    def __init__(self, username, password):
        # ous=True is required for Europe (including Turkey)
        print('Creating DexcomShare instance')
        self._client = Dexcom(password=password, username=username, region=Region.OUS)
        timer_ticked_event.connect(self.fetch_latest_reading)

    def fetch_latest_reading(self, sender=None, **kwargs):
        print('DexcomShareClient fetch latest reading')
        try:
            bg = self._client.get_current_glucose_reading()

            if not bg:
                print('No data')
                return None

            mapped_trend = DEXCOM_TREND_MAP.get(bg.trend_direction, TrendState.UNKNOWN)

            glucose_obj = Glucose(
                value=bg.mg_dl,
                timestamp=bg.datetime,
                trend=mapped_trend,
                source="DexcomShare",
                raw_metadata={
                    "mmol_l": bg.mmol_l,
                    "trend_integer": bg.trend
                }
            )

            new_glucose_data_event.send(self, glucose_data=glucose_obj)


        except Exception as e:
            print(f"Dexcom API Error: {e}")
            raise ClientError(f'{e}')