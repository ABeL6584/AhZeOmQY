# 代码生成时间: 2025-09-15 17:49:08
from fastapi import FastAPI, HTTPException, status
from fastapi.encoders import jsonable_encoder
from pydantic import BaseModel, Field
from typing import Optional
from cryptography.fernet import Fernet
import base64

class Password(BaseModel):
    password: str = Field(..., description="The plaintext password to encode")
    key: Optional[str] = Field(None, description="An optional encryption key, if not provided a new one will be generated")

app = FastAPI()

# Generate a key for encryption/decryption
def get_key():
    return Fernet.generate_key()

# Save the key to a variable or file for later use
key = get_key()

# Save the key in a base64 encoded string format to be shared
encoded_key = base64.b64encode(key).decode('utf-8')

@app.post("/encrypt/")
async def encrypt_password(password: Password):
    """
    Encrypt a plaintext password using Fernet symmetric encryption.
    Returns the encrypted password and the encryption key.
    """
    f = Fernet(key)
    encrypted_password = f.encrypt(password.password.encode()).decode()
    return jsonable_encoder({"encrypted_password": encrypted_password, "key": encoded_key})

@app.post("/decrypt/")
async def decrypt_password(password: Password):
    """
    Decrypt an encrypted password using Fernet symmetric encryption.
    Requires the original key used for encryption.
    """
    try:
        f = Fernet(base64.b64decode(password.key))
        decrypted_password = f.decrypt(password.password.encode()).decode()
        return jsonable_encoder({"decrypted_password": decrypted_password})
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))

@app.get("/")
async def read_root():
    return {"message": "Welcome to the Password Encryption/Decryption API"}

# Custom error handler for 400 errors
@app.exception_handler(HTTPException)
async def http_exception_handler(request, exc):
    return JSONResponse(
        status_code=exc.status_code,
        content={"detail": exc.detail},
    )