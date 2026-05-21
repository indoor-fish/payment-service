import uuid
from datetime import datetime, timedelta, timezone
from src.schemas.payment_schemas import PaymentDTO, PaymentStatus
from src.services.fraud_detection import check_velocity, record_failed_payment, requires_manual_review
from src.events.payment_events import publish_payment_processed, publish_payment_failed

# In-memory store; replace with SQLAlchemy in production
_payments: dict[str, dict] = {}

async def authorise_payment(user_id: str, order_id: str, amount: float, currency: str = "USD") -> PaymentDTO:
    # Business Rule: A single user cannot have more than 3 failed payments in a 24-hour window
    if await check_velocity(user_id):
        raise ValueError(f"Payment denied: user {user_id} has exceeded the failed payment limit in the last 24 hours")

    # Business Rule: Payments above $10,000 require manual fraud review before authorisation
    if await requires_manual_review(amount):
        raise ValueError(f"Payment of ${amount:.2f} requires manual fraud review. Please contact support.")

    payment_id = str(uuid.uuid4())
    now = datetime.now(timezone.utc)
    payment = {
        "id": payment_id,
        "user_id": user_id,
        "order_id": order_id,
        "amount": amount,
        "currency": currency,
        "status": PaymentStatus.AUTHORISED,
        "created_at": now,
        "captured_at": None,
    }
    _payments[payment_id] = payment
    return PaymentDTO(**payment)

async def capture_payment(payment_id: str) -> PaymentDTO:
    payment = _payments.get(payment_id)
    if not payment:
        raise ValueError(f"Payment {payment_id} not found")
    if payment["status"] != PaymentStatus.AUTHORISED:
        raise ValueError(f"Payment must be AUTHORISED before capture, current status: {payment['status']}")
    payment["status"] = PaymentStatus.CAPTURED
    payment["captured_at"] = datetime.now(timezone.utc)
    await publish_payment_processed(payment["user_id"], payment_id, payment["amount"])
    return PaymentDTO(**payment)

async def refund_payment(payment_id: str, amount: float, reason: str) -> PaymentDTO:
    payment = _payments.get(payment_id)
    if not payment:
        raise ValueError(f"Payment {payment_id} not found")
    if payment["status"] != PaymentStatus.CAPTURED:
        raise ValueError("Only CAPTURED payments can be refunded")

    # Business Rule: Refunds can only be initiated within 30 days of capture
    captured_at = payment.get("captured_at")
    if not captured_at or datetime.now(timezone.utc) > captured_at + timedelta(days=30):
        raise ValueError("Refunds must be initiated within 30 days of capture")

    if amount > payment["amount"]:
        raise ValueError("Refund amount cannot exceed original payment amount")

    payment["status"] = PaymentStatus.REFUNDED
    return PaymentDTO(**payment)

async def get_payment(payment_id: str) -> PaymentDTO:
    payment = _payments.get(payment_id)
    if not payment:
        raise ValueError(f"Payment {payment_id} not found")
    return PaymentDTO(**payment)

async def get_user_payments(user_id: str) -> list[PaymentDTO]:
    return [PaymentDTO(**p) for p in _payments.values() if p["user_id"] == user_id]
