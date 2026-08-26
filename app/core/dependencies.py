from pathlib import Path

from app.core.config import IS_DEVELOPMENT
from app.infrastructure.clients.dexcom_client import DexcomShareClient
from app.infrastructure.clients.nightscout_client import NightscoutClient
from app.infrastructure.clients.simulation_client import SimulationClient
from app.infrastructure.interfaces.glucose_provider_interface import IGlucoseProvider

_glucose_provider_instance = None #singleton instance


def get_glucose_provider() -> IGlucoseProvider:
    global _glucose_provider_instance

    #singleton pattern
    if _glucose_provider_instance is None:
        if IS_DEVELOPMENT:
            current_dir = Path(__file__).resolve().parent
            mock_file_path = current_dir.parent.parent / "data" / "mock" / "simulation_data.json"
            _glucose_provider_instance = SimulationClient(str(mock_file_path))
        else:
            # if not development, use desired client (uncomment) and delete 'pass'
            # _glucose_provider_instance = NightscoutClient()
            # _glucose_provider_instance = DexcomShareClient()
            pass


    return _glucose_provider_instance