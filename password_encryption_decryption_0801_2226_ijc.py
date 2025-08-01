# 代码生成时间: 2025-08-01 22:26:36
from fastapi import FastAPI, HTTPException, status
from pydantic import BaseModel, Field
from typing import Optional
from passlib.context import CryptContext
from passlib.hash import bcrypt

# 创建FastAPI应用
app = FastAPI()

# 定义Pydantic模型
class PasswordModel(BaseModel):
    password: str = Field(..., description="Password to be encrypted or decrypted")
    operation: str = Field(..., description="Operation to perform: 'encrypt' or 'decrypt'")

# 创建密码上下文
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

# 密码加密端点
@app.post("/encrypt/")
async def encrypt_password(model: PasswordModel):
    if model.operation != "encrypt":
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Invalid operation. Only 'encrypt' is allowed for this endpoint.")
    hashed_password = pwd_context.hash(model.password)
    return {"message": "Password encrypted successfully.", "hashed_password": hashed_password}

# 密码解密端点
@app.post("/decrypt/")
async def decrypt_password(model: PasswordModel):
    if model.operation != "decrypt":
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Invalid operation. Only 'decrypt' is allowed for this endpoint.")
    if not pwd_context.verify(model.password, model.hashed_password):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Incorrect password or hashed password.")
    return {"message": "Password decrypted successfully."}

# 添加错误处理
@app.exception_handler(HTTPException)
async def http_exception_handler(request, exc):
    return JSONResponse(
        status_code=exc.status_code,
        content={"detail": exc.detail}
    )

# 添加文档支持
@app.get("/docs")
async def read_docs():
    return {"message": "API documentation available at /docs"}
