# 代码生成时间: 2025-08-24 11:04:31
from fastapi import FastAPI, HTTPException, status
from pydantic import BaseModel, ValidationError
from typing import Optional

app = FastAPI()

# Pydantic模型用于表单数据验证
class Item(BaseModel):
    name: str
    description: Optional[str] = None
    price: float
    tax: float = None

# API文档
@app.post("/items/")
async def create_item(item: Item):
    """
    Create an item.
    ### Request Body:
    - **name** : str
    - **description** : Optional[str]
    - **price** : float
    - **tax** : Optional[float]
    """
    return item.dict()

# 错误处理
@app.exception_handler(ValidationError)
async def validation_exception_handler(request, exc: ValidationError):
    return JSONResponse(
        status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
        content={"detail": exc.errors()}
    )

# 运行此服务器
if __name__ == '__main__':
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)