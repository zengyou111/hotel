# app/config.py
class Settings:
    # TODO MySQL 配置
    MYSQL_HOST = "设置本地或者远程的mysql host"
    MYSQL_PORT = 3306
    MYSQL_USER = "zengyouRoot"
    MYSQL_PASSWORD = "zengyouRoot@"
    MYSQL_DATABASE = "hotel"  # 数据库名，启动时自动创建
    # TODO JWT 配置
    SECRET_KEY = "123456"
    ALGORITHM = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES = 7*24*60
    # TODO API 前缀
    API_PREFIX = "/api"

settings = Settings()
