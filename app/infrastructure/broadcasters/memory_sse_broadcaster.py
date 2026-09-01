import asyncio
from typing import Set, AsyncGenerator

from app.infrastructure.interfaces.sse_broadcaster_interface import ISSEBroadcaster


class MemorySSEBroadcaster(ISSEBroadcaster):
    def __init__(self):
        self._queues: Set[asyncio.Queue] = set()

    async def subscribe(self) -> AsyncGenerator[dict, None]:
        queue = asyncio.Queue()
        self._queues.add(queue)
        try:
            while True:
                yield await queue.get()
        except asyncio.CancelledError:
            self._queues.remove(queue)

    def broadcast(self, event_name: str, data: str) -> None:
        for queue in self._queues:
            queue.put_nowait({"event": event_name, "data": data})

