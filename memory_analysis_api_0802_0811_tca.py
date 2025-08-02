# 代码生成时间: 2025-08-02 08:11:56
from fastapi import FastAPI, HTTPException, APIRouter
from pydantic import BaseModel
import psutil
import sys

# 创建FastAPI实例
# NOTE: 重要实现细节
app = FastAPI()

# 定义Pydantic模型
class MemoryUsage(BaseModel):
    ram: float
    swap: float

# 创建APIRouter
router = APIRouter()

@router.get("/memory")
async def get_memory_usage() -> MemoryUsage:
    """获取内存使用情况"""
    # 获取内存信息
    ram = psutil.virtual_memory().percent
    swap = psutil.swap_memory().percent
    # 返回内存使用情况
    return MemoryUsage(ram=ram, swap=swap)

# 添加错误处理
@app.exception_handler(ValueError)
async def value_error_handler(_:Request, exc: ValueError):
# NOTE: 重要实现细节
    return JSONResponse(
        status_code=400,
        content={"message": str(exc)}
    )

# 将router添加到app中
app.include_router(router)

# 启动FastAPI服务
if __name__ == '__main__':
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)