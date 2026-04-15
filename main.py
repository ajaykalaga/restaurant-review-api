from src.storage.dynamodb_client import DynamoDBClient
from src.storage.s3_client import S3Client
from src.external.sentiment_service import SentimentService
from src.api.feedback_handler import FeedbackHandler

import json

# Initialize services
db = DynamoDBClient()
s3 = S3Client()
sentiment = SentimentService()

# Load tenant config into S3 (simulate AWS)
with open("config/tenant_registry.json") as f:
    data = json.load(f)
    s3.upload_json("tenants/config.json", data)

# Create handler
handler = FeedbackHandler(db, s3, sentiment)

# Test submit feedback
response = handler.submit_feedback(
    api_key="pk_pizza_abc123",
    customer_name="Ajay",
    rating=5,
    comment="Amazing pizza and great service!"
)

print("Submit Feedback Response:")
print(response)

# Test insights
insights = handler.get_restaurant_insights("pk_pizza_abc123")

print("\nInsights:")
print(insights)