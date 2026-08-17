from dataclasses import dataclass
from typing import Optional

@dataclass(slots=True)
class Glucose:
    id: str
    sgv: int
    date: int
    date_string: str
    trend: int
    direction: str
    device: str
    type: str
    utc_offset: Optional[int] = None
    sys_time: Optional[str] = None