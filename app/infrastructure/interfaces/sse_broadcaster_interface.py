from abc import ABC, abstractmethod
from typing import AsyncGenerator, List


class ISSEBroadcaster(ABC):
    @abstractmethod
    async def subscribe(self, client_name: str) -> AsyncGenerator[dict, None]:
        yield {}

    @abstractmethod
    def broadcast(self, event_name: str, data: str) -> None:
        pass

    @abstractmethod
    def get_active_clients(self) -> List[str]:
        pass