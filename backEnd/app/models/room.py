from sqlalchemy import Column, Integer, String, DateTime, Boolean, Float, ForeignKey, Text
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship
from app.database import Base

class Room(Base):
    __tablename__ = "rooms"

    id = Column(Integer, primary_key=True, index=True)
    room_number = Column(String(20), nullable=False, index=True)
    room_type = Column(String(50), nullable=False)  # 标准间、豪华间、套房等
    floor = Column(Integer, nullable=False)
    price = Column(Float, nullable=False)
    capacity = Column(Integer, nullable=False, default=2)  # 可住人数
    description = Column(Text, nullable=True)
    is_available = Column(Boolean, default=True)  # 是否可用
    branch_id = Column(Integer, ForeignKey("branches.id"), nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())

    # 关联分店
    branch = relationship("Branch", backref="rooms")
    
    # 唯一约束：同一分店内房间号不能重复
    __table_args__ = (
        {"mysql_charset": "utf8mb4", "mysql_collate": "utf8mb4_unicode_ci"},
    )