# 代码生成时间: 2025-08-04 09:32:00
from fastapi import FastAPI, HTTPException, status
from pydantic import BaseModel, ValidationError
from fastapi.responses import JSONResponse
def validation_exception_handler(request, exc):
    # 错误处理函数
    return JSONResponse(
        content={"message": exc.errors()[0]['msg'], "type": exc.errors()[0]['type']},
        status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
    )

app = FastAPI()
app.add_exception_handler(ValidationError, validation_exception_handler)

class Item(BaseModel):
    name: str = None
    description: str = None
    price: float = None
    tax: float = None

@app.post("/items/")
async def create_item(item: Item):
    # 表单数据验证器
    try:
        # 尝试验证数据
        item = Item(**item.dict())
    except ValidationError as e:
        # 如果验证失败，则抛出HTTPException
        raise HTTPException(status_code=status.HTTP_422_UNPROCESSABLE_ENTITY, detail=str(e))

    # 返回验证成功的消息和数据
    return {"name": item.name, "description": item.description, "price": item.price, "tax": item.tax}

# 以下为FastAPI自动生成的API文档
@app.get("/docs")
async def swagger_ui():
    return {"redirect": "/docs"}

@app.get("/redoc")
async def redoc():
    return {"redirect": "/redoc"}
