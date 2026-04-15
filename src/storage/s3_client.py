import json
from typing import Dict, Optional, List


class S3Client:
    def __init__(self):
        self._storage: Dict[str, str] = {}

    def upload_json(self, key: str, data: dict) -> None:
        try:
            self._storage[key] = json.dumps(data)
        except Exception:
            raise ValueError("Invalid JSON data")

    def download_json(self, key: str) -> Optional[dict]:
        data = self._storage.get(key)
        if not data:
            return None
        return json.loads(data)

    def list_keys(self, prefix: str) -> List[str]:
        return [k for k in self._storage if k.startswith(prefix)]