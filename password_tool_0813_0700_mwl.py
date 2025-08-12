# 代码生成时间: 2025-08-13 07:00:18
from fastapi import FastAPI, HTTPException, status
from pydantic import BaseModel, Field
from typing import Optional
from passlib.context import CryptContext
import base64
import os

# 设置密码哈希上下文
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
app = FastAPI()

# Pydantic 模型定义
class PasswordRequest(BaseModel):
    password: str = Field(..., description="The password to be hashed.")

class HashedPasswordResponse(BaseModel):
    hashed_password: str = Field(..., description="The hashed password.")

class PasswordVerificationResponse(BaseModel):
    password_is_correct: bool = Field(..., description="Whether the password is correct or not.")

# 使用bcrypt加密密码的端点
@app.post("/hash_password/")
async def hash_password(password_request: PasswordRequest):
    hashed_password = pwd_context.hash(password_request.password)
    return HashedPasswordResponse(hashed_password=hashed_password)

# 验证密码的端点
@app.post("/verify_password/")
async def verify_password(plain_password: str, hashed_password: str):
    try:
        is_correct = pwd_context.verify(plain_password, hashed_password)
        return PasswordVerificationResponse(password_is_correct=is_correct)
    except ValueError as e:  # 如果验证失败，捕获错误
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Password is incorrect.")

# 添加错误处理
@app.exception_handler(ValueError)
async def value_error_exception_handler(request, exc):
    return JSONResponse(
        status_code=status.HTTP_400_BAD_REQUEST,
        content={"message": str(exc)}
    )

# 添加文档和UI
@app.get("/docs")
async def get_documentation():
    return {
        "message": "Redirect to /docs for API documentation."
    }

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
