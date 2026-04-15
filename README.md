# Multi-Tenant Restaurant Feedback API

## Overview

This project implements a multi-tenant restaurant feedback system where each restaurant (tenant) has isolated data. The system supports feature flags like sentiment analysis and provides insights based on customer feedback.

---

## Features

- Multi-tenant architecture with strict data isolation
- Sentiment analysis (enabled for premium tenants)
- Mock AWS services (DynamoDB, S3)
- Insights generation (average rating, sentiment summary)
- Unit and integration tests

---

## Setup

```bash
python -m venv venv
source venv/bin/activate   # Windows: venv\Scripts\activate
pip install -r requirements.txt
```
