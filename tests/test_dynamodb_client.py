#implementation
import pytest
from src.storage.dynamodb_client import DynamoDBClient


def test_save_and_get_feedback():
    db = DynamoDBClient()

    feedback = {"feedback_id": "1", "created_at": "2026"}
    db.save_feedback("tenant1", feedback)

    result = db.get_feedback_by_id("tenant1", "1")
    assert result == feedback


def test_tenant_isolation():
    db = DynamoDBClient()

    db.save_feedback("tenant1", {"feedback_id": "1", "created_at": "2026"})
    db.save_feedback("tenant2", {"feedback_id": "2", "created_at": "2026"})

    assert len(db.list_feedback("tenant1")) == 1
    assert len(db.list_feedback("tenant2")) == 1


def test_list_feedback_limit():
    db = DynamoDBClient()

    for i in range(5):
        db.save_feedback("tenant1", {"feedback_id": str(i), "created_at": str(i)})

    result = db.list_feedback("tenant1", limit=2)
    assert len(result) == 2


def test_invalid_tenant():
    db = DynamoDBClient()

    with pytest.raises(ValueError):
        db.save_feedback("", {})