from fastapi import APIRouter, Depends, Request
from sse_starlette.sse import EventSourceResponse

from app.core.dependencies import get_sse_broadcaster
from app.infrastructure.interfaces.sse_broadcaster_interface import ISSEBroadcaster

router = APIRouter(prefix="/api/v1/events", tags=["SSE Stream"])

@router.get("/stream", description="Global event tunnel to frontends (Glucose, Alarms, etc.)")
async def stream_events(
    request: Request,
    broadcaster: ISSEBroadcaster = Depends(get_sse_broadcaster)
):
    headers = {
        "X-Accel-Buffering": "no",
        "Cache-Control": "no-cache",
        "Connection": "keep-alive"
    }

    return EventSourceResponse(
        broadcaster.subscribe(),
        headers=headers
    )