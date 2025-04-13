from sqlalchemy.orm import Session
from app.models.booking import Booking
from app.models.room import Room
from app.models.branch import Branch
from app.models.user import User
from typing import List, Optional
from datetime import datetime, timedelta
import math
from sqlalchemy.orm import Session, joinedload

def get_booking(db: Session, booking_id: int):
    # 使用 join 加载房间和分店信息
    return db.query(Booking).filter(Booking.id == booking_id).first()


def get_user_bookings(db: Session, user_id: int, skip: int = 0, limit: int = 100, status: Optional[str] = None):
    query = db.query(Booking).filter(Booking.user_id == user_id)

    if status:
        query = query.filter(Booking.status == status)

    # 使用 options 预加载关联的房间和分店
    query = query.options(
        joinedload(Booking.room).joinedload(Room.branch)
    )

    return query.order_by(Booking.created_at.desc()).offset(skip).limit(limit).all()


def get_all_bookings(db: Session, skip: int = 0, limit: int = 100, status: Optional[str] = None,
                     branch_id: Optional[int] = None):
    query = db.query(Booking)

    if status:
        query = query.filter(Booking.status == status)

    if branch_id:
        # 通过关联的房间查找分店
        query = query.join(Room).filter(Room.branch_id == branch_id)

    # 使用 options 预加载关联的房间和分店
    query = query.options(
        joinedload(Booking.room).joinedload(Room.branch)
    )

    return query.order_by(Booking.created_at.desc()).offset(skip).limit(limit).all()


# def get_booking(db: Session, booking_id: int):
#     return db.query(Booking).filter(Booking.id == booking_id).first()
#
#
# def get_user_bookings(db: Session, user_id: int, skip: int = 0, limit: int = 100, status: Optional[str] = None):
#     query = db.query(Booking).filter(Booking.user_id == user_id)
#
#     if status:
#         query = query.filter(Booking.status == status)
#
#     return query.order_by(Booking.created_at.desc()).offset(skip).limit(limit).all()
#
#
# def get_all_bookings(db: Session, skip: int = 0, limit: int = 100, status: Optional[str] = None,
#                      branch_id: Optional[int] = None):
#     query = db.query(Booking)
#
#     if status:
#         query = query.filter(Booking.status == status)
#
#     if branch_id:
#         # 通过关联的房间查找分店
#         query = query.join(Room).filter(Room.branch_id == branch_id)
#
#     return query.order_by(Booking.created_at.desc()).offset(skip).limit(limit).all()


def is_room_available(db: Session, room_id: int, check_in_date: datetime, check_out_date: datetime,
                      exclude_booking_id: Optional[int] = None):
    # 检查房间是否存在且可用
    room = db.query(Room).filter(Room.id == room_id, Room.is_available == True).first()
    if not room:
        return False

    # 检查日期是否有效
    if check_in_date >= check_out_date:
        return False

    # 检查是否与现有预订冲突
    query = db.query(Booking).filter(
        Booking.room_id == room_id,
        Booking.status.in_(["pending", "confirmed"]),
        Booking.check_out_date > check_in_date,
        Booking.check_in_date < check_out_date
    )

    if exclude_booking_id:
        query = query.filter(Booking.id != exclude_booking_id)

    conflicting_bookings = query.count()
    return conflicting_bookings == 0


def calculate_total_price(db: Session, room_id: int, check_in_date: datetime, check_out_date: datetime):
    room = db.query(Room).filter(Room.id == room_id).first()
    if not room:
        return None

    # 计算天数
    days = (check_out_date - check_in_date).days
    if days <= 0:
        return None

    # 计算总价
    total_price = room.price * days
    return total_price


def create_booking(
        db: Session,
        user_id: int,
        room_id: int,
        check_in_date: datetime,
        check_out_date: datetime,
        special_requests: Optional[str] = None,
        guest_count: int = 1  # 添加客人数量参数
):
    # 检查房间是否可用
    if not is_room_available(db, room_id, check_in_date, check_out_date):
        return None

    # 计算总价
    total_price = calculate_total_price(db, room_id, check_in_date, check_out_date)
    if total_price is None:
        return None

    # 创建预订
    db_booking = Booking(
        user_id=user_id,
        room_id=room_id,
        check_in_date=check_in_date,
        check_out_date=check_out_date,
        total_price=total_price,
        special_requests=special_requests,
        status="pending",
        guest_count=guest_count  # 设置客人数量
    )

    db.add(db_booking)
    db.commit()
    db.refresh(db_booking)
    return db_booking

def update_booking_status(db: Session, booking_id: int, status: str):
    db_booking = get_booking(db, booking_id)
    if not db_booking:
        return None

    # 检查状态是否有效
    valid_statuses = ["pending", "confirmed", "cancelled", "completed"]
    if status not in valid_statuses:
        return None

    db_booking.status = status
    db.commit()
    db.refresh(db_booking)
    return db_booking


def cancel_booking(db: Session, booking_id: int, user_id: Optional[int] = None):
    db_booking = get_booking(db, booking_id)
    if not db_booking:
        return None

    # 如果提供了用户ID，检查预订是否属于该用户
    if user_id and db_booking.user_id != user_id:
        return None

    # 只有待确认或已确认的预订可以取消
    if db_booking.status not in ["pending", "confirmed"]:
        return None

    db_booking.status = "cancelled"
    db.commit()
    db.refresh(db_booking)
    return db_booking


def get_available_rooms(
        db: Session,
        branch_id: int,
        check_in_date: datetime,
        check_out_date: datetime,
        room_type: Optional[str] = None,
        capacity: Optional[int] = None
):
    # 获取分店中的所有可用房间
    query = db.query(Room).filter(Room.branch_id == branch_id, Room.is_available == True)

    if room_type:
        query = query.filter(Room.room_type == room_type)

    if capacity:
        query = query.filter(Room.capacity >= capacity)

    rooms = query.all()

    # 筛选出在指定日期范围内没有被预订的房间
    available_rooms = []
    for room in rooms:
        if is_room_available(db, room.id, check_in_date, check_out_date):
            available_rooms.append(room)

    return available_rooms



# TODO 管理员端用

def get_admin_bookings(db: Session, skip: int = 0, limit: int = 100, status: str = None, branch_id: int = None):
    """获取所有预订信息（管理员用）"""
    query = db.query(Booking)

    if status:
        query = query.filter(Booking.status == status)

    if branch_id:
        query = query.filter(Booking.room.has(branch_id=branch_id))

    return query.order_by(Booking.created_at.desc()).offset(skip).limit(limit).all()


def get_admin_booking_count(db: Session, status: str = None, branch_id: int = None):
    """获取预订总数（管理员用）"""
    query = db.query(Booking)

    if status:
        query = query.filter(Booking.status == status)

    if branch_id:
        query = query.filter(Booking.room.has(branch_id=branch_id))

    return query.count()

def get_bookings_by_status(db: Session, status: str, skip: int = 0, limit: int = 100):
    """根据状态获取预订信息"""
    return db.query(Booking).filter(Booking.status == status).order_by(Booking.created_at.desc()).offset(skip).limit(limit).all()

def get_booking_status_count(db: Session, status: str):
    """获取特定状态的预订数量"""
    return db.query(Booking).filter(Booking.status == status).count()