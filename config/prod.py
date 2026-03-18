# 开发环境配置（本地/内网MySQL）
from .base import BaseSettings
from dotenv import load_dotenv
import os

class ProdSettings(BaseSettings):
    load_dotenv(".prod_env")
    PROD_MYSQL_PASSWORD = os.getenv("PROD_MYSQL_PASSWORD","")

    # 拼接MySQL连接URL
    @property
    def DATABASE_URL(self) -> str:
        return (
            f"mysql+pymysql://{self.DB_USER}:{self.DB_PASSWORD}@"
            f"{self.DB_HOST}:{self.DB_PORT}/{self.DB_DATABASE}"
        )