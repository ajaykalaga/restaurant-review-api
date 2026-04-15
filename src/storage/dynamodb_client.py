from typing import Dict, List, Optional


class DynamoDBClient:
    def __init__(self):
        self._storage: Dict[str, List[dict]] = {}

    def save_feedback(self, tenant_id: str, feedback: dict) -> None:
        if not tenant_id:
            raise ValueError("tenant_id cannot be empty")

        self._storage.setdefault(tenant_id, []).append(feedback)

    def get_feedback_by_id(self, tenant_id: str, feedback_id: str) -> Optional[dict]:
        for item in self._storage.get(tenant_id, []):
            if item["feedback_id"] == feedback_id:
                return item
        return None

    def list_feedback(self, tenant_id: str, limit: int = 100) -> List[dict]:
        data = self._storage.get(tenant_id, [])
        sorted_data = sorted(data, key=lambda x: x["created_at"], reverse=True)
        return sorted_data[:limit]

    def get_feedback_count(self, tenant_id: str) -> int:
        return len(self._storage.get(tenant_id, []))

    def delete_all_feedback(self, tenant_id: str) -> int:
        count = len(self._storage.get(tenant_id, []))
        self._storage[tenant_id] = []
        return count