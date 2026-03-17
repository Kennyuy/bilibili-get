#!/usr/bin/env python3
"""
配置文件
从环境变量读取配置
"""

import os
from typing import Optional


class Settings:
    """应用配置"""
    
    # 服务配置
    HOST: str = os.getenv("API_HOST", "0.0.0.0")
    PORT: int = int(os.getenv("API_PORT", "8000"))
    DEBUG: bool = os.getenv("DEBUG", "false").lower() == "true"
    
    # API 认证（可选）
    API_KEY: Optional[str] = os.getenv("API_KEY")
    API_KEY_HEADER: str = os.getenv("API_KEY_HEADER", "X-API-Key")
    
    # 下载配置
    DOWNLOAD_DIR: str = os.getenv("DOWNLOAD_DIR", "/tmp/bilibili_downloads")
    DOWNLOAD_TIMEOUT: int = int(os.getenv("DOWNLOAD_TIMEOUT", "600"))
    
    # Cookie 文件路径（可选）
    COOKIES_FILE: Optional[str] = os.getenv("COOKIES_FILE")
    
    # 日志配置
    LOG_LEVEL: str = os.getenv("LOG_LEVEL", "INFO")
    
    # Coze 配置
    COZE_WEBHOOK_ENABLED: bool = os.getenv("COZE_WEBHOOK_ENABLED", "true").lower() == "true"


settings = Settings()
