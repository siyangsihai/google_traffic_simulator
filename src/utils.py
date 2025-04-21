# -*- coding: utf-8 -*-
"""
实用工具模块
包含日志设置和代理轮换功能
"""

import logging
import random
from logging.handlers import RotatingFileHandler


def setup_logging(log_level, log_file):
    """
    配置日志系统
    
    Args:
        log_level: 日志级别 (logging.DEBUG/INFO/WARNING/ERROR/CRITICAL)
        log_file: 日志文件路径
    
    Returns:
        Logger对象
    """
    logger = logging.getLogger('google_traffic')
    logger.setLevel(log_level)
    
    # 文件处理器
    file_handler = RotatingFileHandler(
        log_file, maxBytes=10*1024*1024, backupCount=5
    )
    file_handler.setFormatter(logging.Formatter(
        '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    ))
    logger.addHandler(file_handler)
    
    # 控制台处理器
    console_handler = logging.StreamHandler()
    console_handler.setFormatter(logging.Formatter(
        '%(levelname)s - %(message)s'
    ))
    logger.addHandler(console_handler)
    
    return logger


def rotate_proxy(proxies):
    """
    从代理列表中随机选择一个代理
    
    Args:
        proxies: 代理列表
    
    Returns:
        随机选择的代理字符串，如果没有代理则返回None
    """
    if not proxies:
        return None
    return random.choice(proxies)