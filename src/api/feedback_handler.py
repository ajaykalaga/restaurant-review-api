#implementation
import json
from typing import Optional

from src.models.tenant import Tenant
from src.models.feedback import Feedback


class FeedbackHandler:
    def __init__(self, db_client, s3_client, sentiment_service):
        self.db_client = db_client
        self.s3_client = s3_client
        self.sentiment_service = sentiment_service
        self._tenant_cache = {}

    # 🔑 Load tenant from API key
    def load_tenant_by_api_key(self, api_key: str) -> Optional[Tenant]:
        if not api_key:
            return None

        # Simple cache
        if api_key in self._tenant_cache:
            return self._tenant_cache[api_key]

        data = self.s3_client.download_json("tenants/config.json")
        if not data:
            return None

        for t in data.get("tenants", []):
            if t["api_key"] == api_key:
                tenant = Tenant.from_dict(t)
                self._tenant_cache[api_key] = tenant
                return tenant

        return None

    # 🚀 Submit feedback
    def submit_feedback(self, api_key: str, customer_name: str, rating: int, comment: str) -> dict:
        tenant = self.load_tenant_by_api_key(api_key)
        if not tenant:
            raise ValueError("Invalid API key")

        if not (1 <= rating <= 5):
            raise ValueError("Rating must be between 1 and 5")

        if not comment:
            raise ValueError("Comment cannot be empty")

        sentiment = None

        # Feature flag check
        if tenant.features.get("sentiment_analysis"):
            try:
                sentiment = self.sentiment_service.analyze_sentiment(comment)
            except Exception:
                sentiment = None  # graceful fallback

        feedback = Feedback(
            tenant_id=tenant.tenant_id,
            customer_name=customer_name,
            rating=rating,
            comment=comment,
            sentiment_score=sentiment["score"] if sentiment else None,
            sentiment_label=sentiment["label"] if sentiment else None
        )

        self.db_client.save_feedback(tenant.tenant_id, feedback.to_dict())

        return {
            "feedback_id": feedback.feedback_id,
            "tenant_id": tenant.tenant_id,
            "rating": rating,
            "sentiment": sentiment,
            "created_at": feedback.created_at,
            "message": "Thank you for your feedback!"
        }

    # 📊 Insights
    def get_restaurant_insights(self, api_key: str) -> dict:
        tenant = self.load_tenant_by_api_key(api_key)
        if not tenant:
            raise ValueError("Invalid API key")

        feedbacks = self.db_client.list_feedback(tenant.tenant_id)

        total = len(feedbacks)

        avg_rating = round(
            sum(f["rating"] for f in feedbacks) / total, 2
        ) if total else 0

        # rating distribution
        distribution = {"1": 0, "2": 0, "3": 0, "4": 0, "5": 0}
        for f in feedbacks:
            distribution[str(f["rating"])] += 1

        # sentiment summary
        sentiment_data = [f for f in feedbacks if f.get("sentiment_score") is not None]

        sentiment_summary = None
        if sentiment_data:
            avg_score = round(
                sum(f["sentiment_score"] for f in sentiment_data) / len(sentiment_data), 2
            )

            sentiment_summary = {
                "average_score": avg_score,
                "positive_count": sum(1 for f in sentiment_data if f["sentiment_label"] == "positive"),
                "neutral_count": sum(1 for f in sentiment_data if f["sentiment_label"] == "neutral"),
                "negative_count": sum(1 for f in sentiment_data if f["sentiment_label"] == "negative"),
            }

        return {
            "tenant_id": tenant.tenant_id,
            "restaurant_name": tenant.restaurant_name,
            "total_feedback": total,
            "average_rating": avg_rating,
            "rating_distribution": distribution,
            "sentiment_summary": sentiment_summary,
            "recent_feedback": feedbacks[:5]
        }
    print("Logging enabled")