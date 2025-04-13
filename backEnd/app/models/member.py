from sqlalchemy import Column, Integer, String, DateTime, ForeignKey
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship
from app.database import Base
from app.models.user import User

class Member(Base):
    __tablename__ = "members"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(50), nullable=False)
    phone = Column(String(20), unique=True, index=True, nullable=False)
    level = Column(Integer, default=1)  # 会员等级：1-普通，2-银卡，3-金卡
    user_id = Column(Integer, ForeignKey("users.id"))
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())

    # 关联用户
    user = relationship("User", backref="member_info")