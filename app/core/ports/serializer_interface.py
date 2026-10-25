from abc import abstractmethod, ABC
from typing import Any


class ISerializer(ABC):
    @abstractmethod
    def serialize(self, obj: Any) -> str:
        pass