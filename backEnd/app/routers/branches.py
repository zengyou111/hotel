from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.orm import Session
from typing import List, Optional
from pydantic import BaseModel
from datetime import datetime
from app.database import get_db
from app.services.branch import (
    get_branch, get_branches, create_branch, update_branch, delete_branch
)
from app.services.user import get_current_user, get_current_admin
from app.config import settings

router = APIRouter(prefix=f"{settings.API_PREFIX}/branches", tags=["分店"])

class BranchBase(BaseModel):
    name: str
    address: str
    phone: str
    description: Optional[str] = None
    is_active: bool = True

class BranchCreate(BranchBase):
    pass

class BranchUpdate(BranchBase):
    pass

class Branch(BranchBase):
    id: int
    created_at: datetime
    updated_at: Optional[datetime] = None

    class Config:
        orm_mode = True
        json_encoders = {
            datetime: lambda v: v.strftime("%Y-%m-%d %H:%M:%S")
        }

@router.post("/", response_model=Branch, status_code=status.HTTP_201_CREATED)
def create_branch_endpoint(
    branch: BranchCreate,
    db: Session = Depends(get_db),
    current_admin = Depends(get_current_admin)
):
    """
    创建新分店（仅管理员）
    """
    db_branch = create_branch(
        db=db,
        name=branch.name,
        address=branch.address,
        phone=branch.phone,
        description=branch.description,
        is_active=branch.is_active
    )
    return db_branch

@router.get("/", response_model=List[Branch])
def read_branches(
    skip: int = 0,
    limit: int = 100,
    is_active: Optional[bool] = Query(None, description="筛选活跃状态"),
    db: Session = Depends(get_db),
    current_user = Depends(get_current_user)  # 修改为普通用户权限
):
    """
    获取分店列表（所有用户）
    """
    branches = get_branches(db, skip=skip, limit=limit, is_active=is_active)
    return branches

@router.get("/{branch_id}", response_model=Branch)
def read_branch(
    branch_id: int,
    db: Session = Depends(get_db),
    current_user = Depends(get_current_user)  # 修改为普通用户权限
):
    """
    获取特定分店（所有用户）
    """
    db_branch = get_branch(db, branch_id=branch_id)
    if db_branch is None:
        raise HTTPException(status_code=404, detail="分店不存在")
    return db_branch

@router.put("/{branch_id}", response_model=Branch)
def update_branch_info(
    branch_id: int,
    branch: BranchUpdate,
    db: Session = Depends(get_db),
    current_admin = Depends(get_current_admin)
):
    """
    更新分店信息（仅管理员）
    """
    db_branch = update_branch(
        db,
        branch_id=branch_id,
        name=branch.name,
        address=branch.address,
        phone=branch.phone,
        description=branch.description,
        is_active=branch.is_active
    )
    if db_branch is None:
        raise HTTPException(status_code=404, detail="分店不存在")
    return db_branch

@router.delete("/{branch_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_branch_info(
    branch_id: int,
    db: Session = Depends(get_db),
    current_admin = Depends(get_current_admin)
):
    """
    删除分店（仅管理员）
    """
    success = delete_branch(db, branch_id=branch_id)
    if not success:
        raise HTTPException(status_code=404, detail="分店不存在")
    return None