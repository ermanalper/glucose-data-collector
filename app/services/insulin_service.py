import datetime
from typing import Optional

from app.core.exceptions import ResourceNotFoundException
from app.infrastructure.interfaces.glucose_service_interface import IGlucoseService
from app.infrastructure.interfaces.insulin_repository_interface import IInsulinRepository
from app.infrastructure.interfaces.insulin_service_interface import IInsulinService
from app.models.insulin import Insulin
from app.models.insulin_dose import InsulinDose



class InsulinServiceImpl(IInsulinService):
    def __init__(self, insulin_repo: IInsulinRepository, glucose_service: IGlucoseService):
        self._repo = insulin_repo
        self._glucose_service = glucose_service

    def get_insulin_types(self):
        insulin_types = self._repo.get_insulin_types()
        if not insulin_types:
            raise ResourceNotFoundException("There is no insulin type in the system")
        return insulin_types

    def _get_glucose_value_at_time(self, user_id: str, timestamp: datetime) -> Optional[int]:
        start_time = timestamp - datetime.timedelta(minutes=15)
        end_time = timestamp + datetime.timedelta(minutes=15)

        try:
            readings = self._glucose_service.get_glucose_by_time_interval(
                user_id=user_id,
                start=start_time,
                end=end_time
            )

            closest_reading = min(readings, key=lambda r: abs((r.timestamp - timestamp).total_seconds()))
            return closest_reading.value

        except ResourceNotFoundException:
            return None

    def get_insulin_history_by_time_interval(self, start_time: datetime, end_time: datetime, user_id: str):
        history = self._repo.get_insulin_history_by_time_interval(start_time=start_time, end_time=end_time, user_id=user_id)
        if not history:
            raise ResourceNotFoundException("No glucose data found for this time interval'.")
        return history


    def add_new_insulin_type(self, brand: str):
        new_insulin = Insulin(name=brand)
        self._repo.add_insulin(new_insulin)

    def enter_insulin_dose(self, user_id: str, insulin_id: int, dose: float, timestamp: datetime):
        insulin = Insulin(id=insulin_id)
        glucose_value = self._get_glucose_value_at_time(user_id, timestamp)
        dose = InsulinDose(user_id=user_id, insulin_type=insulin, dose=dose, timestamp=timestamp, glucose_value=glucose_value)
        return self._repo.enter_insulin_dose(dose)