#!/usr/bin/env python
# _*_ coding:utf-8 _*_

import os

from . import Config


class DevelopementConfig(Config):
    """开发模式下的配置"""
    # 查询时会显示原始SQL语句
    FASTAPI_PORT = 9906
