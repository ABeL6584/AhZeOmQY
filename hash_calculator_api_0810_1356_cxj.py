# 代码生成时间: 2025-08-10 13:56:43
from fastapi import FastAPI, HTTPException, status
from pydantic import BaseModel
from hashlib import sha256
from typing import Optional

# Pydantic模型用于输入数据
class HashInput(BaseModel):
    text: str
    algorithm: Optional[str] = "sha256"  # 默认使用SHA-256算法

# 创建FastAPI应用
app = FastAPI()

# 哈希值计算端点
@app.post("/calculate_hash")
async def calculate_hash(input: HashInput):
    # 根据选择的算法计算哈希值
    try:
        if input.algorithm == "sha256":
            hash_object = sha256(input.text.encode())
        else:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Unsupported algorithm")
        # 返回计算得到的哈希值
        return {"hash": hash_object.hexdigest()}
    except Exception as e:
        # 错误处理
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))

# Swagger UI自动文档
@app.get("/docs")
async def show_docs():
    return "Redirect to /docs for API documentation"

@app.get("/redoc")
async def show_redoc():
    return "Redirect to /redoc for API documentation"