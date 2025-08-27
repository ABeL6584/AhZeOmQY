# 代码生成时间: 2025-08-27 16:52:40
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import List
from fastapi.responses import JSONResponse
from fastapi.encoders import jsonable_encoder

# Pydantic model for inventory item
class InventoryItem(BaseModel):
    id: int
    name: str
    quantity: int

# API instance
app = FastAPI()

# Mock inventory data
inventory_data = [
    {
        "id": 1,
        "name": "Widget",
        "quantity": 10
    },
    {
        "id": 2,
        "name": "Gadget",
        "quantity": 5
    }
]

# Get all inventory items
@app.get("/inventory")
async def read_inventory():
    return JSONResponse(content=jsonable_encoder(inventory_data))

# Get a specific inventory item
@app.get("/inventory/{item_id}")
async def read_inventory_item(item_id: int):
    item = next((item for item in inventory_data if item["id"] == item_id), None)
    if item is None:
        raise HTTPException(status_code=404, detail="Inventory item not found")
    return JSONResponse(content=jsonable_encoder(item))

# Add a new inventory item
@app.post("/inventory")
async def create_inventory_item(item: InventoryItem):
    if any(item["id"] == x["id"] for x in inventory_data):
        raise HTTPException(status_code=400, detail="Item already exists")
    inventory_data.append(item.dict())
    return JSONResponse(content=jsonable_encoder(item.dict()), status_code=201)

# Update an inventory item
@app.put("/inventory/{item_id}")
async def update_inventory_item(item_id: int, item: InventoryItem):
    for i, x in enumerate(inventory_data):
        if x["id"] == item_id:
            inventory_data[i] = item.dict()
            return JSONResponse(content=jsonable_encoder(item.dict()))
    raise HTTPException(status_code=404, detail="Inventory item not found")

# Delete an inventory item
@app.delete("/inventory/{item_id}")
async def delete_inventory_item(item_id: int):
    for i, x in enumerate(inventory_data):
        if x["id"] == item_id:
            del inventory_data[i]
            return JSONResponse(status_code=204)
    raise HTTPException(status_code=404, detail="Inventory item not found")