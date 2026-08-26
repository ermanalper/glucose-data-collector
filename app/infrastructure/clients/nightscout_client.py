import datetime
import hashlib
import requests
from typing import Optional

from app.core.config import NIGHTSCOUT_DOCKER_URL, settings
from app.infrastructure.interfaces.glucose_provider_interface import IGlucoseProvider
from app.models.glucose import Glucose


class NightscoutClient(IGlucoseProvider):
    def __init__(self):
        print('Creating Nightscout instance')
        self.base_url = NIGHTSCOUT_DOCKER_URL
        self.raw_api_secret = settings.nightscout_docker_api_secret

    def _get_hashed_secret(self) -> str:
        return hashlib.sha1(self.raw_api_secret.encode('utf-8')).hexdigest()

    def fetch_latest_reading(self) -> Optional[Glucose]:
        try:
            headers = {
                "API-SECRET": self._get_hashed_secret()
            }

            response = requests.get(
                self.base_url,
                timeout=10,
                allow_redirects=False,
                verify=False,
                headers=headers
            )

            if response.status_code != 200:
                print(f"DEBUG: Sunucudan {response.status_code} kodu geldi. İçerik: {response.text}")
                return None

            data = response.json()

            if not data or not isinstance(data, list):
                return None

            latest = data[0]

            timestamp_ms = latest.get("date")
            dt_object = datetime.datetime.fromtimestamp(timestamp_ms / 1000.0)

            return Glucose(
                value=latest.get("sgv"),
                timestamp=dt_object,
                trend=latest.get("direction"),
                source="Nightscout",
                raw_metadata={
                    "id": latest.get("_id"),
                    "device": latest.get("device"),
                    "type": latest.get("type"),
                    "utc_offset": latest.get("utcOffset")
                }
            )
        except Exception as e:
            print(f"Nightscout API Hatası: {e}")
            return None