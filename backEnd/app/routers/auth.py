from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from datetime import timedelta
from pydantic import BaseModel
from app.database import get_db
from app.services.user import authenticate_user, create_user, get_user_by_phone
from app.services.auth import create_access_token
from app.config import settings

router = APIRouter(prefix=f"{settings.API_PREFIX}/auth", tags=["认证"])

class UserCreate(BaseModel):
    phone: str
    password: str
    is_admin: bool = False

class Token(BaseModel):
    access_token: str
    token_type: str

@router.post("/register", response_model=Token)
def register(user_data: UserCreate, db: Session = Depends(get_db)):
    db_user = get_user_by_phone(db, phone=user_data.phone)
    if db_user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="该手机号已被注册"
        )
    user = create_user(
        db=db, 
        phone=user_data.phone, 
        password=user_data.password,
        is_admin=user_data.is_admin
    )
    access_token_expires = timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": user.phone}, expires_delta=access_token_expires
    )
    return {"access_token": access_token, "token_type": "bearer"}

@router.post("/login", response_model=Token)
def login(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    user = authenticate_user(db, form_data.username, form_data.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="手机号或密码错误",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token_expires = timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": user.phone}, expires_delta=access_token_expires
    )
    return {"access_token": access_token, "token_type": "bearer"}