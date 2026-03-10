from datetime import date, datetime
from decimal import Decimal
from typing import Optional

from sqlmodel import Field, SQLModel, create_engine


class GameBase(SQLModel, table=True):
    """
    游戏基础信息表（全球统一数据）
    对应数据库表：mage_game.game_base
    """
    # 表名指定（如果模型名和表名不一致时必须指定，这里保持一致也显式声明）
    __tablename__ = "game_base"
    # 数据库schema指定（对应mage_game库）
    __table_args__ = {"schema": "mage_game"}

    # 自增主键
    id: Optional[int] = Field(
        default=None,
        primary_key=True,
        sa_column_kwargs={"autoincrement": True, "comment": "自增主键"}
    )
    
    # Steam游戏唯一ID（核心关联键）
    steam_app_id: str = Field(
        max_length=20,
        nullable=False,
        sa_column_kwargs={"comment": "Steam游戏唯一ID（核心关联键）"},
        index=True,  # 对应唯一索引uk_steam_app_id
        unique=True
    )
    
    # 开发商（全球统一）
    developer: str = Field(
        max_length=200,
        nullable=False,
        sa_column_kwargs={"comment": "开发商（全球统一）"},
        index=True  # 对应索引idx_developer
    )
    
    # 发行商（全球统一）
    publisher: Optional[str] = Field(
        default=None,
        max_length=200,
        sa_column_kwargs={"comment": "发行商（全球统一）"}
    )
    
    # 全球首发日期（统一）
    global_release_date: Optional[date] = Field(
        default=None,
        sa_column_kwargs={"comment": "全球首发日期（统一）"},
        index=True  # 对应索引idx_global_release_date
    )
    
    # Steam全球好评率（如91.00）
    steam_score: Optional[Decimal] = Field(
        default=None,
        max_digits=5,
        decimal_places=2,
        sa_column_kwargs={"comment": "Steam全球好评率（如91.00）"}
    )
    
    # Metacritic全球媒体评分（0-100）
    mc_media_score: Optional[int] = Field(
        default=None,
        sa_column_kwargs={"comment": "Metacritic全球媒体评分（0-100）"}
    )
    
    # Metacritic全球玩家评分（0-10）
    mc_user_score: Optional[Decimal] = Field(
        default=None,
        max_digits=3,
        decimal_places=1,
        sa_column_kwargs={"comment": "Metacritic全球玩家评分（0-10）"}
    )
    
    # 创建时间
    create_time: Optional[datetime] = Field(
        default=None,
        sa_column_kwargs={
            "comment": "创建时间",
            "server_default": "CURRENT_TIMESTAMP"
        }
    )
    
    # 更新时间
    update_time: Optional[datetime] = Field(
        default=None,
        sa_column_kwargs={
            "comment": "更新时间",
            "server_default": "CURRENT_TIMESTAMP",
            "onupdate": "CURRENT_TIMESTAMP"
        }
    )


# 示例：数据库连接和表创建（实际使用时建议放到单独的配置/初始化文件）
if __name__ == "__main__":
    # 替换为你的数据库连接信息
    DATABASE_URL = "mysql+pymysql://username:password@host:port/mage_game"
    
    # 创建数据库引擎
    engine = create_engine(DATABASE_URL, echo=True)
    
    # 创建表（首次运行时使用）
    SQLModel.metadata.create_all(engine)