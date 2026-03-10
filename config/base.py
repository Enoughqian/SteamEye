# 基础配置：所有环境共用的非敏感配置
from typing import Optional

class BaseSettings:
    # 数据库通用配置
    DB_ECHO: bool = False  # 是否打印SQL语句（生产环境关闭）
    DB_POOL_SIZE: int = 10  # 连接池大小
    DB_MAX_OVERFLOW: int = 20  # 连接池最大溢出数
    DB_SCHEMA: str = "mage_game"  # 数据库schema（库名）
    
    # 环境标识（通过环境变量注入，默认dev）
    ENV: str = "dev"