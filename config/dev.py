# 开发环境配置（本地/内网MySQL）
from .base import BaseSettings

class DevSettings(BaseSettings):
    # MySQL连接信息（开发环境，可写死本地配置，或通过.env读取）
    DB_USER: str = "root"
    DB_PASSWORD: str = "123456"
    DB_HOST: str = "127.0.0.1"
    DB_PORT: int = 3306
    DB_DATABASE: str = "mage_game"
    
    # 拼接MySQL连接URL
    @property
    def DATABASE_URL(self) -> str:
        return (
            f"mysql+pymysql://{self.DB_USER}:{self.DB_PASSWORD}@"
            f"{self.DB_HOST}:{self.DB_PORT}/{self.DB_DATABASE}"
        )