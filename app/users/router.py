from fastapi import APIRouter, Depends
from app.auth.deps import get_current_user

router = APIRouter(prefix="/users", tags=["Users"])

@router.get("/me")
def get_me(user=Depends(get_current_user)):
    return {
        "phone": user["sub"],
        "role": user["role"]
    }
