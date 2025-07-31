# 代码生成时间: 2025-07-31 09:44:52
from fastapi import FastAPI, HTTPException, status
from fastapi.responses import JSONResponse
from fastapi.encoders import jsonable_encoder
from pydantic import BaseModel, ValidationError
from typing import Optional, List

app = FastAPI()

# Pydantic model
class Item(BaseModel):
    name: str
    description: Optional[str] = None
    price: float
    tax: Optional[float] = None

# API endpoint
@app.post("/items/")
async def create_item(item: Item):
    return jsonable_encoder(item)

# API documentation endpoint
@app.get("/items/")
async def read_items():
    return {"message": "All items"}

# Error handling
@app.exception_handler(ValidationError)
async def validation_exception_handler(request, exc: ValidationError):
    return JSONResponse(
        status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
        content=jsonable_encoder({"detail": exc.errors()}),
    )

# Test endpoint
@app.get("/test/")
async def test():
    return {"message": "Test endpoint is working"}
