from app.infrastructure.interfaces.insulin_repository_interface import IInsulinRepository
from app.models.insulin import Insulin


class SqlAlchemyInsulinRepository(IInsulinRepository):
    def add_insulin(self, insulin: Insulin):
        pass