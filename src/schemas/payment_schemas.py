from pydantic import BaseModel, Field
from enum import Enum
from datetime import datetime
from typing import Optional
import uuid

class PaymentStatus(str, Enum):
    PENDING = "PENDING"
    AUTHORISED = "AUTHORISED"
    CAPTURED = "CAPTURED"
    REFUNDED = "REFUNDED"
    FAILED = "FAILED"

class AuthorisePaymentRequest(BaseModel):
    user_id: str
    order_id: str
    amount: float = Field(gt=0)
    currency: str = "USD"

class CapturePaymentRequest(BaseModel):
    payment_id: str

class RefundRequest(BaseModel):
    amount: float = Field(gt=0)
    reason: str

class PaymentDTO(BaseModel):
    id: str
    user_id: str
    order_id: str
    amount: float
    currency: str
    status: PaymentStatus
    created_at: datetime
    captured_at: Optional[datetime] = None

class PaymentResponse(BaseModel):
    payment: PaymentDTO
