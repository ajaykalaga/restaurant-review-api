import random


class SentimentService:
    def __init__(self, api_key: str | None = None):
        self.api_key = api_key

    def analyze_sentiment(self, text: str) -> dict:
        if not text:
            raise ValueError("Text cannot be empty")

        positive_words = ["great", "excellent", "amazing", "love", "best", "wonderful", "delicious"]
        negative_words = ["bad", "terrible", "awful", "hate", "worst", "disgusting", "never"]

        text_lower = text.lower()

        positive_count = sum(1 for word in positive_words if word in text_lower)
        negative_count = sum(1 for word in negative_words if word in text_lower)

        # Simulate 1% failure
        if random.random() < 0.01:
            raise Exception("Sentiment API temporarily unavailable")

        if positive_count > negative_count:
            score = min(0.9, 0.3 + (positive_count * 0.2))
            label = "positive"
        elif negative_count > positive_count:
            score = max(-0.9, -0.3 - (negative_count * 0.2))
            label = "negative"
        else:
            score = 0.0
            label = "neutral"

        return {
            "score": round(score, 2),
            "label": label,
            "confidence": 0.85
        }