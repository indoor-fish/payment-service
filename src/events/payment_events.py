import httpx
import os

NOTIFICATION_SERVICE_URL = os.getenv("NOTIFICATION_SERVICE_URL", "http://localhost:3005")

async def publish_payment_processed(user_id: str, payment_id: str, amount: float) -> None:
    payload = {
        "userId": user_id,
        "topic": "payment.processed",
        "channel": "EMAIL",
        "data": {"paymentId": payment_id, "amount": amount},
    }
    try:
        async with httpx.AsyncClient() as client:
            await client.post(
                f"{NOTIFICATION_SERVICE_URL}/internal/notify",
                json=payload,
                headers={"X-Internal-Service": "payment-service"},
                timeout=5.0,
            )
    except Exception as e:
        print(f"[payment_events] Failed to publish payment.processed: {e}")

async def publish_payment_failed(user_id: str, payment_id: str, reason: str) -> None:
    payload = {
        "userId": user_id,
        "topic": "payment.failed",
        "channel": "EMAIL",
        "data": {"paymentId": payment_id, "reason": reason},
    }
    try:
        async with httpx.AsyncClient() as client:
            await client.post(
                f"{NOTIFICATION_SERVICE_URL}/internal/notify",
                json=payload,
                headers={"X-Internal-Service": "payment-service"},
                timeout=5.0,
            )
    except Exception as e:
        print(f"[payment_events] Failed to publish payment.failed: {e}")
