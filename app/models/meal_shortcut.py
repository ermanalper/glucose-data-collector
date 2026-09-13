from dataclasses import dataclass


@dataclass(slots=True)
class MealShortcut:
    user_id: str
    title: str
    desc: str