from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.orm import Session
from typing import List, Optional
from pydantic import BaseModel
from datetime import datetime, date
from app.database import get_db
from app.services.booking import (
    get_booking, get_user_bookings, get_all_bookings, create_booking,
    update_booking_status, cancel_booking, get_available_rooms
)
from app.services.user import get_current_user, get_current_admin
from app.config import settings

router = APIRouter(prefix=f"{settings.API_PREFIX}/bookings", tags=["预订"])


class RoomInfo(BaseModel):
    id: int
    room_number: str
    room_type: str
    price: float
    capacity: int
    branch_id: int  # 添加分店ID

    class Config:
        orm_mode = True


class BranchInfo(BaseModel):
    id: int
    name: str
    address: str

    class Config:
        orm_mode = True


class BookingBase(BaseModel):
    check_in_date: date
    check_out_date: date
    special_requests: Optional[str] = None


# class BookingCreate(BookingBase):
#     room_id: int

# 更新 BookingCreate 类
class BookingCreate(BookingBase):
    room_id: int
    guest_count: int = 1  # 添加客人数量字段，默认为1

# 更新 BookingResponse 类
# class BookingResponse(BookingBase):
#     id: int
#     status: str
#     total_price: float
#     user_id: int
#     room_id: int
#     guest_count: int  # 添加客人数量字段
#     room: RoomInfo
#     created_at: datetime
#     updated_at: Optional[datetime] = None
#
#     class Config:
#         orm_mode = True
#         json_encoders = {
#             datetime: lambda v: v.strftime("%Y-%m-%d %H:%M:%S"),
#             date: lambda v: v.strftime("%Y-%m-%d")
#         }

# 修改 BookingResponse 类，添加 branch 字段
class BookingResponse(BookingBase):
    id: int
    status: str
    total_price: float
    user_id: int
    room_id: int
    guest_count: int
    room: RoomInfo
    branch: Optional[BranchInfo] = None  # 添加分店信息
    created_at: datetime
    updated_at: Optional[datetime] = None

    class Config:
        orm_mode = True
        json_encoders = {
            datetime: lambda v: v.strftime("%Y-%m-%d %H:%M:%S"),
            date: lambda v: v.strftime("%Y-%m-%d")
        }



# class BookingResponse(BookingBase):
#     id: int
#     status: str
#     total_price: float
#     user_id: int
#     room_id: int
#     room: RoomInfo
#     created_at: datetime
#     updated_at: Optional[datetime] = None
#
#     class Config:
#         orm_mode = True
#         json_encoders = {
#             datetime: lambda v: v.strftime("%Y-%m-%d %H:%M:%S"),
#             date: lambda v: v.strftime("%Y-%m-%d")
#         }


class BookingStatusUpdate(BaseModel):
    status: str


class AvailableRoomResponse(BaseModel):
    id: int
    room_number: str
    room_type: str
    floor: int
    price: float
    capacity: int
    description: Optional[str] = None
    branch_id: int

    class Config:
        orm_mode = True


# 更新创建预订的路由
@router.post("/", response_model=BookingResponse, status_code=status.HTTP_201_CREATED)
def create_new_booking(
        booking: BookingCreate,
        db: Session = Depends(get_db),
        current_user=Depends(get_current_user)
):
    """
    创建新预订（普通用户）
    """
    # 转换日期为datetime
    check_in_date = datetime.combine(booking.check_in_date, datetime.min.time())
    check_out_date = datetime.combine(booking.check_out_date, datetime.min.time())

    db_booking = create_booking(
        db=db,
        user_id=current_user.id,
        room_id=booking.room_id,
        check_in_date=check_in_date,
        check_out_date=check_out_date,
        special_requests=booking.special_requests,
        guest_count=booking.guest_count  # 传递客人数量
    )

    if db_booking is None:
        raise HTTPException(
            status_code=400,
            detail="创建预订失败，可能是房间不可用或日期无效"
        )
    return db_booking
