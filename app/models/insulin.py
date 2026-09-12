from dataclasses import dataclass


@dataclass(slots=True)
class Insulin:
    user_id: str
    name: str