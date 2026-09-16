from typing import Optional, AsyncGenerator

from datetime import datetime
import datetime
from app.api.schemas.glucose_schema import PushGlucosePayload
from app.core.exceptions import ResourceNotFoundException, FalseClientException
from app.events.events import timer_ticked_event, new_glucose_data_event
from app.infrastructure.interfaces.glucose.glucose_provider_interface import IGlucoseProvider, IPullClient, IPushClient
from app.infrastructure.interfaces.glucose.glucose_repository_interface import IGlucoseRepository
from app.infrastructure.interfaces.glucose.glucose_service_interface import IGlucoseService
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
        timer_ticked_event.connect(self._handle_timer_tick)

    def get_glucose_value_at_time(self, user_id: str, timestamp: datetime) -> Optional[int]:
        start_time = timestamp - datetime.timedelta(minutes=15)
        end_time = timestamp + datetime.timedelta(minutes=15)

        try:
            readings = self.get_glucose_by_time_interval(
                user_id=user_id,
                start=start_time,
                end=end_time
            )

            closest_reading = min(readings, key=lambda r: abs((r.timestamp - timestamp).total_seconds()))
            return closest_reading.value

        except ResourceNotFoundException:
            return None

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

    def _handle_timer_tick(self, sender=None, **kwargs):
        # Only pull clients work with timer tick
        if isinstance(self._provider, IPullClient):
            glucose_data = self._provider.fetch_latest_reading()
            if glucose_data:
                self._save_and_broadcast(glucose_data)

    def handle_incoming_webhook(self, payload: PushGlucosePayload):
        # Only push clients work with webhook
        if isinstance(self._provider, IPushClient):
            glucose_data = self._provider.process_pushed_data(
                value=payload.value,
                trend_symbol=payload.trend_symbol
            )
            if glucose_data:
                self._save_and_broadcast(glucose_data)
        else:
            raise FalseClientException("Pull clients do not work with webhook")

    def _save_and_broadcast(self, glucose_data: Glucose):
        print(f"[{datetime.datetime.now()}] [SERVICE] New glucose event caught! Pass it to repo and save.")
        self._repo.save(glucose_data)
        new_glucose_data_event.send(self, glucose_data=glucose_data)

