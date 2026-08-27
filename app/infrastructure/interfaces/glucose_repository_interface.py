from abc import abstractmethod, ABC
from app.models.glucose import Glucose

#get glucose data and save it in the database
class IGlucoseRepository(ABC):
    @abstractmethod
    def save(self, glucose: Glucose) -> None:
        pass