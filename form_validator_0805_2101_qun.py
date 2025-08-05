# 代码生成时间: 2025-08-05 21:01:17
from fastapi import FastAPI, HTTPException, status
from fastapi.encoders import jsonable_encoder
from pydantic import BaseModel, ValidationError, validator
from typing import Optional
import json

app = FastAPI()

# Pydantic模型用于表单数据验证
class Item(BaseModel):
    name: str
    description: Optional[str] = None
    price: float
    tax: float = None

    # 验证器确保price和tax非负
    @validator('price', 'tax')
def validate_price(cls, value):
        if value < 0:
            raise ValueError('Price and tax should be non-negative')
        return value

# 错误处理
@app.exception_handler(ValidationError)
async def validation_exception_handler(request, exc: ValidationError):
    detail = jsonable_encoder(exc)
    raise HTTPException(status_code=status.HTTP_422_UNPROCESSABLE_ENTITY, detail=detail)

# FastAPI端点，包含API文档
@app.post("/items/")
async def create_item(item: Item):
    return {
        "name": item.name,
        "description": item.description,
        "price": item.price,
        "tax": item.tax,
    }
