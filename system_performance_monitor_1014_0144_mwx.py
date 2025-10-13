# 代码生成时间: 2025-10-14 01:44:23
from fastapi import FastAPI, HTTPException, APIRouter
from pydantic import BaseModel
from typing import Optional
from datetime import datetime
import psutil
import uvloop; uvloop.install()


# Define Pydantic models
class SystemPerformance(BaseModel):
    timestamp: datetime
    cpu_usage: float
    memory_usage: float
    disk_usage: float


# Create FastAPI app
app = FastAPI()
router = APIRouter()


# Health check endpoint
@router.get("/health")
async def health_check():
    return {"status": "ok"}


# System performance endpoint
@router.get("/performance")
async def system_performance():
    cpu_usage = psutil.cpu_percent()
    memory = psutil.virtual_memory()
    disk_usage = psutil.disk_usage('/')
    
    return SystemPerformance(
        timestamp=datetime.now(),
        cpu_usage=cpu_usage,
        memory_usage=memory.percent,
        disk_usage=disk_usage.percent
    )


# Include router in app
app.include_router(router)


# Error handling
@app.exception_handler(Exception)
async def custom_exception_handler(request, exc):
    return HTTPException(
        status_code=500,
        detail="Internal Server Error"
    )

# If you need to handle specific exceptions like HTTPException, you can do it as follows:
# @app.exception_handler(HTTPException)
# async def http_exception_handler(request, exc):
#     return JSONResponse(
#         status_code=exc.status_code,
#         content={"detail": exc.detail}
#     )


# Run the app if this script is executed directly
if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)