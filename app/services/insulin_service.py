import datetime

from app.api.schemas.insulin_dose_schema import InsulinDoseResponse
from app.infrastructure.interfaces.insulin_repository_interface import IInsulinRepository
from app.infrastructure.interfaces.insulin_service_interface import IInsulinService
from app.models.insulin import Insulin
from app.models.insulin_dose import InsulinDose


class InsulinServiceImpl(IInsulinService):
    def __init__(self, insulin_repo: IInsulinRepository):
        self._repo = insulin_repo


    def add_new_insulin_type(self, brand: str):
        new_insulin = Insulin(name=brand)
        self._repo.add_insulin(new_insulin)

    def enter_insulin_dose(self, user_id: str, insulin_id: int, dose: float, timestamp: datetime) -> InsulinDoseResponse:
        insulin = Insulin(id=insulin_id)
        dose = InsulinDose(user_id=user_id, insulin_type=insulin, dose=dose, timestamp=timestamp)
        return self._repo.enter_insulin_dose(dose)