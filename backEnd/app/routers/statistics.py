from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.config import settings
from app.database import get_db
from app.services import statistics
from app.models.user import User
from app.services.user import get_current_user

router = APIRouter(prefix=f"{settings.API_PREFIX}/statistics", tags=["统计"])

@router.get("/bookings")
def get_booking_statistics(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """获取预订统计数据"""
    if not current_user.is_admin:
        raise HTTPException(status_code=403, detail="权限不足")
    
    return statistics.get_booking_statistics(db)