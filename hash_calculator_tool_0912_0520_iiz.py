# 代码生成时间: 2025-09-12 05:20:55
from fastapi import FastAPI, HTTPException, APIRouter, Depends
from pydantic import BaseModel, Field
from hashlib import sha256, sha3_256
from typing import Optional

# 定义Pydantic模型
class HashData(BaseModel):
    data: str = Field(..., description="The data to be hashed")
    algorithm: str = Field("sha256", description="Hashing algorithm to use")

# 创建FastAPI应用
app = FastAPI()

# 定义路由
router = APIRouter()

# 添加FastAPI文档
app.include_router(router, prefix="/hash", tags=["hash"])

# 定义哈希计算端点
@router.post("/calculate")
async def calculate_hash(hash_data: HashData):
    # 根据选择的算法计算哈希值
    if hash_data.algorithm == "sha256":
        hash = sha256(hash_data.data.encode()).hexdigest()
    elif hash_data.algorithm == "sha3_256":
        hash = sha3_256(hash_data.data.encode()).hexdigest()
    else:
        raise HTTPException(status_code=400, detail="Unsupported hashing algorithm")
    
    # 返回哈希值
    return {"hash": hash}

# 错误处理
@app.exception_handler(ValueError)
async def value_error_handler(request, exc):
    return JSONResponse(
        status_code=400,
        content={"detail": str(exc)}
    )

# 运行应用
if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)