# 代码生成时间: 2025-09-22 11:01:27
from fastapi import FastAPI, HTTPException, status
from pydantic import BaseModel, ValidationError
from fastapi.responses import JSONResponse
from fastapi.encoders import jsonable_encoder
import json

# Pydantic模型定义
class ApiResponseModel(BaseModel):
    code: int
    message: str
    data: dict = {}

# 创建FastAPI应用实例
app = FastAPI()

# 错误处理器
@app.exception_handler(ValidationError)
async def validation_exception_handler(request, exc):
    error_message = jsonable_encoder({'detail': exc.errors()})
    return JSONResponse(content=error_message, status_code=status.HTTP_422_UNPROCESSABLE_ENTITY)

# API响应格式化工具端点
@app.post("/format-response")
async def format_response(data: dict):
    try:
        # 验证传入的数据是否为合法的字典
        if not isinstance(data, dict):
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Invalid data format. Expected a dictionary.")

        # 使用ApiResponseModel模型格式化响应
        model = ApiResponseModel(code=200, message="Success", data=data)
        # 将模型编码为JSON响应
        return JSONResponse(content=jsonable_encoder(model))
    except ValidationError as e:
        # 如果数据验证失败，返回错误信息
        return JSONResponse(content=jsonable_encoder({'code': 422, 'message': 'Validation Error', 'data': e.errors()}), status_code=status.HTTP_422_UNPROCESSABLE_ENTITY)
    except Exception as e:
        # 处理其他异常情况
# 增强安全性
        return JSONResponse(content=jsonable_encoder({'code': 500, 'message': 'Internal Server Error', 'data': str(e)}), status_code=status.HTTP_500_INTERNAL_SERVER_ERROR)
