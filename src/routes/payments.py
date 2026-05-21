from fastapi import APIRouter, HTTPException
from src.schemas.payment_schemas import AuthorisePaymentRequest, CapturePaymentRequest, RefundRequest, PaymentResponse
from src.services import payment_service

router = APIRouter()

@router.post("/authorise", response_model=PaymentResponse)
async def authorise(req: AuthorisePaymentRequest):
    try:
        payment = await payment_service.authorise_payment(req.user_id, req.order_id, req.amount, req.currency)
        return PaymentResponse(payment=payment)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.post("/capture", response_model=PaymentResponse)
async def capture(req: CapturePaymentRequest):
    try:
        payment = await payment_service.capture_payment(req.payment_id)
        return PaymentResponse(payment=payment)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.post("/{payment_id}/refund", response_model=PaymentResponse)
async def refund(payment_id: str, req: RefundRequest):
    try:
        payment = await payment_service.refund_payment(payment_id, req.amount, req.reason)
        return PaymentResponse(payment=payment)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
