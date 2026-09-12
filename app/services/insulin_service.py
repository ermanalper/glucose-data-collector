from app.infrastructure.interfaces.insulin_repository_interface import IInsulinRepository
from app.infrastructure.interfaces.insulin_service_interface import IInsulinService
from app.models.insulin import Insulin


class InsulinServiceImpl(IInsulinService):
    def __init__(self, insulin_repo: IInsulinRepository):
        self._repo = insulin_repo


    def add_new_insulin_type(self, user_id: str, brand: str):
        new_insulin = Insulin(user_id, brand)
        self._repo.add_insulin(new_insulin)