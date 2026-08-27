from abc import abstractmethod, ABC
from typing import Optional

from app.models.glucose import Glucose

#get glucose data and save it in the database
class IGlucoseRepository(ABC):
    @abstractmethod
    def save(self, glucose: Glucose) -> None:
        pass

    @abstractmethod
    def get_latest(self, user_id: str) -> Optional[Glucose]:
        pass