# 代码生成时间: 2025-08-15 10:36:56
from fastapi import FastAPI, HTTPException, Response
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from starlette.requests import Request
from starlette.responses import Response
from typing import List
from fastapi_cache import Cache, CacheSettings
from fastapi_cache.schemas import BaseCacheBackendSchema
from fastapi_cache.backends.memory import MemoryBackend
import time


# Define Pydantic model
class Item(BaseModel):
    name: str
    price: float
    description: str = None


# Create FastAPI app
app = FastAPI()
cache_settings = CacheSettings()
cache = Cache(backend=MemoryBackend(), settings=cache_settings)

# Add CORS middleware (optional)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Define API endpoint with caching
@app.get("/items")
@cache.cached(timeout=60, query_params=['name'])  # Caches the response for 60 seconds, based on the 'name' argument
async def read_item(name: str, request: Request):
    # Simulate a database call
    time.sleep(1)
    items = [
        Item(name="Item 1", price=10.5, description="An item"),
        Item(name="Item 2", price=12.0, description="Another item"),
    ]
    item = next((item for item in items if item.name == name), None)
    if not item:
        raise HTTPException(status_code=404, detail=f"Item {name} not found")
    return item

# Error handler for 404 errors
@app.exception_handler(404)
async def not_found_exception_handler(request: Request, exc: HTTPException):
    return JSONResponse(
        status_code=404,
        content={"detail": exc.detail},
    )

# Run Uvicorn server
if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)