# 代码生成时间: 2025-09-03 05:31:25
from fastapi import FastAPI, HTTPException, APIRouter
from pydantic import BaseModel
from random import randint, choice
from typing import List

# Pydantic 模型定义
class RandomNumberRequest(BaseModel):
    numbers: int  # 生成随机数的数量
    min_value: int = 1  # 最小值
    max_value: int = 100  # 最大值

class RandomNumberResponse(BaseModel):
    numbers: List[int]  # 随机数列表

# FastAPI 实例
app = FastAPI()

# API 路由
router = APIRouter()

# 随机数生成器端点
@router.post("/generate")
async def generate_random_numbers(request: RandomNumberRequest) -> RandomNumberResponse:
    try:
        # 检查最小值和最大值是否合理
        if request.min_value >= request.max_value:
            raise ValueError("Minimum value must be less than maximum value.")

        # 生成随机数列表
        random_numbers = [
            randint(request.min_value, request.max_value)
            for _ in range(request.numbers)
        ]
        return RandomNumberResponse(numbers=random_numbers)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

# 将路由添加到FastAPI应用
app.include_router(router)

# 运行时可以通过命令行使用 uvicorn random_number_generator:app 启动服务