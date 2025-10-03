# 代码生成时间: 2025-10-03 19:44:41
from fastapi import FastAPI, HTTPException, APIRouter
from pydantic import BaseModel, ValidationError
from shutil import disk_usage
import json

# Pydantic模型定义
class DiskSpace(BaseModel):
    total: float  # 总磁盘空间
    used: float  # 已用磁盘空间
    free: float  # 可用磁盘空间
    percentage: float  # 已用磁盘空间百分比

# 创建FastAPI应用
app = FastAPI()
router = APIRouter()

# 添加磁盘空间管理端点
@router.get("/disk-space", summary="获取磁盘空间信息", response_model=DiskSpace)
async def get_disk_space():
    """
    获取磁盘空间信息
    
    返回一个DiskSpace对象，包含总磁盘空间、已用磁盘空间、可用磁盘空间和已用磁盘空间百分比。
    """
    try:
        du = disk_usage('/')  # 获取根目录磁盘空间信息
        return {
            "total": du.total / (1024 ** 3),  # 转换为GB
            "used": du.used / (1024 ** 3),
            "free": du.free / (1024 ** 3),
            "percentage": du.percent
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# 添加错误处理
@app.exception_handler(ValidationError)
async def validation_exception_handler(request, exc):
    return JSONResponse(
        status_code=400,
        content={"message": "验证失败", "errors": exc.errors()}
    )

# 将router添加到app中
app.include_router(router)

# 运行FastAPI应用
if __name__ == '__main__':
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)