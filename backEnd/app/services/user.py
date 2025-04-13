from sqlalchemy.orm import Session
from app.models.user import User
from app.services.auth import get_password_hash, verify_password
from jose import jwt, JWTError
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from app.config import settings
from app.database import get_db

oauth2_scheme = OAuth2PasswordBearer(tokenUrl=f"{settings.API_PREFIX}/auth/login")

def get_user_by_phone(db: Session, phone: str):
    return db.query(User).filter(User.phone == phone).first()

def create_user(db: Session, phone: str, password: str, is_admin: bool = False):
    hashed_password = get_password_hash(password)
    db_user = User(phone=phone, hashed_password=hashed_password, is_admin=is_admin)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user

# 在authenticate_user函数中添加调试信息
def authenticate_user(db: Session, phone: str, password: str):
    user = get_user_by_phone(db, phone)
    if not user:
        print(f"User with phone {phone} not found")
        return False
    print(f"Found user: {user.phone}, checking password")
    if not verify_password(password, user.hashed_password):
        print(f"Password verification failed for user {user.phone}")
        return False
    print(f"Password verified for user {user.phone}")
    return user

async def get_current_user(token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="无效的认证凭据",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM])
        phone: str = payload.get("sub")
        if phone is None:
            raise credentials_exception
    except JWTError:
        raise credentials_exception
    user = get_user_by_phone(db, phone=phone)
    if user is None:
        raise credentials_exception
    return user

async def get_current_admin(current_user: User = Depends(get_current_user)):
    if not current_user.is_admin:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="权限不足，需要管理员权限"
        )
    return current_user