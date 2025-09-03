# 代码生成时间: 2025-09-03 21:29:21
from fastapi import FastAPI, HTTPException, status
from fastapi.responses import JSONResponse
from pydantic import BaseModel
from typing import Optional

# Pydantic模型用于请求和响应数据校验
class Notification(BaseModel):
    title: str
    message: str
    recipient_id: Optional[int] = None

# 创建FastAPI实例
app = FastAPI()

# 错误处理器
@app.exception_handler(ValueError)
async def value_error_exception_handler(request, exc):
    return JSONResponse(
        status_code=status.HTTP_400_BAD_REQUEST,
        content={"message": str(exc)}
    )

# 消息通知系统端点
@app.post("/notify")
async def notify(notification: Notification):
    # 这里可以添加实际的逻辑来处理通知
    # 例如，保存通知、发送邮件等
    # 以下为模拟响应
    return {
        "title": notification.title,
        "message": notification.message,
        "recipient_id": notification.recipient_id
    }

# 启动FastAPI应用
if __name__ == '__main__':
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)