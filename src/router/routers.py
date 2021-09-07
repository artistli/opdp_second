# -*- coding:UTF-8 -*-
"""
@see: 路由配置
@author: 孙留平
"""
from fastapi import APIRouter
from src.controller import demo_controller
from src.controller.open.for_java import java_demo_controller
from src.controller.open.for_python import python_for_second_controller
from src.controller import python_controller

router = APIRouter()

router.include_router(demo_controller.router, tags=["Demo"])
router.include_router(java_demo_controller.router, tags=["JAVA_DEMO"])
router.include_router(python_for_second_controller.router, tags=["PYTHON_DEMO"])
router.include_router(python_controller.router, tags=["PYTHON_CONTROLLER"])
