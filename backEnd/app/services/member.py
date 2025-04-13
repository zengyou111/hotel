from sqlalchemy.orm import Session
from app.models.member import Member
from app.models.user import User
from typing import List, Optional

def get_member(db: Session, member_id: int):
    return db.query(Member).filter(Member.id == member_id).first()

def get_member_by_phone(db: Session, phone: str):
    return db.query(Member).filter(Member.phone == phone).first()

def get_members(db: Session, skip: int = 0, limit: int = 100):
    return db.query(Member).offset(skip).limit(limit).all()

def get_users_without_member(db: Session, skip: int = 0, limit: int = 100):
    # 查询没有关联会员的用户
    return db.query(User).outerjoin(Member, User.id == Member.user_id).filter(Member.id == None).offset(skip).limit(limit).all()

def get_user_by_phone(db: Session, phone: str):
    return db.query(User).filter(User.phone == phone).first()

def create_member(db: Session, name: str, phone: str, level: int = 1, user_id: Optional[int] = None):
    # 检查用户是否存在
    if user_id:
        user = db.query(User).filter(User.id == user_id).first()
        if not user:
            return None
    
    # 检查会员是否已存在
    existing_member = get_member_by_phone(db, phone)
    if existing_member:
        return None
    
    db_member = Member(name=name, phone=phone, level=level, user_id=user_id)
    db.add(db_member)
    db.commit()
    db.refresh(db_member)
    return db_member

def update_member(db: Session, member_id: int, name: Optional[str] = None, level: Optional[int] = None):
    db_member = get_member(db, member_id)
    if not db_member:
        return None
    
    if name is not None:
        db_member.name = name
    if level is not None:
        db_member.level = level
    
    db.commit()
    db.refresh(db_member)
    return db_member

def delete_member(db: Session, member_id: int):
    db_member = get_member(db, member_id)
    if not db_member:
        return False
    
    db.delete(db_member)
    db.commit()
    return True