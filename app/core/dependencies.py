from app.infrastructure.clients.nightscout_client import NightscoutClient
from app.infrastructure.interfaces.glucose_provider_interface import IGlucoseProvider

_glucose_provider_instance = None #singleton instance


def get_glucose_provider() -> IGlucoseProvider:
    global _glucose_provider_instance

    #singleton pattern
    if _glucose_provider_instance is None:
        print("Creating Nightscout instance")
        _glucose_provider_instance = NightscoutClient()

    return _glucose_provider_instance