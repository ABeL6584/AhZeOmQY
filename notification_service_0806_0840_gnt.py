# 代码生成时间: 2025-08-06 08:40:38
from fastapi import FastAPI, HTTPException, status
from pydantic import BaseModel
from typing import Optional
from fastapi.responses import JSONResponse
from fastapi.encoders import jsonable_encoder

# Pydantic模型定义通知消息
class Notification(BaseModel):
    title: str
    content: str
    priority: Optional[str] = None

# 初始化FastAPI应用
app = FastAPI()

# 创建通知的端点
@app.post("/notify/")
async def create_notification(notification: Notification):
    # 模拟创建通知的过程
    notification_data = jsonable_encoder(notification)
    return JSONResponse(content=notification_data, status_code=status.HTTP_201_CREATED)

# 错误处理
@app.exception_handler(ValueError)
async def validation_exception_handler(request, exc):
    return JSONResponse(
        content={"message": str(exc), "errors": "Validation failed"},
        status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
    )

# 启动文档服务器，支持自动API文档
if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)