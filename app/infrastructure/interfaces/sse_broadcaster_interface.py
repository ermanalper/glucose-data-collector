from abc import ABC, abstractmethod
from typing import AsyncGenerator


class ISSEBroadcaster(ABC):
    @abstractmethod
    async def subscribe(self) -> AsyncGenerator[dict, None]:
        yield {}

    @abstractmethod
    def broadcast(self, event_name: str, data: str) -> None:
        pass