# 代码生成时间: 2025-09-23 01:28:20
from fastapi import FastAPI, HTTPException, status
from pydantic import BaseModel
from typing import List
import plotly.graph_objects as go

# Pydantic模型定义
class ChartData(BaseModel):
    x_data: List[float]
    y_data: List[float]
    chart_type: str = "line"  # 默认为线图

# 创建FastAPI应用
app = FastAPI()

# 交互式图表生成器端点
@app.post("/generate-chart/")
async def generate_chart(data: ChartData):
    # 检查图表类型
    if data.chart_type not in ["line", "bar", "scatter"]:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Unsupported chart type.")

    # 根据图表类型创建图表
    if data.chart_type == "line":
        chart = go.Figure(data=[go.Scatter(x=data.x_data, y=data.y_data)])
    elif data.chart_type == "bar":
        chart = go.Figure(data=[go.Bar(x=data.x_data, y=data.y_data)])
    elif data.chart_type == "scatter":
        chart = go.Figure(data=[go.Scatter(x=data.x_data, y=data.y_data, mode="markers")])

    # 使图表可交互
    chart.update_layout(dragmode='pan')
    chart_div = chart.to_html(full_html=False)  # 生成HTML内容，不包含HTML标签

    return {
        "chart_html": chart_div,
        "message": "Interactive chart generated successfully."
    }


# 错误处理
@app.exception_handler(ValueError)
async def value_error_handler(request, exc):
    return JSONResponse(
        status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
        content={"detail": exc.args[0], "message": "Invalid input."}
    )

# 健康检查端点
@app.get("/health")
async def health_check():
    return {"status": "ok"}