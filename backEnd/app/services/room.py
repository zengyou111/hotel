from sqlalchemy.orm import Session
from app.models.room import Room
from app.models.branch import Branch
from typing import List, Optional

def get_room(db: Session, room_id: int):
    return db.query(Room).filter(Room.id == room_id).first()

def get_room_by_number_and_branch(db: Session, room_number: str, branch_id: int):
    return db.query(Room).filter(Room.room_number == room_number, Room.branch_id == branch_id).first()

def get_rooms(
    db: Session, 
    skip: int = 0, 
    limit: int = 100, 
    branch_id: Optional[int] = None,
    is_available: Optional[bool] = None,
    room_type: Optional[str] = None
):
    query = db.query(Room)
    
    if branch_id is not None:
        query = query.filter(Room.branch_id == branch_id)
    
    if is_available is not None:
        query = query.filter(Room.is_available == is_available)
        
    if room_type is not None:
        query = query.filter(Room.room_type == room_type)
        
    return query.offset(skip).limit(limit).all()

def create_room(
    db: Session, 
    room_number: str, 
    room_type: str, 
    floor: int,
    price: float,
    capacity: int,
    branch_id: int,
    description: Optional[str] = None
):
    # 检查分店是否存在
    branch = db.query(Branch).filter(Branch.id == branch_id).first()
    if not branch:
        return None
    
    # 检查房间号在该分店是否已存在
    existing_room = get_room_by_number_and_branch(db, room_number, branch_id)
    if existing_room:
        return None
    
    db_room = Room(
        room_number=room_number,
        room_type=room_type,
        floor=floor,
        price=price,
        capacity=capacity,
        branch_id=branch_id,
        description=description
    )
    db.add(db_room)
    db.commit()
    db.refresh(db_room)
    return db_room

def update_room(
    db: Session, 
    room_id: int, 
    room_number: Optional[str] = None,
    room_type: Optional[str] = None,
    floor: Optional[int] = None,
    price: Optional[float] = None,
    capacity: Optional[int] = None,
    description: Optional[str] = None,
    is_available: Optional[bool] = None
):
    db_room = get_room(db, room_id)
    if not db_room:
        return None
    
    # 如果要更新房间号，检查新房间号是否已存在
    if room_number is not None and room_number != db_room.room_number:
        existing_room = get_room_by_number_and_branch(db, room_number, db_room.branch_id)
        if existing_room:
            return None
        db_room.room_number = room_number
    
    if room_type is not None:
        db_room.room_type = room_type
    if floor is not None:
        db_room.floor = floor
    if price is not None:
        db_room.price = price
    if capacity is not None:
        db_room.capacity = capacity
    if description is not None:
        db_room.description = description
    if is_available is not None:
        db_room.is_available = is_available
    
    db.commit()
    db.refresh(db_room)
    return db_room

def delete_room(db: Session, room_id: int):
    db_room = get_room(db, room_id)
    if not db_room:
        return False
    
    db.delete(db_room)
    db.commit()
    return True