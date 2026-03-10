# 配置加载核心：根据环境变量自动加载对应配置
import os
from typing import Type
from .base import BaseSettings
from .dev import DevSettings
from .prod import ProdSettings
from .test import TestSettings

# 环境映射：ENV值 → 对应配置类
ENV_SETTINGS_MAP = {
    "dev": DevSettings,
    "prod": ProdSettings,
    "test": TestSettings,
}

# 加载配置（单例模式）
def load_settings() -> BaseSettings:
    env = os.getenv("PROJECT_ENV", "dev")  # 读取环境变量，默认dev
    settings_cls: Type[BaseSettings] = ENV_SETTINGS_MAP.get(env, DevSettings)
    return settings_cls()

# 全局配置实例（项目中直接导入这个实例使用）
settings = load_settings()