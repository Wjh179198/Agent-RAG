import os
from datetime import datetime

from utils.path_tool_util import get_project_root
import logging

# 日志保存的根目录
LOG_ROOT = get_project_root()

# 确保保存日志的目录存在
os.makedirs(LOG_ROOT, exist_ok=True)

DEFAULT_LOG_FORMAT = logging.Formatter(
    "%(asctime)s - %(name)s - %(levelname)s - %(filename)s:%(lineno)d - %(message)s"
)

def get_logger(
        name: str = "agent",
        console_level: int = logging.INFO,
        file_level: int = logging.DEBUG,
        log_file = None
) -> logging.Logger:
    logger = logging.getLogger(name)
    logger.setLevel(logging.DEBUG)

    # 避免重复添加日志
    if logger.handlers:
        return logger

    # 控制台logger
    console_logger = logging.StreamHandler()
    console_logger.setLevel(console_level)
    console_logger.setFormatter(DEFAULT_LOG_FORMAT)
    logger.addHandler(console_logger)

    # 文件logger
    if not log_file:
        log_file = os.path.join(LOG_ROOT, f"{name}_{datetime.now().strftime('%Y%m%d')}.log")

    file_logger = logging.FileHandler(log_file)
    file_logger.setLevel(file_level)
    file_logger.setFormatter(DEFAULT_LOG_FORMAT)
    logger.addHandler(file_logger)

    return logger

# 快捷获取日志管理器
logger = get_logger()