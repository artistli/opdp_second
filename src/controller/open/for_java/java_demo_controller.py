from fastapi import APIRouter
from fastapi.requests import Request

from src.common.utils.response_data import ResponseData
from src.model import schemas
from src.service.demo_service import  DemoService
router = APIRouter()


@router.post("/for_java/add", response_model=schemas.ResponseModel, summary="for_java添加", description="for_java添加")
async def add(demo: schemas.Demo, request: Request ):
    return ResponseData.get_successful_response(DemoService().add(demo))


@router.delete("/for_java/{id}", response_model=schemas.ResponseModel, summary="for_java删除", description="for_java删除")
async def delete(id: int , request: Request ):
    return ResponseData.get_successful_response(DemoService().delete(id))


@router.get("/for_java/{id}", response_model=schemas.ResponseModel, summary="for_java获取详情", description="for_java获取详情")
async def get(id: int , request: Request ):
    return ResponseData.get_successful_response(DemoService().get(id))