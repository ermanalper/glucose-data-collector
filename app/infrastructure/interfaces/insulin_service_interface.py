from abc import ABC, abstractmethod


class IInsulinService(ABC):
    @abstractmethod
    def add_new_insulin_type(self, user_id: str, brand: str):
        pass