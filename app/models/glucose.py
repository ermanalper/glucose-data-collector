import datetime
from dataclasses import dataclass, field
from enum import Enum
from typing import Any, Dict

from app.core.exceptions import UnknownTrendError

NORMAL_LOWER = 120
NORMAL_UPPER = 240
WARNING_LOWER = 100
WARNING_UPPER = 280


class TrendState(str, Enum):
    DOUBLE_UP = "DOUBLE_UP"
    SINGLE_UP = "SINGLE_UP"
    FORTY_FIVE_UP = "FORTY_FIVE_UP"
    FLAT = "FLAT"
    FORTY_FIVE_DOWN = "FORTY_FIVE_DOWN"
    SINGLE_DOWN = "SINGLE_DOWN"
    DOUBLE_DOWN = "DOUBLE_DOWN"
    UNKNOWN = "UNKNOWN"

class GlucoseStatus(str, Enum):
    NORMAL = "NORMAL"
    WARNING = "WARNING"
    CRITICAL = "CRITICAL"

@dataclass(slots=True)
class Glucose:
    # These are the common fields between DexcomShare and Nightscout clients.
    # If, in the future, another client is added, these fields might not be common anymore and could be changed.
    value: int
    timestamp: datetime.datetime
    trend: TrendState
    source: str
    # If some data is not common between all clients, so they are client-specific data, they can be stored in this dict
    raw_metadata: Dict[str, Any] = field(default_factory=dict) #for source-specific data

    status: GlucoseStatus = field(init=False)

    def __post_init__(self):
        self.status = self._calculate_status()

    def _calculate_status(self) -> GlucoseStatus:
        if (NORMAL_LOWER <= self.value <= NORMAL_UPPER
                and self.trend in (TrendState.DOUBLE_DOWN, TrendState.DOUBLE_UP)):
            return GlucoseStatus.WARNING

        est = self.value
        match self.trend:
            case TrendState.DOUBLE_UP:
                est += 30
            case TrendState.SINGLE_UP:
                est += 10
            case TrendState.FORTY_FIVE_UP:
                est += 5
            case TrendState.FLAT:
                pass
            case TrendState.FORTY_FIVE_DOWN:
                est -= 5
            case TrendState.SINGLE_DOWN:
                est -= 10
            case TrendState.DOUBLE_DOWN:
                est -= 30
            case _:
                raise UnknownTrendError(message=f"Unknown trend: {self.trend}")

        if NORMAL_LOWER <= est <= NORMAL_UPPER:
            return GlucoseStatus.NORMAL
        elif WARNING_LOWER <= est < NORMAL_LOWER or NORMAL_UPPER < est <= WARNING_UPPER:
            return GlucoseStatus.WARNING
        return GlucoseStatus.CRITICAL



