from abc import abstractmethod, ABC
from typing import Optional

from app.models.glucose import Glucose


class IGlucoseProvider(ABC):
    @abstractmethod
    def fetch_latest_reading(self) -> Optional[Glucose]:
        pass