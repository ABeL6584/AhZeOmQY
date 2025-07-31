# 代码生成时间: 2025-07-31 20:37:50
from fastapi import FastAPI, HTTPException, status
from pydantic import BaseModel
from typing import Optional

# Pydantic模型定义
class Item(BaseModel):
    name: str
    description: Optional[str] = None
    price: float
    tax: Optional[float] = None

# FastAPI实例化
app = FastAPI()

# API文档自动生成
@app.get("/items/")
async def read_items():
    return {
        "message": "Hello World"
    }

@app.get("/items/{item_id}")
async def read_item(item_id: int):
    if item_id == 42:
        return {
            "id": item_id,
            "name": "Foo"
        }
    else:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Item not found")

@app.post("/items/")
async def create_item(item: Item):
    return {
        "name": item.name,
        "description": item.description,
        "price": item.price,
        "tax": item.tax
    }

# 错误处理
@app.exception_handler(404)
async def not_found_exception_handler(request, exc):
    return {
        "message": "Item not found",
        "error": exc.detail
    }, 404

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)