from fastapi import APIRouter
from fastapi.requests import Request

from src.common.utils.response_data import ResponseData
from src.model import schemas
from src.service.demo_service import  DemoService
router = APIRouter()


@router.post("/demo/add", response_model=schemas.ResponseModel, summary="demo添加", description="demo添加")
async def add(demo: schemas.Demo, request: Request ):
    return ResponseData.get_successful_response(DemoService().add(demo))


@router.delete("/demo/{id}", response_model=schemas.ResponseModel, summary="demo删除", description="demo删除")
async def delete(id: int , request: Request ):
    return ResponseData.get_successful_response(DemoService().delete(id))


@router.get("/demo/{id}", response_model=schemas.ResponseModel, summary="demo获取详情", description="demo获取详情")
async def get(id: int , request: Request ):
    return ResponseData.get_successful_response(DemoService().get(id))


@router.get("/demo", response_model=schemas.ResponseModel, summary="demo获取所有", description="demo获取所有")
async def get(request: Request ):
    return ResponseData.get_successful_response(DemoService().get_all())