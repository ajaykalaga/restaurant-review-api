# Multi-Tenant Restaurant Feedback API

## 📌 Overview

This project implements a multi-tenant restaurant feedback system where multiple restaurants can collect and analyze customer reviews using a shared backend. Each tenant’s data is strictly isolated, and feature flags enable capabilities like sentiment analysis based on subscription plans.

The system simulates AWS services (DynamoDB and S3) using in-memory storage and exposes functionality via a Flask API.

---

## 🚀 Features

- Multi-tenant architecture with strict data isolation  
- Feature flags (sentiment analysis for premium tenants)  
- Mock AWS services (DynamoDB, S3)  
- Sentiment analysis integration (mock external API)  
- Insights generation (average rating, sentiment summary)  
- REST API using Flask  
- Unit and integration tests  

---

## ⚙️ Setup

```bash
python -m venv venv
source venv/bin/activate   # Windows: venv\Scripts\activate
pip install -r requirements.txt
```

---

## ▶️ Run Application

```bash
python app.py
```

---

## 🧪 Run Tests

```bash
pytest tests/ -v --cov=src --cov-report=term-missing
```

---

## 🌐 API Endpoints

### POST /api/feedback

Submit feedback using API key in header.

```bash
curl -X POST http://127.0.0.1:5000/api/feedback \
  -H "Content-Type: application/json" \
  -H "x-api-key: pk_pizza_abc123" \
  -d '{
    "customer_name": "Ajay",
    "rating": 5,
    "comment": "Amazing pizza!"
  }'
```

---

### GET /api/insights

Retrieve restaurant insights.

```bash
curl -X GET http://127.0.0.1:5000/api/insights \
  -H "x-api-key: pk_pizza_abc123"
```

---

## 💻 Example Usage (Without API)

```python
from src.api.feedback_handler import FeedbackHandler
from src.storage.dynamodb_client import DynamoDBClient
from src.storage.s3_client import S3Client
from src.external.sentiment_service import SentimentService

handler = FeedbackHandler(
    DynamoDBClient(),
    S3Client(),
    SentimentService()
)

result = handler.submit_feedback(
    api_key="pk_pizza_abc123",
    customer_name="John Doe",
    rating=5,
    comment="Amazing pizza!"
)

print(result)
```

---

## 🧠 Architecture Decisions

- **Multi-Tenancy:** Tenant isolation is achieved using `tenant_id` as a partition key in storage. Each tenant’s data is stored separately to prevent leakage.  
- **Storage Design:** DynamoDB and S3 are simulated using in-memory data structures for simplicity.  
- **Dependency Injection:** Core services are injected into the handler to improve modularity and testability.  
- **Feature Flags:** Tenant-specific features like sentiment analysis are controlled via configuration.  

---

## ⚖️ Trade-offs

- In-memory storage instead of real AWS (simpler and faster for this assignment)  
- Sentiment analysis is keyword-based (mock implementation)  
- No persistence (data resets when app restarts)  

---

## 📁 Project Structure

```
src/
  api/
  storage/
  external/
  models/
  utils/
tests/
config/
app.py
```

---

## 📌 Notes

This implementation focuses on clean architecture, testability, and demonstrating multi-tenant design patterns rather than production deployment.
