from fastapi import APIRouter
from fastapi.requests import Request

from src.common.utils.response_data import ResponseData
from src.model import schemas
from src.service.demo_service import DemoService

router = APIRouter()


@router.post("/call_python/add", response_model=schemas.ResponseModel, summary="call_python添加",
             description="call_python添加")
async def add(call_python: schemas.Demo, request: Request):
    return ResponseData.get_successful_response(DemoService().add(call_python))


@router.delete("/call_python/{id}", response_model=schemas.ResponseModel, summary="call_python删除",
               description="call_python删除")
async def delete(id: int, request: Request):
    return ResponseData.get_successful_response(DemoService().delete(id))


@router.get("/call_python/{id}", response_model=schemas.ResponseModel, summary="call_python获取详情",
            description="call_python获取详情")
async def get(id: int, request: Request):
    return ResponseData.get_successful_response(DemoService().get(id))


@router.get("/call_python", response_model=schemas.ResponseModel, summary="call_python获取所有",
            description="call_python获取所有")
async def get(request: Request):
    return ResponseData.get_successful_response(DemoService().get_all())
