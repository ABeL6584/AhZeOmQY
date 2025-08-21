# 代码生成时间: 2025-08-21 09:14:28
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from fastapi.responses import JSONResponse
from fastapi.openapi.utils import get_openapi
import uvicorn

# Pydantic模型定义，用于请求和响应数据的验证
class ChartRequest(BaseModel):
    data: list = []  # 数据列表
    title: str = ""  # 图表标题
    type: str = "line"  # 图表类型

# 创建FastAPI应用实例
app = FastAPI()

# 自定义异常处理
@app.exception_handler(ValueError)
async def value_error_handler(request, exc):
    return JSONResponse(
        status_code=400,
        content={"message": str(exc)}
    )

# 交互式图表生成器端点
@app.post("/generate-chart/")
async def generate_chart(request: ChartRequest):
    # 验证请求数据
    if not request.data or not request.title:
        raise HTTPException(status_code=400, detail="Data and title are required")

    # 模拟图表生成过程（这里仅作为示例）
    chart_data = {
        "title": request.title,
        "type": request.type,
        "data": request.data,
    }
    return chart_data

# 修改OpenAPI文档中的API服务器URL
def custom_openapi():
    if app.openapi_schema:
        yield from app.openapi_schema
        app.openapi_schema["info