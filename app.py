from flask import Flask, request, jsonify
from src.storage.dynamodb_client import DynamoDBClient
from src.storage.s3_client import S3Client
from src.external.sentiment_service import SentimentService
from src.api.feedback_handler import FeedbackHandler

import json

app = Flask(__name__)

# Initialize services
db = DynamoDBClient()
s3 = S3Client()
sentiment = SentimentService()

# Load tenant config
with open("config/tenant_registry.json") as f:
    data = json.load(f)
    s3.upload_json("tenants/config.json", data)

handler = FeedbackHandler(db, s3, sentiment)


# 🔐 Helper to get API key
def get_api_key():
    return request.headers.get("x-api-key")


# 🚀 POST /api/feedback
@app.route("/api/feedback", methods=["POST"])
def submit_feedback():
    try:
        api_key = get_api_key()
        body = request.json

        result = handler.submit_feedback(
            api_key=api_key,
            customer_name=body.get("customer_name", ""),
            rating=body.get("rating"),
            comment=body.get("comment")
        )

        return jsonify(result), 200

    except Exception as e:
        return jsonify({"error": str(e)}), 400


# 📊 GET /api/insights
@app.route("/api/insights", methods=["GET"])
def get_insights():
    try:
        api_key = get_api_key()

        result = handler.get_restaurant_insights(api_key)

        return jsonify(result), 200

    except Exception as e:
        return jsonify({"error": str(e)}), 400


if __name__ == "__main__":
    app.run(debug=True)