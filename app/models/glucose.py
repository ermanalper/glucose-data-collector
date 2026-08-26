import datetime
from dataclasses import dataclass, field
from enum import Enum
from typing import Optional, Any, Dict

class TrendState(Enum):
    DOUBLE_UP = "DOUBLE_UP"
    SINGLE_UP = "SINGLE_UP"
    FORTY_FIVE_UP = "FORTY_FIVE_UP"
    FLAT = "FLAT"
    FORTY_FIVE_DOWN = "FORTY_FIVE_DOWN"
    SINGLE_DOWN = "SINGLE_DOWN"
    DOUBLE_DOWN = "DOUBLE_DOWN"
    UNKNOWN = "UNKNOWN"

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

