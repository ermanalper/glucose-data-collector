from fastapi import APIRouter, Depends, Request, Query
from sse_starlette.sse import EventSourceResponse

from app.core.dependencies import get_sse_broadcaster
from app.infrastructure.interfaces.sse_broadcaster_interface import ISSEBroadcaster

router = APIRouter(prefix="/api/v1/events", tags=["SSE Stream"])

@router.get("/stream", description="Global event tunnel to frontends (Glucose, Alarms, etc.)")
async def stream_events(
    request: Request,
    client_name: str = Query("Unknown Client", description="Name for the client that listens to this client"),
    broadcaster: ISSEBroadcaster = Depends(get_sse_broadcaster)
):
    headers = {
        "X-Accel-Buffering": "no",
        "Cache-Control": "no-cache",
        "Connection": "keep-alive"
    }

    return EventSourceResponse(
        broadcaster.subscribe(client_name=client_name),
        headers=headers
    )

@router.get("/clients", description="Lists all the clients that are currently listening to the SSE stream")
async def get_active_clients(broadcaster: ISSEBroadcaster = Depends(get_sse_broadcaster)):
    return {
        "active_clients_count": len(broadcaster.get_active_clients()),
        "clients": broadcaster.get_active_clients()
    }