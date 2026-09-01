import json
from typing import Any

from app.infrastructure.interfaces.serializer_interface import ISerializer


class JsonSerializer(ISerializer):
    def serialize(self, obj: Any) -> str:
        return json.dumps(obj, default=str)