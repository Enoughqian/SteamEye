from typing import List, Optional
from decimal import Decimal
from datetime import date, datetime
from sqlmodel import Session, select, and_
from SteamEye.db.models.game_base import GameBase  # 替换为实际的模型导入路径


class GameBaseCRUD:
    """游戏基础信息表 CRUD 操作类（纯原子操作，无业务逻辑）"""

    @staticmethod
    def get_by_id(db: Session, game_id: int) -> Optional[GameBase]:
        """根据自增主键查询单条记录"""
        return db.get(GameBase, game_id)

    @staticmethod
    def get_by_steam_app_id(db: Session, steam_app_id: str) -> Optional[GameBase]:
        """根据Steam唯一ID查询（核心关联键）"""
        statement = select(GameBase).where(GameBase.steam_app_id == steam_app_id)
        return db.exec(statement).first()

    @staticmethod
    def list_by_developer(
        db: Session,
        developer: str,
        limit: int = 100,
        offset: int = 0
    ) -> List[GameBase]:
        """根据开发商查询多条记录（带分页）"""
        statement = (
            select(GameBase)
            .where(GameBase.developer == developer)
            .limit(limit)
            .offset(offset)
            .order_by(GameBase.global_release_date.desc())
        )
        return db.exec(statement).all()

    @staticmethod
    def list_by_release_date_range(
        db: Session,
        start_date: date,
        end_date: date,
        limit: int = 100,
        offset: int = 0
    ) -> List[GameBase]:
        """根据全球首发日期范围查询（带分页）"""
        statement = (
            select(GameBase)
            .where(
                and_(
                    GameBase.global_release_date >= start_date,
                    GameBase.global_release_date <= end_date
                )
            )
            .limit(limit)
            .offset(offset)
            .order_by(GameBase.global_release_date)
        )
        return db.exec(statement).all()

    @staticmethod
    def create(db: Session, game_data: GameBase) -> GameBase:
        """创建单条游戏基础信息记录"""
        db.add(game_data)
        db.commit()
        db.refresh(game_data)  # 刷新获取数据库自动生成的字段（如id、create_time）
        return game_data

    @staticmethod
    def update(
        db: Session,
        game_id: int,
        **kwargs
    ) -> Optional[GameBase]:
        """更新游戏基础信息（支持动态字段更新）"""
        game = db.get(GameBase, game_id)
        if not game:
            return None

        # 动态更新传入的字段（仅更新非None的字段）
        for key, value in kwargs.items():
            if hasattr(game, key) and value is not None:
                setattr(game, key, value)

        # 手动更新update_time（如果数据库未自动触发）
        game.update_time = datetime.now()
        
        db.commit()
        db.refresh(game)
        return game

    @staticmethod
    def delete_by_id(db: Session, game_id: int) -> bool:
        """根据主键删除记录"""
        game = db.get(GameBase, game_id)
        if not game:
            return False

        db.delete(game)
        db.commit()
        return True

    @staticmethod
    def delete_by_steam_app_id(db: Session, steam_app_id: str) -> bool:
        """根据Steam App ID删除记录"""
        statement = select(GameBase).where(GameBase.steam_app_id == steam_app_id)
        game = db.exec(statement).first()
        if not game:
            return False

        db.delete(game)
        db.commit()
        return True

if __name__ == "__main__":
