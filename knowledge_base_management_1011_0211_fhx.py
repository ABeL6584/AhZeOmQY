# 代码生成时间: 2025-10-11 02:11:28
from fastapi import FastAPI, HTTPException, status
from pydantic import BaseModel, Field
from typing import Optional
from fastapi.responses import JSONResponse

# Pydantic模型定义
class KnowledgeItem(BaseModel):
    id: int = Field(..., example=1, description="知识库条目的ID")
    title: str = Field(..., example="Example Title", max_length=100, description="条目的标题")
    content: str = Field(..., example="Example Content", description="条目的内容")
    tags: list[str] = Field(..., example=["example", "tag"], description="相关标签列表")

# 创建FastAPI应用实例
app = FastAPI()

# 知识库数据模拟
knowledge_base = {
    "1": {
        "title": "Example Title",
        "content": "Example Content",
        "tags": ["example", "tag"]
    }
}

# GET端点：获取所有知识库条目
@app.get("/items")
async def read_items():
    return knowledge_base.values()

# GET端点：通过ID获取知识库条目
@app.get("/items/{item_id}")
async def read_item(item_id: int):
    if item_id not in knowledge_base:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Item not found")
    return knowledge_base[item_id]

# POST端点：添加新知识库条目
@app.post("/items/")
async def create_item(item: KnowledgeItem):
    new_id = max(knowledge_base.keys()) + 1 if knowledge_base else 1
    knowledge_base[new_id] = {
        "title": item.title,
        "content": item.content,
        "tags": item.tags
    }
    return JSONResponse(
        status_code=status.HTTP_201_CREATED,
        content={"id": new_id, "item": knowledge_base[new_id]}
    )

# PUT端点：更新知识库条目
@app.put("/items/{item_id}")
async def update_item(item_id: int, item: KnowledgeItem):
    if item_id not in knowledge_base:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Item not found")
    knowledge_base[item_id] = {
        "title": item.title,
        "content": item.content,
        "tags": item.tags
    }
    return knowledge_base[item_id]

# DELETE端点：删除知识库条目
@app.delete("/items/{item_id}")
async def delete_item(item_id: int):
    if item_id not in knowledge_base:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Item not found")
    del knowledge_base[item_id]
    return {"detail": "Item deleted"}

# 错误处理
@app.exception_handler(404)
async def not_found(request: Request, exc: HTTPException):
    return JSONResponse(
        status_code=404,
        content={"detail": f"{request.method} {request.url} not found"}
    )

# 添加API文档
@app.get("/docs")
async def get_documentation():
    return JSONResponse(content={"message": "Visit /docs for Swagger UI", "docs_url": "/docs"})

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)