# 代码生成时间: 2025-08-28 03:05:28
from fastapi import FastAPI, HTTPException, APIRouter
from pydantic import BaseModel, Field
from typing import Optional
from fastapi.responses import JSONResponse
import psutil
import json
import uvicorn

# Define a Pydantic model for the system performance data
class SystemPerformance(BaseModel):
    cpu_usage: float = Field(..., description="CPU usage percentage")
    memory_usage: float = Field(..., description="Memory usage in percentage")
    disk_usage: float = Field(..., description="Disk usage in percentage")
    network_speed: str = Field(..., description="Network speed")

# Create a FastAPI app instance
app = FastAPI()

# Define a router for the system performance endpoint
router = APIRouter()

# Add a GET endpoint for system performance
@router.get("/monitor")
async def get_system_performance() -> SystemPerformance:
    """
    Returns the system performance data.
    """
    try:
        # Get CPU usage
        cpu_usage = psutil.cpu_percent(interval=1)
        
        # Get memory usage
        memory = psutil.virtual_memory()
        memory_usage = memory.percent
        
        # Get disk usage
        disk_usage = psutil.disk_usage('/').percent
        
        # Get network speed (this is a simplified example)
        network_speed = "100 Mbps"  # Replace with actual network speed calculation
        
        # Return the system performance data
        return SystemPerformance(
            cpu_usage=cpu_usage,
            memory_usage=memory_usage,
            disk_usage=disk_usage,
            network_speed=network_speed
        )
    except Exception as e:
        # Handle any exceptions and return an error response
        return JSONResponse(
            status_code=500,
            content=json.dumps({"message": str(e)})
        )

# Include the router in the FastAPI app
app.include_router(router)

# Run the FastAPI app
if __name__ == '__main__':
    uvicorn.run(app, host="0.0.0.0", port=8000)
