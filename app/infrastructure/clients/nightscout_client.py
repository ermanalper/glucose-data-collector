import datetime
import hashlib
import requests
from typing import Optional

from app.core.config import NIGHTSCOUT_DOCKER_URL, settings
from app.core.exceptions import ClientError
from app.events.events import timer_ticked_event, new_glucose_data_event
from app.infrastructure.interfaces.glucose_provider_interface import IGlucoseProvider
from app.models.glucose import Glucose, TrendState

NIGHTSCOUT_TREND_MAP = {
    "DoubleUp": TrendState.DOUBLE_UP,
    "SingleUp": TrendState.SINGLE_UP,
    "FortyFiveUp": TrendState.FORTY_FIVE_UP,
    "Flat": TrendState.FLAT,
    "FortyFiveDown": TrendState.FORTY_FIVE_DOWN,
    "SingleDown": TrendState.SINGLE_DOWN,
    "DoubleDown": TrendState.DOUBLE_DOWN,
    "NONE": TrendState.UNKNOWN,
    "NOT COMPUTABLE": TrendState.UNKNOWN,
    "RATE OUT OF RANGE": TrendState.UNKNOWN
}

class NightscoutClient(IGlucoseProvider):
    def __init__(self, base_url, raw_api_secret):
        print('Creating Nightscout instance')
        self._base_url = NIGHTSCOUT_DOCKER_URL
        self._raw_api_secret = settings.nightscout_docker_api_secret
        timer_ticked_event.connect(self.fetch_latest_reading)


    def _get_hashed_secret(self) -> str:
        return hashlib.sha1(self._raw_api_secret.encode('utf-8')).hexdigest()

    def fetch_latest_reading(self, sender=None, **kwargs):
        try:
            headers = {
                "API-SECRET": self._get_hashed_secret()
            }

            response = requests.get(
                self._base_url,
                timeout=10,
                allow_redirects=False,
                verify=False,
                headers=headers
            )

            if response.status_code != 200:
                print(f"DEBUG: Server Response: {response.status_code}  {response.text}")
                return None

            data = response.json()

            if not data or not isinstance(data, list):
                print('No data')
                return None

            latest = data[0]

            timestamp_ms = latest.get("date")
            dt_object = datetime.datetime.fromtimestamp(timestamp_ms / 1000.0)

            mapped_trend = NIGHTSCOUT_TREND_MAP.get(latest.get("direction"), TrendState.UNKNOWN)

            glucose_obj = Glucose(
                value=latest.get("sgv"),
                timestamp=dt_object,
                trend=mapped_trend,
                source="Nightscout",
                raw_metadata={
                    "id": latest.get("_id"),
                    "device": latest.get("device"),
                    "type": latest.get("type"),
                    "utc_offset": latest.get("utcOffset")
                }
            )
            new_glucose_data_event.send(self, glucose_data=glucose_obj)
        except Exception as e:
            print(f"Nightscout API Error: {e}")
            raise ClientError(f'{e}')