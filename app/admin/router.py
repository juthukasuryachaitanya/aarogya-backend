from fastapi import APIRouter, HTTPException
from pydantic import BaseModel

from app.core.security import create_access_token
from app.core.logger import logger

router = APIRouter(prefix="/admin", tags=["Admin"])

class AdminLogin(BaseModel):
    phone: str
    otp: str

@router.post("/login")
def admin_login(data: AdminLogin):
    if data.otp != "999999":
        logger.warning(
            f"Failed admin login attempt | phone={data.phone}"
        )
        raise HTTPException(status_code=400, detail="Invalid admin OTP")

    token = create_access_token({
        "sub": data.phone,
        "role": "admin",
    })

    # 🧾 LOG — ADMIN LOGIN SUCCESS
    logger.info(f"Admin login successful | phone={data.phone}")

    return {
        "access_token": token,
        "token_type": "bearer",
    }
