from typing import Optional
from pydexcom import Dexcom, Region


from app.core.config import settings
from app.infrastructure.interfaces.glucose_provider_interface import IGlucoseProvider
from app.models.glucose import Glucose


class DexcomShareClient(IGlucoseProvider):
    def __init__(self):
        # ous=True is required for Europe (including Turkey)
        #print("şifre ", settings.dexcom_password)
        #print("username ", settings.dexcom_email)
        print('Creating DexcomShare instance')
        self._client = Dexcom(password=settings.dexcom_password, username=settings.dexcom_email, region=Region.OUS)

    def fetch_latest_reading(self) -> Optional[Glucose]:
        try:
            bg = self._client.get_current_glucose_reading()

            if not bg:
                return None

            return Glucose(
            value=bg.mg_dl,
            timestamp=bg.datetime,
            trend=bg.trend_arrow,
            source="DexcomShare",
            raw_metadata={
                "mmol_l": bg.mmol_l,
                "trend_integer": bg.trend
            }
        )
        except Exception as e:
            print(f"Dexcom API Error: {e}")
            return None