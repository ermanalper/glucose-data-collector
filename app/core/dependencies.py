from pathlib import Path

from fastapi import Depends

from app.core.config import IS_DEVELOPMENT, settings, NIGHTSCOUT_DOCKER_URL
from app.infrastructure.broadcasters.memory_sse_broadcaster import MemorySSEBroadcaster
from app.infrastructure.clients.dexcom_client import DexcomShareClient
from app.infrastructure.clients.nightscout_client import NightscoutClient
from app.infrastructure.clients.push_client import PushClient
from app.infrastructure.clients.simulation_client import SimulationClient
from app.infrastructure.interfaces.glucose_provider_interface import IGlucoseProvider
from app.infrastructure.interfaces.glucose_repository_interface import IGlucoseRepository
from app.infrastructure.interfaces.glucose_service_interface import IGlucoseService
from app.infrastructure.interfaces.insulin_repository_interface import IInsulinRepository
from app.infrastructure.interfaces.insulin_service_interface import IInsulinService
from app.infrastructure.interfaces.meal_repository_interface import IMealRepository
from app.infrastructure.interfaces.meal_service_interface import IMealService
from app.infrastructure.interfaces.serializer_interface import ISerializer
from app.infrastructure.interfaces.sse_broadcaster_interface import ISSEBroadcaster
from app.infrastructure.persistence.repositories.glucose_repository import SqlAlchemyGlucoseRepository
from app.infrastructure.persistence.repositories.insulin_repository import SqlAlchemyInsulinRepository
from app.infrastructure.persistence.repositories.meal_repository import MealRepositoryImpl
from app.infrastructure.serializers.json_serializer import JsonSerializer
from app.services.glucose_service import GlucoseServiceImpl
from app.services.insulin_service import InsulinServiceImpl
from app.services.meal_service import MealServiceImpl

_glucose_provider_instance = None # Singleton instance
_glucose_repository_instance = None # Singleton instance
_sse_broadcaster_instance = None
_serializer_instance = None
_insulin_repository_instance = None
_glucose_service_instance = None
_insulin_service_instance = None
_meal_service_instance = None
_meal_repository_instance = None

def get_glucose_provider() -> IGlucoseProvider:
    global _glucose_provider_instance
    #singleton pattern
    if _glucose_provider_instance is None:
        if IS_DEVELOPMENT:
            current_dir = Path(__file__).resolve().parent
            mock_file_path = current_dir.parent.parent / "data" / "mock" / "simulation_data.json"
            _glucose_provider_instance = PushClient()
           # _glucose_provider_instance = SimulationClient(str(mock_file_path))
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

def get_current_user_id() -> str:
    # This is a self-hosted backend that has single user support.
    # The reason is, when the user enters their credentials (e.g. username and password)
    # in the frontend, we cannot hash and secure it, but we must pass them directly to this
    # backend as plain text, because the backend uses the credentials to log in to
    # Dexcom Share or Nightscout (or some other client).
    # Hence, the current user service is not essential, but it is a good thing to do
    # to help possible further development
    return "default_user"

def get_sse_broadcaster() -> ISSEBroadcaster:
    global _sse_broadcaster_instance
    if _sse_broadcaster_instance is None:
        _sse_broadcaster_instance = MemorySSEBroadcaster()
    return _sse_broadcaster_instance

def get_serializer() -> ISerializer:
    global _serializer_instance
    if _serializer_instance is None:
        _serializer_instance = JsonSerializer()
    return _serializer_instance

def get_insulin_repository() -> IInsulinRepository:
    global _insulin_repository_instance
    if _insulin_repository_instance is None:
        _insulin_repository_instance = SqlAlchemyInsulinRepository()
    return _insulin_repository_instance

def get_glucose_service() -> IGlucoseService:
    global _glucose_service_instance
    if _glucose_service_instance is None:
        _glucose_service_instance = GlucoseServiceImpl(
            repo=get_glucose_repository(),
            broadcaster=get_sse_broadcaster(),
            provider=get_glucose_provider()
        )

    return _glucose_service_instance

def get_insulin_service() -> IInsulinService:
    global _insulin_service_instance
    if _insulin_service_instance is None:
        _insulin_service_instance = InsulinServiceImpl(
            insulin_repo=get_insulin_repository(),
            glucose_service=get_glucose_service())
    return _insulin_service_instance

def get_meal_repository() -> IMealRepository:
    global _meal_repository_instance
    if _meal_repository_instance is None:
        _meal_repository_instance = MealRepositoryImpl()
    return _meal_repository_instance

def get_meal_service() -> IMealService:
    global _meal_service_instance
    if _meal_service_instance is None:
        _meal_service_instance = MealServiceImpl(
            repo=get_meal_repository(),
            glucose_service=get_glucose_service()
        )
    return _meal_service_instance