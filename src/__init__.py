#!/usr/bin/env python
# _*_ coding:utf-8 _*_
from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles

from src.settings.dev import DevelopementConfig
from src.settings.prop import ProductionConfig
from src import settings

from src.common.utils.response_data import register_exception

config_json = {
    "dev": DevelopementConfig,
    "prop": ProductionConfig,
}


def init_app(config_name):
    """项目的初始化函数"""
    # 设置配置类
    Config = config_json[config_name]
    settings.global_config = Config
    app = FastAPI(title=Config.TITLE_NAME, description=Config.DESCRIPTION, version=Config.LATEST_VERSION, openapi_url=Config.OPEN_API_URL)

    # app.mount("/%s" % (Config.STATIC_NAME), StaticFiles(directory=Config.STATIC_FOLDER), name=Config.STATIC_NAME)

    register_exception(app)
    from src.router.routers import router
    app.include_router(router, prefix=Config.OPEN_API_URL_PREFIX)

    return app, Config
