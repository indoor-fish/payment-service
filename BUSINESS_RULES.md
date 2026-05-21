# Payment Service — Business Rules

## Rule 1: High-Value Payment Review
Payments above **$10,000** require manual fraud review before authorisation. These payments are rejected automatically and require the customer to contact support to proceed.

## Rule 2: Refund Window
Refunds can only be initiated within **30 days of capture**. After 30 days, the payment is final and cannot be reversed through the API.

## Rule 3: Failed Payment Velocity
A single user account cannot have more than **3 failed payment attempts within any 24-hour window**. Exceeding this limit results in all further payment attempts being denied until the window resets. This protects against fraud and card testing attacks.
