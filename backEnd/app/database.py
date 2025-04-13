# app/database.py
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from urllib.parse import quote_plus
from app.config import settings

# 对密码中的 @ 进行转义
encoded_password = quote_plus(settings.MYSQL_PASSWORD)

# MySQL 基础连接字符串（不含数据库名，用于初始创建）
BASE_MYSQL_URL = (
    f"mysql+pymysql://{settings.MYSQL_USER}:{encoded_password}"
    f"@{settings.MYSQL_HOST}:{settings.MYSQL_PORT}"
)

# 完整连接字符串（含数据库名）
SQLALCHEMY_DATABASE_URL = f"{BASE_MYSQL_URL}/{settings.MYSQL_DATABASE}"

engine = create_engine(SQLALCHEMY_DATABASE_URL, echo=True)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()