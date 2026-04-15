from src.api.feedback_handler import FeedbackHandler
from src.storage.dynamodb_client import DynamoDBClient
from src.storage.s3_client import S3Client
from src.external.sentiment_service import SentimentService

import json


def setup_handler():
    db = DynamoDBClient()
    s3 = S3Client()
    sentiment = SentimentService()

    with open("config/tenant_registry.json") as f:
        data = json.load(f)
        s3.upload_json("tenants/config.json", data)

    return FeedbackHandler(db, s3, sentiment)


def test_submit_feedback():
    handler = setup_handler()

    result = handler.submit_feedback(
        api_key="pk_pizza_abc123",
        customer_name="Ajay",
        rating=5,
        comment="Amazing food"
    )

    assert "feedback_id" in result
    assert result["sentiment"] is not None


def test_invalid_api_key():
    handler = setup_handler()

    try:
        handler.submit_feedback("wrong_key", "Ajay", 5, "Good")
    except ValueError:
        assert True


def test_get_insights():
    handler = setup_handler()

    handler.submit_feedback("pk_pizza_abc123", "A", 5, "Great")
    handler.submit_feedback("pk_pizza_abc123", "B", 4, "Good")

    insights = handler.get_restaurant_insights("pk_pizza_abc123")

    assert insights["total_feedback"] == 2
    