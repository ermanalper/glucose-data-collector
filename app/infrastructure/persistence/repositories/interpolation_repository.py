import os
import json
from datetime import datetime

from app.core.ports.repositories.interpolation_repository_interface import IInterpolationRepository
from app.models.poly_result import PolyResult
from app.core.ports.serializer_interface import ISerializer


class InterpolationRepository(IInterpolationRepository):
    def __init__(self, file_path: str, serializer: ISerializer):
        self._file_path = file_path
        self._serializer = serializer
        self._ensure_file_exists()

    def _ensure_file_exists(self):
        os.makedirs(os.path.dirname(self._file_path), exist_ok=True)
        if not os.path.exists(self._file_path) or os.path.getsize(self._file_path) == 0:
            with open(self._file_path, 'w', encoding='utf-8') as f:
                f.write('[]')

    def save_interpolation(self, poly: PolyResult, timestamp: datetime):
        new_record = {
            "timestamp": timestamp,
            "result": {
                "coefficients": poly.coefficients,
                "degree": poly.degree
            }
        }

        json_content = self._serializer.serialize(new_record)
        with open(self._file_path, 'a', encoding='utf-8') as f:
            f.write(json_content + '\n')