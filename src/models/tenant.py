from dataclasses import dataclass
from typing import Dict


@dataclass
class Tenant:
    tenant_id: str
    restaurant_name: str
    api_key: str
    plan: str
    features: Dict[str, bool]
    created_at: str

    def __post_init__(self):
        if self.plan not in ["basic", "premium"]:
            raise ValueError("plan must be 'basic' or 'premium'")

    @classmethod
    def from_dict(cls, data: dict) -> "Tenant":
        return cls(**data)

    def to_dict(self) -> dict:
        return self.__dict__