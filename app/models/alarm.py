from datetime import datetime, timezone
from dataclasses import dataclass
from uuid import UUID


@dataclass(slots=True)
class Alarm:
    id: UUID | None # this is used to reset an active alarm
    user_id: str
    level : int
    message: str
    timestamp : datetime = datetime.now(timezone.utc)
