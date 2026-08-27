from pathlib import Path

from app.core.config import IS_DEVELOPMENT, settings, NIGHTSCOUT_DOCKER_URL
from app.infrastructure.clients.dexcom_client import DexcomShareClient
from app.infrastructure.clients.nightscout_client import NightscoutClient
from app.infrastructure.clients.simulation_client import SimulationClient
from app.infrastructure.interfaces.glucose_provider_interface import IGlucoseProvider
from app.infrastructure.interfaces.glucose_repository_interface import IGlucoseRepository
from app.infrastructure.persistence.repositories.glucose_repository import SqlAlchemyGlucoseRepository

_glucose_provider_instance = None # Singleton instance
_glucose_repository_instance = None # Singleton instance

def get_glucose_provider() -> IGlucoseProvider:
    global _glucose_provider_instance
    #singleton pattern
    if _glucose_provider_instance is None:
        if IS_DEVELOPMENT:
            current_dir = Path(__file__).resolve().parent
            mock_file_path = current_dir.parent.parent / "data" / "mock" / "simulation_data.json"
            _glucose_provider_instance = SimulationClient(str(mock_file_path))
           # _glucose_provider_instance = NightscoutClient(base_url=NIGHTSCOUT_DOCKER_URL ,raw_api_secret=settings.nightscout_docker_api_secret)

            print('Development, provider: ', _glucose_provider_instance)
        else:
            # if not development, use desired client (uncomment) and delete 'pass'
            #_glucose_provider_instance = NightscoutClient(base_url=NIGHTSCOUT_DOCKER_URL ,raw_api_secret=settings.nightscout_docker_api_secret)
            #_glucose_provider_instance = DexcomShareClient(username=settings.dexcom_email, password=settings.dexcom_password)
            pass


    return _glucose_provider_instance

def get_glucose_repository() -> IGlucoseRepository:
    global _glucose_repository_instance
    if _glucose_repository_instance is None:
        _glucose_repository_instance = SqlAlchemyGlucoseRepository()

    return _glucose_repository_instance