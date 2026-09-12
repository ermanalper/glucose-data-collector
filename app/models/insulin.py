from dataclasses import dataclass


@dataclass(slots=True)
class Insulin:
    id: int | None = None
    name: str = ""