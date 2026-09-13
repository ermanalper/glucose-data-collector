import datetime
from dataclasses import dataclass


@dataclass(slots=True)
class Meal:
    user_id: str
    desc: str #description of the meal. e.g. "A bowl of soup and 100 grams of rice"
    timestamp: datetime
    glucose_value: int #glucose value when the meal is eaten