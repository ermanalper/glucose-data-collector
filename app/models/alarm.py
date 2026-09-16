import datetime
from dataclasses import dataclass
from uuid import UUID


@dataclass(slots=True)
class Alarm:
    id: UUID # this is used to reset an active alarm
    user_id: str
    timestamp: datetime
    message: str