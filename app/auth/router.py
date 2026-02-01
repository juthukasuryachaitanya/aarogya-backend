from fastapi import APIRouter, Depends, HTTPException, Request
from pydantic import BaseModel

from app.core.security import create_access_token
from app.core.rate_limit import limiter

router = APIRouter(prefix="/auth", tags=["Auth"])

# =========================
# SCHEMAS
# =========================
class LoginRequest(BaseModel):
    phone: str


class VerifyOtpRequest(BaseModel):
    phone: str
    otp: str


# =========================
# LOGIN (SEND OTP)
# =========================
@router.post("/login")
@limiter.limit("5/minute")
def login(
    request: Request,          # 🔴 REQUIRED FOR SLOWAPI
    data: LoginRequest,
):
    if len(data.phone) != 10:
        raise HTTPException(status_code=400, detail="Invalid phone number")

    # OTP sending will be integrated later (SMS / WhatsApp)
    return {
        "message": "OTP sent successfully",
        "otp_hint": "Use 123456 for now"
    }


# =========================
# VERIFY OTP
# =========================
@router.post("/verify-otp")
@limiter.limit("5/minute")
def verify_otp(
    request: Request,          # 🔴 REQUIRED FOR SLOWAPI
    data: VerifyOtpRequest,
):
    if data.otp != "123456":
        raise HTTPException(status_code=400, detail="Invalid OTP")

    token = create_access_token({
        "sub": data.phone,
        "role": "customer",
    })

    return {
        "access_token": token,
        "token_type": "bearer",
    }
