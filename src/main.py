from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
from src.routes import payments, history

app = FastAPI(title="payment-service", version="1.0.0")
app.include_router(payments.router, prefix="/payments", tags=["payments"])
app.include_router(history.router, prefix="/payments", tags=["history"])

@app.get("/health")
async def health():
    return {"status": "ok", "service": "payment-service"}

@app.exception_handler(Exception)
async def global_exception_handler(_request: Request, exc: Exception):
    return JSONResponse(status_code=500, content={"error": str(exc)})
