#!/usr/bin/env python
# _*_ coding:utf-8 _*_

from . import Config


class ProductionConfig(Config):
    """生产模式下的配置"""
    DEBUG = True
