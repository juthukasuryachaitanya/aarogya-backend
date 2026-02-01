from fastapi import Depends, HTTPException, status
from app.auth.jwt import get_current_user

def admin_only(user=Depends(get_current_user)):
    if user.get("role") != "admin":
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Admin access only"
        )
    return user
