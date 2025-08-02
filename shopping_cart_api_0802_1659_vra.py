# 代码生成时间: 2025-08-02 16:59:27
from fastapi import FastAPI, HTTPException, status
from fastapi.responses import JSONResponse
from pydantic import BaseModel
from typing import List, Optional

app = FastAPI()

# Pydantic模型定义
class CartItem(BaseModel):
    id: int
    name: str
    quantity: int
    price: float

class Cart(BaseModel):
    items: List[CartItem]

# 购物车数据
cart_data = []

# 获取购物车
@app.get("/cart")
async def get_cart():
    return cart_data

# 添加购物车商品
@app.post("/cart")
async def add_item_to_cart(item: CartItem):
    cart_data.append(item.dict())
    return item

# 更新购物车商品数量
@app.put("/cart/{item_id}")
async def update_item_in_cart(item_id: int, item: CartItem):
    for cart_item in cart_data:
        if cart_item['id'] == item_id:
            cart_item['quantity'] = item.quantity
            return cart_item
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Item not found")

# 删除购物车商品
@app.delete("/cart/{item_id}")
async def remove_item_from_cart(item_id: int):
    for i, cart_item in enumerate(cart_data):
        if cart_item['id'] == item_id:
            del cart_data[i]
            return JSONResponse(content={"detail": "Item removed"}, status_code=status.HTTP_200_OK)
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Item not found")

# 错误处理
@app.exception_handler(HTTPException)
async def custom_http_exception_handler(request: Request, exc: HTTPException):
    return JSONResponse(content={"detail": exc.detail}, status_code=exc.status_code)