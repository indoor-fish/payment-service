# payment-service

Handles payment authorisation, capture, and refunds. The most business-logic-heavy service in the platform.

## Port: 3002

## API Endpoints
- `POST /payments/authorise` — authorise a payment
- `POST /payments/capture` — capture an authorised payment
- `POST /payments/{id}/refund` — refund a captured payment
- `GET /payments/user/{userId}` — get all payments for a user
- `GET /payments/{id}` — get a specific payment

## Dependencies
- `notification-service` (outbound) — publishes `payment.processed` and `payment.failed` events
- `@indoor-fish/shared-libs` — shared types (PaymentDTO, PaymentStatus)

See `BUSINESS_RULES.md` for payment processing rules.
