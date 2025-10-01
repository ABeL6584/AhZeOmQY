# 代码生成时间: 2025-10-02 03:54:24
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, ValidationError
from typing import Optional
from fastapi.responses import JSONResponse
from fastapi.encoders import jsonable_encoder

# Pydantic模型
class PriceInfo(BaseModel):
    item_id: int
    current_price: float
    previous_price: float
    change_percentage: Optional[float] = None

# 初始化FastAPI应用
app = FastAPI()

# 端点：监控价格变化并返回结果
@app.post("/monitor")
async def monitor_price(price_info: PriceInfo):
    # 错误处理：检查价格变化百分比是否有效
    if price_info.change_percentage and (price_info.change_percentage < -100 or price_info.change_percentage > 100):
        raise HTTPException(status_code=400, detail="Change percentage must be between -100 and 100")

    # 计算价格变化百分比（如果有需要）
    if not price_info.change_percentage:
        price_info.change_percentage = ((price_info.current_price - price_info.previous_price) / price_info.previous_price) * 100

    # 返回监控结果
    return jsonable_encoder(price_info)

# 错误处理：捕获Pydantic模型验证错误
@app.exception_handler(ValidationError)
async def validation_exception_handler(request, exc: ValidationError):
    return JSONResponse(status_code=422, content={"detail": exc.errors()})

# 错误处理：统一错误响应格式
@app.exception_handler(Exception)
async def general_exception_handler(request, exc):
    return JSONResponse(status_code=500, content={"detail": str(exc)})

# FastAPI文档页面
@app.get("/docs")
async def read_docs():
    return "API文档可以在 /docs 访问。"

# 运行FastAPI应用
if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)