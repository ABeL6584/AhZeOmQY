# 代码生成时间: 2025-08-30 10:14:30
from fastapi import FastAPI, HTTPException, status
from pydantic import BaseModel
from passlib.context import CryptContext
from passlib.hash import bcrypt
from typing import Optional

# 创建FastAPI应用实例
app = FastAPI()

# 创建密码哈希上下文
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

# Pydantic模型定义
class PasswordData(BaseModel):
    password: str

class EncryptedPassword(PasswordData):
    encrypted_password: str

# 加密密码的端点
@app.post("/encrypt/")
async def encrypt_password(password_data: PasswordData):
    # 加密密码
    hashed_password = pwd_context.hash(password_data.password)
    # 返回加密后的密码
    return EncryptedPassword(
        password=password_data.password,
        encrypted_password=hashed_password
    )

# 解密密码的端点
@app.post("/decrypt/")
async def decrypt_password(password_data: PasswordData):
    # 检查密码是否正确
    if not pwd_context.verify(password_data.password, password_data.password):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Incorrect password")
    # 如果密码正确，返回加密后的密码
    return EncryptedPassword(
        password=password_data.password,
        encrypted_password=password_data.password  # 注意：这里返回的是原始密码，因为实际解密操作不适用bcrypt
    )

# 添加错误处理
@app.exception_handler(HTTPException)
async def http_exception_handler(request, exc):
    return JSONResponse(
        status_code=exc.status_code,
        content={"detail": exc.detail}
    )

# 添加API文档
@app.get("/docs")
async def get_documentation():
    return {
        "message": "API Documentation is available at /docs and /redoc"
    }
