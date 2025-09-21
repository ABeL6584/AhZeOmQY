# 代码生成时间: 2025-09-22 02:56:01
from fastapi import FastAPI, HTTPException, status
from pydantic import BaseModel
from typing import Optional

# Pydantic模型定义
class Item(BaseModel):
    id: int
    name: str
    description: Optional[str] = None
    price: float
    is_offer: bool = False

# 创建FastAPI应用
app = FastAPI()

# 模拟数据库
items_db = {
    "1": {
        "id": 1,
        "name": "Item 1",
        "description": "This is item 1",
        "price": 10.0,
        "is_offer": False
    },
    "2": {
        "id": 2,
        "name": "Item 2",
        "description": "This is item 2",
        "price": 20.0,
        "is_offer": True
    }
}

# 获取单个项目的端点
@app.get("/items/{item_id}")
async def read_item(item_id: int):
    item = items_db.get(str(item_id))
    if item is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Item not found")
    return item

# 获取所有项目的端点
@app.get("/items")
async def read_items():
    return list(items_db.values())

# 添加新项目的端点
@app.post("/items/")
async def create_item(item: Item):
    new_id = max(int(item_id) for item_id in items_db) + 1
    new_item = item.dict()
    new_item['id'] = new_id
    items_db[str(new_id)] = new_item
    return new_item

# 错误处理
@app.exception_handler(HTTPException)
async def http_exception_handler(request, exc):
    return JSONResponse(
        status_code=exc.status_code,
        content={"detail": exc.detail}
    )

# 运行uvicorn服务器
# 例如：uvicorn restful_api:app --reload
