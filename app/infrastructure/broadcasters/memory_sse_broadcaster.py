import asyncio
import time
from typing import Set, Tuple, AsyncGenerator, List, Dict
from app.infrastructure.interfaces.sse_broadcaster_interface import ISSEBroadcaster


class MemorySSEBroadcaster(ISSEBroadcaster):
    def __init__(self):
        self._queues: Set[Tuple[asyncio.AbstractEventLoop, asyncio.Queue, str]] = set()
        #last ping times for each client
        self._last_heartbeats: Dict[str, float] = {}

    async def subscribe(self, client_name: str) -> AsyncGenerator[dict, None]:
        loop = asyncio.get_running_loop()
        queue = asyncio.Queue()
        item = (loop, queue, client_name)

        self._queues.add(item)
        self._last_heartbeats[client_name] = time.time()

        try:
            while True:
                yield await queue.get()
        finally:
            self._queues.discard(item)
            self._last_heartbeats.pop(client_name, None)

    def broadcast(self, event_name: str, data: str) -> None:
        for loop, queue, _ in self._queues:
            loop.call_soon_threadsafe(
                queue.put_nowait,
                {"event": event_name, "data": data}
            )

    def heartbeat(self, client_name: str) -> None:
        # update last ping time for each client
        if client_name in self._last_heartbeats:
            self._last_heartbeats[client_name] = time.time()

    def get_active_clients(self) -> List[str]:
        current_time = time.time()
        timeout_seconds = 40.0  # remove all clients from listening's list

        dead_clients = [c for c, t in self._last_heartbeats.items() if current_time - t > timeout_seconds]

        for dead in dead_clients:
            self._last_heartbeats.pop(dead, None)

            items_to_remove = [item for item in self._queues if item[2] == dead]
            for item in items_to_remove:
                self._queues.discard(item)

        return list(self._last_heartbeats.keys())