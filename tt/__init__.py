"""
TT - Telegram 自动化工具库

提供 Telegram 自动化开发所需的基础功能：
- 数据库操作
- Telegram 客户端封装
- 日志管理
- 配置管理
- 应用框架
"""

__version__ = '0.1.0'

from .db import DB
from .client import TGClient
from .log import Logger, err, info, warn, debug, exception, setup_telethon_logger, get_now
from .config import Config
from .app import TelegramApp, TaskManager

__all__ = [
    # 数据库
    'DB',
    
    # Telegram 客户端
    'TGClient',
    
    # 日志
    'Logger',
    'err',
    'info',
    'warn',
    'debug',
    'exception',
    'setup_telethon_logger',
    'get_now',
    
    # 配置
    'Config',
    
    # 应用框架
    'TelegramApp',
    'TaskManager',
]

