from datetime import datetime, timedelta, timezone
from typing import TYPE_CHECKING

# In-memory store for demo; replace with DB query in production
_failed_payments: list[dict] = []

async def check_velocity(user_id: str) -> bool:
    """
    Returns True if user has exceeded 3 failed payments in the last 24 hours.
    Business Rule: A single user cannot have more than 3 failed payments in a 24-hour window.
    """
    cutoff = datetime.now(timezone.utc) - timedelta(hours=24)
    recent_failures = [
        p for p in _failed_payments
        if p["user_id"] == user_id and p["timestamp"] > cutoff
    ]
    return len(recent_failures) >= 3

async def record_failed_payment(user_id: str) -> None:
    _failed_payments.append({"user_id": user_id, "timestamp": datetime.now(timezone.utc)})

async def requires_manual_review(amount: float) -> bool:
    """
    Business Rule: Payments above $10,000 require manual fraud review before authorisation.
    """
    return amount > 10_000
