from __future__ import annotations

import sys
import os
from pathlib import Path
from typing import Dict, Any, Optional, Callable, Union, List

from loguru import logger as _logger


# 移除默認的 handler
_logger.remove()

# 設定默認的日誌格式
DEFAULT_FORMAT = (
    "<green>{time:YYYY-MM-DD HH:mm:ss.SSS}</green> | "
    "<level>{level: <8}</level> | "
    "<cyan>{name}</cyan>:<cyan>{function}</cyan>:<cyan>{line}</cyan> - "
    "<level>{message}</level>"
)

# 添加控制台輸出
_logger.add(
    sys.stderr,
    format=DEFAULT_FORMAT,
    level=os.getenv("LOG_LEVEL", "INFO"),
    enqueue=True,
)


class Logger:
    """自定義 Logger 封裝 loguru"""

    def __init__(self) -> None:
        self._logger = _logger

    def configure_output(
        self,
        sink: Union[str, Path, Callable, Any],
        level: str = "INFO",
        format: str = DEFAULT_FORMAT,
        rotation: Optional[str] = None,
        retention: Optional[str] = None,
        filter: Optional[Union[str, Callable, Dict[str, str]]] = None,
        **kwargs,
    ) -> int:
        """添加一個自訂的日誌輸出

        Args:
            sink: 日誌輸出目標 (文件路徑、函數等)
            level: 日誌級別
            format: 日誌格式
            rotation: 日誌輪換設置 (例如 "500 MB", "1 week")
            retention: 日誌保留設置 (例如 "10 days")
            filter: 過濾特定記錄的函數或字典
            **kwargs: 傳遞給 loguru.add 的其他參數

        Returns:
            handler_id: 處理器ID，可用於後續移除
        """
        return self._logger.add(
            sink=sink,
            level=level,
            format=format,
            rotation=rotation,
            retention=retention,
            filter=filter,
            **kwargs,
        )

    def remove_output(self, handler_id: int) -> None:
        """移除指定的日誌輸出

        Args:
            handler_id: 通過 configure_output 返回的處理器ID
        """
        self._logger.remove(handler_id)

    def debug(self, message: str, *args, **kwargs) -> None:
        self._logger.debug(message, *args, **kwargs)

    def info(self, message: str, *args, **kwargs) -> None:
        self._logger.info(message, *args, **kwargs)

    def warning(self, message: str, *args, **kwargs) -> None:
        self._logger.warning(message, *args, **kwargs)

    def error(self, message: str, *args, **kwargs) -> None:
        self._logger.error(message, *args, **kwargs)

    def critical(self, message: str, *args, **kwargs) -> None:
        self._logger.critical(message, *args, **kwargs)

    def exception(self, message: str, *args, **kwargs) -> None:
        self._logger.exception(message, *args, **kwargs)

    def bind(self, **kwargs) -> Logger:
        """創建一個帶有上下文變量的 logger 實例"""
        bound_logger = Logger()
        bound_logger._logger = self._logger.bind(**kwargs)
        return bound_logger


# 創建默認的 logger 實例
logger = Logger()

# 方便直接導入使用
__all__ = ["logger", "Logger"]

"""
使用範例說明
============

1. 基本用法
-----------
from app.core.logger import logger

# 輸出不同級別的日誌
logger.debug("這是一條調試信息")
logger.info("這是一條普通信息")
logger.warning("這是一條警告信息")
logger.error("這是一條錯誤信息")
logger.critical("這是一條嚴重錯誤信息")

# 帶參數的格式化輸出
user_id = 1234
logger.info(f"用戶 {user_id} 登入系統")
# 或使用 loguru 的格式化語法
logger.info("用戶 {} 登入系統", user_id)

# 輸出異常信息
try:
    1 / 0
except Exception:
    logger.exception("除以零錯誤")

2. 配置自定義輸出
----------------
# 輸出到文件
file_handler_id = logger.configure_output(
    "logs/app.log",
    level="INFO",
    rotation="500 MB",  # 當文件達到 500MB 時輪替
    retention="10 days",  # 保留 10 天的日誌
)

# 輸出到函數
def notify_admin(message):
    # 發送重要日誌到管理員
    pass

critical_handler_id = logger.configure_output(
    notify_admin,
    level="CRITICAL",
    format="{message}"  # 簡化格式只輸出消息
)

# 自定義過濾器
def only_auth_module(record):
    return "auth" in record["name"]

auth_handler_id = logger.configure_output(
    "logs/auth.log",
    level="DEBUG",
    filter=only_auth_module
)

3. 使用上下文綁定
----------------
# 在整個請求處理過程中跟蹤用戶
user_logger = logger.bind(user_id="12345", request_id="abc-123")
user_logger.info("用戶開始請求")
user_logger.info("請求處理完成")

# 在處理特定模塊時添加模塊標識
db_logger = logger.bind(module="database")
db_logger.info("執行數據庫查詢")

4. 移除輸出
----------
# 當不再需要某個輸出時，可以移除它
logger.remove_output(file_handler_id)
logger.remove_output(critical_handler_id)
"""
