from datetime import datetime, timezone
import json

from app.infrastructure.interfaces.glucose_provider_interface import IGlucoseProvider, IPullClient
from app.models.glucose import Glucose, TrendState

"""
THIS IS NOT A REAL CLIENT,
BUT IT SIMULATES THE DATA THAT COMES FROM THE GLUCOSE PROVIDER WHEN A
PUBLISHER ACCOUNT IS LINKED.
THIS FAKE CLIENT USES THE DATA HARDCODED IN ./data/mock/simulation_data.json
"""

SIMULATION_TREND_MAP = {
    "DOUBLE_UP": TrendState.DOUBLE_UP,
    "SINGLE_UP": TrendState.SINGLE_UP,
    "FORTY_FIVE_UP": TrendState.FORTY_FIVE_UP,
    "FLAT": TrendState.FLAT,
    "FORTY_FIVE_DOWN": TrendState.FORTY_FIVE_DOWN,
    "SINGLE_DOWN": TrendState.SINGLE_DOWN,
    "DOUBLE_DOWN": TrendState.DOUBLE_DOWN,
}

class SimulationClient(IPullClient):
    def __init__(self, file_path: str, user_id:str="default_user"):
        self._file_path = file_path
        self._current_index = 0
        self._mock_data = self._load_data()
        self._user_id = user_id


    def _load_data(self) -> list:
        with open(self._file_path, 'r', encoding='utf-8') as f:
            return json.load(f)

    def fetch_latest_reading(self, sender=None, **kwargs):
        if self._current_index >= len(self._mock_data):
            self._current_index = 0

        raw_item = self._mock_data[self._current_index]
        self._current_index += 1

        dt_object = datetime.now(timezone.utc)
        mapped_trend = SIMULATION_TREND_MAP.get(raw_item["trend"], TrendState.UNKNOWN)
        glucose_obj = Glucose(
            value=raw_item["value"],
            timestamp=dt_object,
            trend=mapped_trend,
            source=raw_item["source"],
            raw_metadata={"simulated_index": self._current_index},
            user_id = self._user_id
        )
        return glucose_obj