import datetime
from dataclasses import dataclass, field
from typing import Optional, Any, Dict


@dataclass(slots=True)
class Glucose:
    # These are the common fields between DexcomShare and Nightscout clients.
    # If, in the future, another client is added, these fields might not be common anymore and could be changed.
    value: int
    timestamp: datetime.datetime
    trend: str
    source: str

    # If some data is not common between all clients, so they are client-specific data, they can be stored in this dict
    raw_metadata: Dict[str, Any] = field(default_factory=dict) #for source-specific data