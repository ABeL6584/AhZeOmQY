# 代码生成时间: 2025-09-20 14:12:41
from fastapi import FastAPI, HTTPException, APIRouter
from pydantic import BaseModel, Field
from typing import Optional
import psutil
import platform
import time

# Pydantic model for system information
class SystemInfo(BaseModel):
    current_time: str = Field(description="Current system time")
    cpu_usage: float = Field(description="CPU usage percentage")
    memory_usage: float = Field(description="Memory usage percentage")
    disk_usage: float = Field(description="Disk usage percentage")

# API router
router = APIRouter()

# FastAPI instance
app = FastAPI(title="System Performance Monitor", description="API for monitoring system performance")
app.include_router(router)

# Endpoint to get system information
@router.get("/system_info")
async def get_system_info():
    # Get system information
    cpu_usage = psutil.cpu_percent()
    memory = psutil.virtual_memory()
    memory_usage = memory.percent
    disk = psutil.disk_usage('/')
    disk_usage = disk.percent
    current_time = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())

    # Create a SystemInfo instance
    system_info = SystemInfo(
        current_time=current_time,
        cpu_usage=cpu_usage,
        memory_usage=memory_usage,
        disk_usage=disk_usage
    )
    return system_info

# Error handler
@app.exception_handler(ValueError)
async def value_error_handler(request, exc):
    return JSONResponse(
        status_code=400,
        content={"message": str(exc)}
    )

# Run the application
if __name__ == '__main__':
    import uvicorn
    uvicorn.run(app, host="0.0.1.0", port=8000)