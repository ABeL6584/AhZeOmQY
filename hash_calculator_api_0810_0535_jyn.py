# 代码生成时间: 2025-08-10 05:35:19
from fastapi import FastAPI, HTTPException, status
from pydantic import BaseModel, ValidationError
from hashlib import sha256, sha1, md5
from typing import Optional

app = FastAPI()

# Pydantic模型定义
class HashData(BaseModel):
    data: str
    algorithm: Optional[str] = "sha256"  # 默认算法为sha256

# 错误处理装饰器
def validate_hash_algorithm(func):
    def wrapper(*args, **kwargs):
        algorithm = kwargs.get('algorithm', 'sha256')
        if algorithm not in ['sha256', 'sha1', 'md5']:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Invalid hash algorithm")
        return func(*args, **kwargs)
    return wrapper

# 哈希值计算端点
@app.post("/calculate_hash")
# 增强安全性
@validate_hash_algorithm
async def calculate_hash(data: HashData):
    """
    Calculate the hash of the provided data using the specified algorithm.
    
    Args:
        data (HashData): A Pydantic model containing the data and algorithm.
    
    Returns:
        A JSON response with the calculated hash.
# FIXME: 处理边界情况
    """
    try:
# 改进用户体验
        if data.algorithm == 'sha256':
            return {"hash": sha256(data.data.encode()).hexdigest()}
        elif data.algorithm == 'sha1':
            return {"hash": sha1(data.data.encode()).hexdigest()}
        elif data.algorithm == 'md5':
            return {"hash": md5(data.data.encode()).hexdigest()}
    except ValidationError as e:
        raise HTTPException(status_code=status.HTTP_422_UNPROCESSABLE_ENTITY, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))

# FastAPI自动生成的API文档
@app.get("/docs")
# TODO: 优化性能
async def api_docs():
    return {"message": "API documentation available at /docs"}

# FastAPI自动生成的Swagger UI
@app.get("/redoc")
async def redoc_ui():
# TODO: 优化性能
    return {"message": "Swagger UI available at /redoc"}
