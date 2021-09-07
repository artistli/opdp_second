#!/usr/bin/env python
# _*_ coding:utf-8 _*_

import os
from datetime import timedelta

from redis import StrictRedis


class Config(object):
    """项目配置核心类"""
    # 调试模式
    DEBUG = True

    FASTAPI_PORT = 9905
    FASTAPI_HOST = "0.0.0.0"

    # 配置日志
    LOG_LEVEL = "DEBUG"
    TITLE_NAME = "OPDP_FASTAPI_SERVICE_SECOND"
    DESCRIPTION = "OPDP_FAST_API_SECOND_DEMO后端接口"
    VERSION = "1.0"
    LATEST_VERSION = VERSION
    OPEN_API_URL = "/api/v1/opdp_fastapi_second"
    OPEN_API_URL_PREFIX = OPEN_API_URL
    STATIC_NAME = 'static'
    HERE = os.path.abspath(os.path.dirname(os.path.dirname(os.path.dirname(__file__))))
    STATIC_FOLDER = os.path.join(os.path.dirname(HERE), STATIC_NAME)
global_config = None

opdp_query_client = None
opdp_modify_client = None
c2c_query_client = None
c2c_modify_client = None