# @router.post("/", response_model=BookingResponse, status_code=status.HTTP_201_CREATED)
# def create_new_booking(
#         booking: BookingCreate,
#         db: Session = Depends(get_db),
#         current_user=Depends(get_current_user)
# ):
#     """
#     创建新预订（普通用户）
#     """
#     # 转换日期为datetime
#     check_in_date = datetime.combine(booking.check_in_date, datetime.min.time())
#     check_out_date = datetime.combine(booking.check_out_date, datetime.min.time())
#
#     db_booking = create_booking(
#         db=db,
#         user_id=current_user.id,
#         room_id=booking.room_id,
#         check_in_date=check_in_date,
#         check_out_date=check_out_date,
#         special_requests=booking.special_requests
#     )
#
#     if db_booking is None:
#         raise HTTPException(
#             status_code=400,
#             detail="创建预订失败，可能是房间不可用或日期无效"
#         )
#     return db_booking


@router.get("/my-bookings", response_model=List[BookingResponse])
def read_my_bookings(
        skip: int = 0,
        limit: int = 100,
        status: Optional[str] = Query(None, description="筛选状态"),
        db: Session = Depends(get_db),
        current_user=Depends(get_current_user)
):
    """
    获取当前用户的预订（普通用户）
    """
    bookings = get_user_bookings(db, user_id=current_user.id, skip=skip, limit=limit, status=status)
    return bookings


@router.get("/admin", response_model=List[BookingResponse])
def read_all_bookings(
        skip: int = 0,
        limit: int = 100,
        status: Optional[str] = Query(None, description="筛选状态"),
        branch_id: Optional[int] = Query(None, description="筛选分店"),
        db: Session = Depends(get_db),
        current_admin=Depends(get_current_admin)
):
    """
    获取所有预订（仅管理员）
    """
    bookings = get_all_bookings(db, skip=skip, limit=limit, status=status, branch_id=branch_id)
    return bookings


@router.get("/available-rooms", response_model=List[AvailableRoomResponse])
def read_available_rooms(
        branch_id: int,
        check_in_date: date,
        check_out_date: date,
        room_type: Optional[str] = Query(None, description="筛选房间类型"),
        capacity: Optional[int] = Query(None, description="最小容纳人数"),
        db: Session = Depends(get_db),
        current_user=Depends(get_current_user)
):
    """
    获取可用房间（普通用户）
    """
    # 转换日期为datetime
    check_in = datetime.combine(check_in_date, datetime.min.time())
    check_out = datetime.combine(check_out_date, datetime.min.time())

    rooms = get_available_rooms(
        db,
        branch_id=branch_id,
        check_in_date=check_in,
        check_out_date=check_out,
        room_type=room_type,
        capacity=capacity
    )
    return rooms


@router.get("/{booking_id}", response_model=BookingResponse)
def read_booking(
        booking_id: int,
        db: Session = Depends(get_db),
        current_user=Depends(get_current_user)
):
    """
    获取特定预订（用户只能查看自己的预订，管理员可查看所有）
    """
    db_booking = get_booking(db, booking_id=booking_id)
    if db_booking is None:
        raise HTTPException(status_code=404, detail="预订不存在")

    # 检查权限：普通用户只能查看自己的预订
    if not current_user.is_admin and db_booking.user_id != current_user.id:
        raise HTTPException(status_code=403, detail="没有权限查看此预订")

    return db_booking


@router.put("/{booking_id}/status", response_model=BookingResponse)
def update_booking_status_endpoint(
        booking_id: int,
        status_update: BookingStatusUpdate,
        db: Session = Depends(get_db),
        current_admin=Depends(get_current_admin)
):
    """
    更新预订状态（仅管理员）
    """
    db_booking = update_booking_status(db, booking_id=booking_id, status=status_update.status)
    if db_booking is None:
        raise HTTPException(
            status_code=404,
            detail="预订不存在或状态无效"
        )
    return db_booking


