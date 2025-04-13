from sqlalchemy import func, distinct
from sqlalchemy.orm import Session
from datetime import datetime, timedelta
from app.models.booking import Booking
from app.models.room import Room
from app.models.branch import Branch
from app.models.user import User

def get_booking_statistics(db: Session):
    """获取预订统计数据"""
    # 总预订数
    total_bookings = db.query(Booking).count()
    
    # 各状态预订数
    status_counts = db.query(
        Booking.status, 
        func.count(Booking.id).label('count')
    ).group_by(Booking.status).all()
    
    status_stats = {status: count for status, count in status_counts}
    
    # 计算总收入
    total_revenue = db.query(func.sum(Booking.total_price)).filter(
        Booking.status.in_(['confirmed', 'completed'])
    ).scalar() or 0
    
    # 获取最近7天的预订数据
    today = datetime.now().date()
    last_week = today - timedelta(days=6)
    
    daily_bookings = db.query(
        func.date(Booking.created_at).label('date'),
        func.count(Booking.id).label('count')
    ).filter(
        func.date(Booking.created_at) >= last_week
    ).group_by(
        func.date(Booking.created_at)
    ).all()
    
    # 填充没有预订的日期
    daily_stats = {}
    for i in range(7):
        date = (last_week + timedelta(days=i)).isoformat()
        daily_stats[date] = 0
    
    for date, count in daily_bookings:
        daily_stats[date.isoformat()] = count
    
    # 按分店统计预订数
    branch_bookings = db.query(
        Branch.name,
        func.count(Booking.id).label('count')
    ).join(
        Room, Room.branch_id == Branch.id
    ).join(
        Booking, Booking.room_id == Room.id
    ).group_by(
        Branch.name
    ).all()
    
    branch_stats = {name: count for name, count in branch_bookings}
    
    # 房型受欢迎程度
    room_type_stats = db.query(
        Room.room_type,
        func.count(Booking.id).label('count')
    ).join(
        Booking, Booking.room_id == Room.id
    ).group_by(
        Room.room_type
    ).all()
    
    room_type_popularity = {room_type: count for room_type, count in room_type_stats}
    
    # 用户数统计
    total_users = db.query(User).filter(User.is_admin == False).count()
    
    # 有预订记录的用户数
    users_with_bookings = db.query(func.count(distinct(Booking.user_id))).scalar() or 0
    
    return {
        "total_bookings": total_bookings,
        "status_statistics": status_stats,
        "total_revenue": float(total_revenue),
        "daily_statistics": daily_stats,
        "branch_statistics": branch_stats,
        "room_type_popularity": room_type_popularity,
        "user_statistics": {
            "total_users": total_users,
            "users_with_bookings": users_with_bookings
        }
    }