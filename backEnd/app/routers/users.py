from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from pydantic import BaseModel
from app.database import get_db
from app.services.user import get_current_user
from app.models.user import User
from app.config import settings

router = APIRouter(prefix=f"{settings.API_PREFIX}/users", tags=["用户"])

class UserResponse(BaseModel):
    id: int
    phone: str
    is_admin: bool

    class Config:
        orm_mode = True

@router.get("/me", response_model=UserResponse)
async def read_users_me(current_user: User = Depends(get_current_user)):
    """
    获取当前登录用户的信息
    """
    return current_user