@router.put("/{booking_id}/cancel", response_model=BookingResponse)
def cancel_booking_endpoint(
        booking_id: int,
        db: Session = Depends(get_db),
        current_user=Depends(get_current_user)
):
    """
    取消预订（用户只能取消自己的预订，管理员可取消所有）
    """
    # 管理员可以取消任何预订
    if current_user.is_admin:
        db_booking = cancel_booking(db, booking_id=booking_id)
    else:
        # 普通用户只能取消自己的预订
        db_booking = cancel_booking(db, booking_id=booking_id, user_id=current_user.id)

    if db_booking is None:
        raise HTTPException(
            status_code=404,
            detail="预订不存在、无权取消或预订状态不允许取消"
        )
    return db_booking


# TODO 管理员端用
# ... existing code ...
from typing import List, Optional
from app.models import user
from app.services import booking


@router.get("/admin")
def admin_get_bookings(
        skip: int = 0,
        limit: int = 100,
        status: Optional[str] = None,
        branch_id: Optional[int] = None,
        db: Session = Depends(get_db),
        current_user: user.User = Depends(get_current_user)
):
    """管理员获取所有预订"""
    if not current_user.is_admin:
        raise HTTPException(status_code=403, detail="权限不足")

    bookings = booking.get_admin_bookings(db, skip=skip, limit=limit, status=status, branch_id=branch_id)

    # 将ORM对象转换为字典
    result = []
    for b in bookings:
        # 确保获取用户信息
        user_info = db.query(user.User).filter(user.User.id == b.user_id).first()

        booking_dict = {
            "id": b.id,
            "user_id": b.user_id,
            "room_id": b.room_id,
            "check_in_date": b.check_in_date,
            "check_out_date": b.check_out_date,
            "total_price": b.total_price,
            "status": b.status,
            "created_at": b.created_at,
            "updated_at": b.updated_at,
            "user": {
                "id": user_info.id,
                "phone": user_info.phone,
                "is_admin": user_info.is_admin
            },
            "room": {
                "id": b.room.id,
                "room_number": b.room.room_number,
                "room_type": b.room.room_type,
                "price": b.room.price,
                "branch_id": b.room.branch_id
            }
        }
        result.append(booking_dict)

    return result


# @router.get("/admin")
# def admin_get_bookings(
#         skip: int = 0,
#         limit: int = 100,
#         status: Optional[str] = None,
#         branch_id: Optional[int] = None,
#         db: Session = Depends(get_db),
#         current_user: user.User = Depends(get_current_user)
# ):
#     """管理员获取所有预订"""
#     if not current_user.is_admin:
#         raise HTTPException(status_code=403, detail="权限不足")
#
#     bookings = booking.get_admin_bookings(db, skip=skip, limit=limit, status=status, branch_id=branch_id)
#
#     # 将ORM对象转换为字典
#     result = []
#     for b in bookings:
#         booking_dict = {
#             "id": b.id,
#             "user_id": b.user_id,
#             "room_id": b.room_id,
#             "check_in_date": b.check_in_date,
#             "check_out_date": b.check_out_date,
#             "total_price": b.total_price,
#             "status": b.status,
#             "created_at": b.created_at,
#             "updated_at": b.updated_at,
#             "user": {
#                 "id": b.user.id,
#                 "phone": b.user.phone,
#                 "is_admin": b.user.is_admin
#             },
#             "room": {
#                 "id": b.room.id,
#                 "room_number": b.room.room_number,
#                 "room_type": b.room.room_type,
#                 "price": b.room.price,
#                 "branch": {
#                     "id": b.room.branch.id,
#                     "name": b.room.branch.name,
#                     "address": b.room.branch.address
#                 }
#             }
#         }
#         result.append(booking_dict)
#
#     return result


@router.get("/admin/count")
def admin_get_booking_count(
        status: Optional[str] = None,
        branch_id: Optional[int] = None,
        db: Session = Depends(get_db),
        current_user: user.User = Depends(get_current_user)
):
    """获取预订总数"""
    if not current_user.is_admin:
        raise HTTPException(status_code=403, detail="权限不足")

    count = booking.get_admin_booking_count(db, status=status, branch_id=branch_id)

    return {"count": count}

# ... existing code ...