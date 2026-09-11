from dataclasses import dataclass


@dataclass(slots=True)
class Insulin:
    name: str