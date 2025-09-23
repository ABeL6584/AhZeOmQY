# 代码生成时间: 2025-09-23 22:18:44
from fastapi import FastAPI, HTTPException, status
from pydantic import BaseModel
from typing import Optional
import logging
from fastapi.responses import JSONResponse

# 创建日志配置
logging.basicConfig(level=logging.ERROR, format='%(asctime)s - %(levelname)s - %(message)s')

# 创建Pydantic模型
class ErrorLog(BaseModel):
    error_message: str
    error_type: str
    user_id: Optional[int] = None

# 创建FastAPI应用
app = FastAPI()

# 创建错误日志收集器端点
@app.post("/error-logs")
async def log_error(error_log: ErrorLog):
    # 记录错误日志
    logging.error(f"Error from user {error_log.user_id}: {error_log.error_message} ({error_log.error_type})")
    # 返回成功响应
    return JSONResponse(content={"message": "Error logged successfully"}, status_code=status.HTTP_200_OK)

# 添加错误处理
@app.exception_handler(HTTPException)
async def http_exception_handler(request, exc):
    # 记录异常信息
    logging.error(f"HTTP Exception: {exc.detail}")
    # 返回错误信息给客户端
    return JSONResponse(content={"detail": exc.detail}, status_code=exc.status_code)

if __name__ == '__main__':
    import uvicorn
    uvicorn.run(app, host='0.0.0.0', port=8000)