from app.infrastructure.clients.dexcom_client import DexcomShareClient
from app.infrastructure.clients.nightscout_client import NightscoutClient
from app.infrastructure.interfaces.glucose_provider_interface import IGlucoseProvider

_glucose_provider_instance = None #singleton instance


def get_glucose_provider() -> IGlucoseProvider:
    global _glucose_provider_instance

    #singleton pattern
    if _glucose_provider_instance is None:
        _glucose_provider_instance = NightscoutClient()
       # _glucose_provider_instance = DexcomShareClient()
    return _glucose_provider_instance