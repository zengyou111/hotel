from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List, Optional
from pydantic import BaseModel
from datetime import datetime
from app.database import get_db
from app.services.member import (
    get_member, get_members, create_member, update_member, delete_member,
    get_users_without_member, get_user_by_phone
)
from app.services.user import get_current_admin
from app.config import settings

router = APIRouter(prefix=f"{settings.API_PREFIX}/members", tags=["会员"])

class MemberBase(BaseModel):
    name: str
    phone: str
    level: int = 1

class MemberCreate(MemberBase):
    user_id: Optional[int] = None

class MemberUpdate(BaseModel):
    name: Optional[str] = None
    level: Optional[int] = None

class MemberResponse(MemberBase):
    id: int
    user_id: Optional[int] = None
    created_at: datetime  # 改为 datetime 类型
    updated_at: Optional[datetime] = None  # 改为 datetime 类型

    class Config:
        orm_mode = True
        json_encoders = {
            datetime: lambda v: v.strftime("%Y-%m-%d %H:%M:%S")
        }

class UserBase(BaseModel):
    id: int
    phone: str
    is_admin: bool

    class Config:
        orm_mode = True

@router.post("/", response_model=MemberResponse, status_code=status.HTTP_201_CREATED)
def create_new_member(
    member: MemberCreate, 
    db: Session = Depends(get_db),
    current_admin: dict = Depends(get_current_admin)
):
    """
    创建新会员（仅管理员）
    """
    result = create_member(
        db=db, 
        name=member.name, 
        phone=member.phone, 
        level=member.level, 
        user_id=member.user_id
    )
    if not result:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="创建会员失败，可能是用户不存在或会员已存在"
        )
    return result

@router.get("/", response_model=List[MemberResponse])
def read_members(
    skip: int = 0, 
    limit: int = 100, 
    db: Session = Depends(get_db),
    current_admin: dict = Depends(get_current_admin)
):
    """
    获取所有会员（仅管理员）
    """
    members = get_members(db, skip=skip, limit=limit)
    return members

@router.get("/available-users", response_model=List[UserBase])
def read_available_users(
    skip: int = 0, 
    limit: int = 100, 
    db: Session = Depends(get_db),
    current_admin: dict = Depends(get_current_admin)
):
    """
    获取所有没有关联会员的用户（仅管理员）
    """
    users = get_users_without_member(db, skip=skip, limit=limit)
    return users

@router.get("/user/{phone}", response_model=UserBase)
def read_user_by_phone(
    phone: str,
    db: Session = Depends(get_db),
    current_admin: dict = Depends(get_current_admin)
):
    """
    通过手机号查找用户（仅管理员）
    """
    user = get_user_by_phone(db, phone=phone)
    if user is None:
        raise HTTPException(status_code=404, detail="用户不存在")
    return user

@router.get("/{member_id}", response_model=MemberResponse)
def read_member(
    member_id: int, 
    db: Session = Depends(get_db),
    current_admin: dict = Depends(get_current_admin)
):
    """
    获取特定会员（仅管理员）
    """
    db_member = get_member(db, member_id=member_id)
    if db_member is None:
        raise HTTPException(status_code=404, detail="会员不存在")
    return db_member

@router.put("/{member_id}", response_model=MemberResponse)
def update_member_info(
    member_id: int, 
    member: MemberUpdate, 
    db: Session = Depends(get_db),
    current_admin: dict = Depends(get_current_admin)
):
    """
    更新会员信息（仅管理员）
    """
    db_member = update_member(db, member_id=member_id, name=member.name, level=member.level)
    if db_member is None:
        raise HTTPException(status_code=404, detail="会员不存在")
    return db_member

@router.delete("/{member_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_member_info(
    member_id: int, 
    db: Session = Depends(get_db),
    current_admin: dict = Depends(get_current_admin)
):
    """
    删除会员（仅管理员）
    """
    success = delete_member(db, member_id=member_id)
    if not success:
        raise HTTPException(status_code=404, detail="会员不存在")
    return None