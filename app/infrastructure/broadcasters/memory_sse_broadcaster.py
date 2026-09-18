import asyncio
from typing import Set, Tuple, AsyncGenerator, List
from app.infrastructure.interfaces.sse_broadcaster_interface import ISSEBroadcaster


class MemorySSEBroadcaster(ISSEBroadcaster):
    def __init__(self):
        self._queues: Set[Tuple[asyncio.AbstractEventLoop, asyncio.Queue, str]] = set()

    async def subscribe(self, client_name: str) -> AsyncGenerator[dict, None]:
        loop = asyncio.get_running_loop()
        queue = asyncio.Queue()
        item = (loop, queue, client_name)

        self._queues.add(item)
        try:
            while True:
                yield await queue.get()
        finally:
            self._queues.discard(item)
            print(f"[{client_name}] Left the tunnel. Listening clients: {len(self._queues)}")

    def broadcast(self, event_name: str, data: str) -> None:
        for loop, queue, _ in self._queues:
            loop.call_soon_threadsafe(
                queue.put_nowait,
                {"event": event_name, "data": data}
            )

    def get_active_clients(self) -> List[str]:
        return [client_name for _, _, client_name in self._queues]