from fastapi import APIRouter, HTTPException
from src.services import payment_service

router = APIRouter()

@router.get("/user/{user_id}")
async def get_user_payments(user_id: str):
    payments = await payment_service.get_user_payments(user_id)
    return {"payments": payments}

@router.get("/{payment_id}")
async def get_payment(payment_id: str):
    try:
        payment = await payment_service.get_payment(payment_id)
        return {"payment": payment}
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))
