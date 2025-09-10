# 代码生成时间: 2025-09-10 20:37:25
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from random import randint


# Pydantic模型定义
class RandomNumberParams(BaseModel):
    min: int = 1
    max: int = 100

# FastAPI应用实例
app = FastAPI()

# 随机数生成器端点
@app.get("/random")
async def generate_random_number(params: RandomNumberParams):
    """
    根据给定的范围生成一个随机数。
    
    Args:
        params (RandomNumberParams): 包含最小值和最大值参数的Pydantic模型。
    
    Returns:
        dict: 包含随机数的字典。
    
    Raises:
        HTTPException: 如果参数不正确，抛出400错误。
    """
    if params.min >= params.max:
        raise HTTPException(status_code=400, detail="Minimum value must be less than maximum value.")
    random_number = randint(params.min, params.max)
    return {"random_number": random_number}

# 错误处理
@app.exception_handler(ValueError)
async def value_error_handler(request, exc):
    return JSONResponse(
        content={"detail": str(exc)},
        status_code=400,
    )

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)