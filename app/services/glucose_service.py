from typing import Optional, AsyncGenerator

import datetime

from app.core.exceptions import ResourceNotFoundException
from app.events.events import timer_ticked_event, new_glucose_data_event
from app.infrastructure.interfaces.glucose_provider_interface import IGlucoseProvider
from app.infrastructure.interfaces.glucose_repository_interface import IGlucoseRepository
from app.infrastructure.interfaces.glucose_service_interface import IGlucoseService
from app.infrastructure.interfaces.sse_broadcaster_interface import ISSEBroadcaster
from app.models.glucose import Glucose

class GlucoseServiceImpl(IGlucoseService):
    def __init__(
            self,
            repo: IGlucoseRepository,
            broadcaster: ISSEBroadcaster,
            provider: IGlucoseProvider
    ):
        self._repo = repo
        self._broadcaster = broadcaster
        self._provider = provider
        timer_ticked_event.connect(self.sync_latest_dexcom_data)

    def subscribe_to_glucose_stream(self) -> AsyncGenerator[dict, None]:
        return self._broadcaster.subscribe()

    def get_first_glucose_entry_date(self, current_user_id):
        first_data_date = self._repo.get_first_entry_date(user_id=current_user_id)
        return first_data_date
    def get_glucose_by_time_interval(self, user_id, start, end) -> list[Glucose]:
        historical_data = self._repo.get_by_time_interval(user_id=user_id, start=start, end=end)
        if not historical_data:
            raise ResourceNotFoundException("No glucose data found for this time interval.")
        return historical_data

    def get_latest_n_readings(self, user_id, n, offset) -> list[Glucose]:
        historical_data = self._repo.get_latest_n(user_id=user_id, n=n, offset=offset)
        if not historical_data:
            raise ResourceNotFoundException("No glucose data found for this user.")
        return historical_data

    def get_latest_glucose(self, user_id: str) -> Optional[Glucose]:
        latest_data = self._repo.get_latest(user_id=user_id)
        if not latest_data:
            raise ResourceNotFoundException("No glucose data found for this user.")
        return latest_data


    # subscribe to event
    def sync_latest_dexcom_data(self, sender, **kwargs):
        print(f"[{datetime.datetime.now()}] Event caught! Fetch data from glucose provider and publish event.")
        latest_data: Glucose = self._provider.fetch_latest_reading()
        if latest_data:
            print(latest_data)
            new_glucose_data_event.send('glucose_service', glucose_data=latest_data) #publish glucose data
        else:
            print("No new data.")

