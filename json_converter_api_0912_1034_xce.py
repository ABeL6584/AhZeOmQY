# 代码生成时间: 2025-09-12 10:34:21
from fastapi import FastAPI, HTTPException, status
from pydantic import BaseModel, ValidationError
from typing import Any, Dict
import json


# Pydantic 模型用于数据校验和转换
class JSONConverterModel(BaseModel):
    json_data: str

# 创建 FastAPI 应用
app = FastAPI()

# 创建一个端点用于 JSON 数据格式转换
@app.post("/convert")
async def convert_json(json_converter: JSONConverterModel):
    try:
        # 尝试解析 JSON 字符串
        data = json.loads(json_converter.json_data)
    except json.JSONDecodeError as e:
        # 错误处理：如果 JSON 字符串无效，则抛出 HTTP 错误
        raise HTTPException(status_code=status.HTTP_422_UNPROCESSABLE_ENTITY, 
                            detail=f"Invalid JSON data: {e}")
    except ValidationError as e:
        # 错误处理：如果 Pydantic 模型验证失败，则抛出 HTTP 错误
        raise HTTPException(status_code=status.HTTP_422_UNPROCESSABLE_ENTITY, 
                            detail=f"Invalid data format: {e}")
    return {
        "original": json_converter.json_data,
        "converted": data
    }

# 添加错误处理中间件
@app.exception_handler(ValidationError)
async def validation_exception_handler(request, exc):
    return JSONResponse(
        status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
        content={"detail": exc.errors()}
    )

# 添加异常处理器以提供更友好的错误信息
@app.exception_handler(HTTPException)
async def http_exception_handler(request, exc):
    return JSONResponse(
        status_code=exc.status_code,
        content={"detail": exc.detail}
    )

# FastAPI 应用自动生成 API 文档和 Swagger UI
# 可以通过 /docs 和 /redoc 访问
