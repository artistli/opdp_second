from datetime import datetime
from typing import Dict, List, Union, Optional

from pydantic import BaseModel


class Demo(BaseModel):
    id: Optional[int]
    name: str = ''
    age: int = 10
    serviceProvider: Optional[str]

# 按照规范，制定所有返回值模型
class ResponseModel(BaseModel):
    total: int = 0
    result: bool
    code: int
    message: str
    data: Union[List, Dict]

    class Config:
        orm_mode = True  # 开启orm映射