from sqlalchemy import Column, Integer, String, DateTime, Boolean, ForeignKey, Text, Float
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship
from app.database import Base
from datetime import datetime


class Booking(Base):
    __tablename__ = "bookings"

    id = Column(Integer, primary_key=True, index=True)
    check_in_date = Column(DateTime, nullable=False)
    check_out_date = Column(DateTime, nullable=False)
    status = Column(String(20), nullable=False, default="pending")  # pending, confirmed, cancelled, completed
    total_price = Column(Float, nullable=False)
    special_requests = Column(Text, nullable=True)
    guest_count = Column(Integer, nullable=False, default=1)  # 添加客人数量字段

    # 关联用户和房间
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    room_id = Column(Integer, ForeignKey("rooms.id"), nullable=False)

    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())

    # 关系
    user = relationship("User", backref="bookings")
    room = relationship("Room", backref="bookings")