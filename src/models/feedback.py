import uuid
from datetime import datetime, UTC
from dataclasses import dataclass, field
from typing import Optional


@dataclass
class Feedback:
    tenant_id: str
    rating: int
    comment: str
    customer_name: str = ""

    feedback_id: str = field(default_factory=lambda: str(uuid.uuid4()))
    sentiment_score: Optional[float] = None
    sentiment_label: Optional[str] = None
    created_at: str = field(default_factory=lambda: datetime.now(UTC).isoformat())

    def __post_init__(self):
        if not (1 <= self.rating <= 5):
            raise ValueError("rating must be between 1 and 5")

        if not self.comment:
            raise ValueError("comment cannot be empty")

    def to_dict(self) -> dict:
        return self.__dict__