# 代码生成时间: 2025-08-27 23:25:06
from fastapi import FastAPI, HTTPException, status
from pydantic import BaseModel, Field
from typing import Optional
from cryptography.fernet import Fernet
import os

# Pydantic模型用于输入密码
class PasswordData(BaseModel):
    password: str = Field(..., description="The password to encrypt or decrypt.")
    operation: str = Field(..., description="Operation to perform: 'encrypt' or 'decrypt'.")

# 生成一个密钥并保存（在实际部署中，这个密钥应该安全地存储）
key = Fernet.generate_key()
cipher_suite = Fernet(key)

# FastAPI应用
app = FastAPI()

# 密码加密解密端点
@app.post("/password/")
async def password_encryption_decryption(password_data: PasswordData):
    """
    Handle password encryption and decryption.

    Args:
        password_data (PasswordData): Pydantic model containing password and operation.

    Returns:
        A dictionary with the result of the operation.
    """
    try:
        if password_data.operation.lower() == 'encrypt':
            # 加密密码
            encrypted_password = cipher_suite.encrypt(password_data.password.encode())
            return {"result": encrypted_password.decode()}
        elif password_data.operation.lower() == 'decrypt':
            # 解密密码
            decrypted_password = cipher_suite.decrypt(password_data.password.encode())
            return {"result": decrypted_password.decode()}
        else:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Invalid operation. Use 'encrypt' or 'decrypt'.")
    except Exception as e:
        # 错误处理
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))

# 启动应用
if __name__ == '__main__':
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=8000)
