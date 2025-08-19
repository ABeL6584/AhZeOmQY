# 代码生成时间: 2025-08-19 22:26:46
from fastapi import FastAPI, HTTPException, status
from pydantic import BaseModel
from datetime import datetime
import logging

# 设置日志记录
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Pydantic模型定义
class AuditLog(BaseModel):
    action: str
    user_id: int
    timestamp: datetime
    details: dict

# 创建FastAPI应用实例
app = FastAPI(title="Audit Log API", version="1.0.0")

# 审计日志存储列表
audit_logs = []

@app.post("/log/")
async def log_audit(audit: AuditLog):
    """记录安全审计日志"""
    # 将日志存储到列表中
    audit_logs.append(audit.dict())
    # 日志记录
    logger.info(f"Logged action: {audit.action}, user_id: {audit.user_id}")
    return {
        "message": "Audit log recorded successfully",
        "data": audit.dict()
    }

@app.get("/logs/")
async def get_audit_logs():
    """获取所有安全审计日志"""
    return audit_logs

@app.exception_handler(HTTPException)
async def http_exception_handler(request, exc):
    """错误处理器"""
    logger.error(f"HTTPException: {exc.detail}")
    return JSONResponse(
        status_code=exc.status_code,
        content={"message": exc.detail}
    )

# 添加错误处理响应模型
from starlette.responses import JSONResponse