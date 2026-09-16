import asyncio
from typing import Set, Tuple, AsyncGenerator
from app.infrastructure.interfaces.sse_broadcaster_interface import ISSEBroadcaster


class MemorySSEBroadcaster(ISSEBroadcaster):
    def __init__(self):
        self._queues: Set[Tuple[asyncio.AbstractEventLoop, asyncio.Queue]] = set()

    async def subscribe(self) -> AsyncGenerator[dict, None]:
        loop = asyncio.get_running_loop()
        queue = asyncio.Queue()
        item = (loop, queue)

        self._queues.add(item)
        try:
            while True:
                yield await queue.get()
        except asyncio.CancelledError:
            self._queues.remove(item)

    def broadcast(self, event_name: str, data: str) -> None:
        for loop, queue in self._queues:
            loop.call_soon_threadsafe(
                queue.put_nowait,
                {"event": event_name, "data": data}
            )