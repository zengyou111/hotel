from sqlalchemy.orm import Session
from app.models.branch import Branch
from typing import List, Optional

def get_branch(db: Session, branch_id: int):
    return db.query(Branch).filter(Branch.id == branch_id).first()

def get_branch_by_name(db: Session, name: str):
    return db.query(Branch).filter(Branch.name == name).first()

def get_branches(db: Session, skip: int = 0, limit: int = 100, is_active: Optional[bool] = None):
    query = db.query(Branch)
    if is_active is not None:
        query = query.filter(Branch.is_active == is_active)
    return query.offset(skip).limit(limit).all()

def create_branch(db: Session, name: str, address: str, phone: str, description: Optional[str] = None,is_active=None):
    # 检查分店名称是否已存在
    existing_branch = get_branch_by_name(db, name)
    if existing_branch:
        return None
    
    db_branch = Branch(
        name=name, 
        address=address, 
        phone=phone, 
        description=description,
        is_active=is_active
    )
    db.add(db_branch)
    db.commit()
    db.refresh(db_branch)
    return db_branch

def update_branch(
    db: Session, 
    branch_id: int, 
    name: Optional[str] = None, 
    address: Optional[str] = None, 
    phone: Optional[str] = None, 
    description: Optional[str] = None,
    is_active: Optional[bool] = None
):
    db_branch = get_branch(db, branch_id)
    if not db_branch:
        return None
    
    # 如果要更新名称，检查新名称是否已存在
    if name is not None and name != db_branch.name:
        existing_branch = get_branch_by_name(db, name)
        if existing_branch:
            return None
        db_branch.name = name
    
    if address is not None:
        db_branch.address = address
    if phone is not None:
        db_branch.phone = phone
    if description is not None:
        db_branch.description = description
    if is_active is not None:
        db_branch.is_active = is_active
    
    db.commit()
    db.refresh(db_branch)
    return db_branch

def delete_branch(db: Session, branch_id: int):
    db_branch = get_branch(db, branch_id)
    if not db_branch:
        return False
    
    db.delete(db_branch)
    db.commit()
    return True