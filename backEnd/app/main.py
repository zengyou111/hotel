from fastapi import FastAPI, Depends
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy import text
from app.database import engine, Base, get_db, BASE_MYSQL_URL
from app.config import settings
from app.routers import auth, users ,members,branches,rooms,bookings,statistics
from sqlalchemy.orm import Session
import pymysql

app = FastAPI()

# 添加CORS中间件
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # 允许所有来源，生产环境应该限制
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# 创建数据库（如果不存在）
def create_database_if_not_exists():
    conn = pymysql.connect(
        host=settings.MYSQL_HOST,
        port=settings.MYSQL_PORT,
        user=settings.MYSQL_USER,
        password=settings.MYSQL_PASSWORD
    )
    cursor = conn.cursor()
    cursor.execute(f"CREATE DATABASE IF NOT EXISTS {settings.MYSQL_DATABASE}")
    conn.commit()
    cursor.close()
    conn.close()

# 注册路由
app.include_router(auth.router)
app.include_router(users.router)
app.include_router(members.router)
app.include_router(branches.router)
app.include_router(rooms.router)
app.include_router(bookings.router)
app.include_router(statistics.router)




@app.on_event("startup")
async def startup():
    # 创建数据库（如果不存在）
    create_database_if_not_exists()
    # 创建所有表
    Base.metadata.create_all(bind=engine)

@app.get("/")
def read_root():
    return {"message": "酒店管理系统API"}

@app.get(f"{settings.API_PREFIX}/health")
def health_check(db: Session = Depends(get_db)):
    # 测试数据库连接
    db.execute(text("SELECT 1"))
    return {"status": "healthy"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("app.main:app", host="0.0.0.0", port=8000, reload=True)