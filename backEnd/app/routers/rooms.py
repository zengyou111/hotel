from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.orm import Session
from typing import List, Optional
from pydantic import BaseModel
from datetime import datetime
from app.database import get_db
from app.services.room import (
    get_room, get_rooms, create_room, update_room, delete_room
)
from app.services.user import get_current_admin
from app.config import settings

router = APIRouter(prefix=f"{settings.API_PREFIX}/rooms", tags=["客房"])

class RoomBase(BaseModel):
    room_number: str
    room_type: str
    floor: int
    price: float
    capacity: int
    description: Optional[str] = None

class RoomCreate(RoomBase):
    branch_id: int

class RoomUpdate(BaseModel):
    room_number: Optional[str] = None
    room_type: Optional[str] = None
    floor: Optional[int] = None
    price: Optional[float] = None
    capacity: Optional[int] = None
    description: Optional[str] = None
    is_available: Optional[bool] = None

class BranchInfo(BaseModel):
    id: int
    name: str

    class Config:
        orm_mode = True

class RoomResponse(RoomBase):
    id: int
    is_available: bool
    branch_id: int
    branch: BranchInfo
    created_at: datetime
    updated_at: Optional[datetime] = None

    class Config:
        orm_mode = True
        json_encoders = {
            datetime: lambda v: v.strftime("%Y-%m-%d %H:%M:%S")
        }

@router.post("/", response_model=RoomResponse, status_code=status.HTTP_201_CREATED)
def create_new_room(
    room: RoomCreate,
    db: Session = Depends(get_db),
    current_admin: dict = Depends(get_current_admin)
):
    """
    创建新客房（仅管理员）
    """
    result = create_room(
        db=db,
        room_number=room.room_number,
        room_type=room.room_type,
        floor=room.floor,
        price=room.price,
        capacity=room.capacity,
        branch_id=room.branch_id,
        description=room.description
    )
    if not result:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="创建客房失败，可能是分店不存在或房间号已存在"
        )
    return result

@router.get("/", response_model=List[RoomResponse])
def read_rooms(
    skip: int = 0,
    limit: int = 100,
    branch_id: Optional[int] = Query(None, description="筛选分店"),
    is_available: Optional[bool] = Query(None, description="筛选可用状态"),
    room_type: Optional[str] = Query(None, description="筛选房间类型"),
    db: Session = Depends(get_db),
    current_admin: dict = Depends(get_current_admin)
):
    """
    获取所有客房（仅管理员）
    """
    rooms = get_rooms(
        db,
        skip=skip,
        limit=limit,
        branch_id=branch_id,
        is_available=is_available,
        room_type=room_type
    )
    return rooms

@router.get("/{room_id}", response_model=RoomResponse)
def read_room(
    room_id: int,
    db: Session = Depends(get_db),
    current_admin: dict = Depends(get_current_admin)
):
    """
    获取特定客房（仅管理员）
    """
    db_room = get_room(db, room_id=room_id)
    if db_room is None:
        raise HTTPException(status_code=404, detail="客房不存在")
    return db_room

@router.put("/{room_id}", response_model=RoomResponse)
def update_room_info(
    room_id: int,
    room: RoomUpdate,
    db: Session = Depends(get_db),
    current_admin: dict = Depends(get_current_admin)
):
    """
    更新客房信息（仅管理员）
    """
    db_room = update_room(
        db,
        room_id=room_id,
        room_number=room.room_number,
        room_type=room.room_type,
        floor=room.floor,
        price=room.price,
        capacity=room.capacity,
        description=room.description,
        is_available=room.is_available
    )
    if db_room is None:
        raise HTTPException(
            status_code=404,
            detail="客房不存在或房间号已被使用"
        )
    return db_room

@router.delete("/{room_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_room_info(
    room_id: int,
    db: Session = Depends(get_db),
    current_admin: dict = Depends(get_current_admin)
):
    """
    删除客房（仅管理员）
    """
    success = delete_room(db, room_id=room_id)
    if not success:
        raise HTTPException(status_code=404, detail="客房不存在")
    return None