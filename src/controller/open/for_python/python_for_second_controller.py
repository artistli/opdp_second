from fastapi import APIRouter
from fastapi.requests import Request

from src.common.utils.response_data import ResponseData
from src.model import schemas
from src.client.call_first_python_api import first_python_client

router = APIRouter()


@router.post("/for_python/add", response_model=schemas.ResponseModel, summary="for_python添加",
             description="for_python添加")
async def add(demo: schemas.Demo, request: Request):
    return ResponseData.get_successful_response(first_python_client.add(demo))


@router.delete("/for_python/{id}", response_model=schemas.ResponseModel, summary="for_python删除",
               description="for_python删除")
async def delete(id: int, request: Request):
    return ResponseData.get_successful_response(first_python_client.delete(id))


@router.get("/for_python/{id}", response_model=schemas.ResponseModel, summary="for_python获取详情",
            description="for_python获取详情")
async def get(id: int, request: Request):
    return ResponseData.get_successful_response(first_python_client.get(id))
