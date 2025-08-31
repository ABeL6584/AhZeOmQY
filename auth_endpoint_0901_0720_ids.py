# 代码生成时间: 2025-09-01 07:20:40
from fastapi import FastAPI, Depends, HTTPException, status, Security
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from pydantic import BaseModel
from typing import Optional
from passlib.context import CryptContext
from jose import JWTError, jwt
from datetime import datetime, timedelta
from time import time

# 初始化FastAPI应用
app = FastAPI()

# 用于密码哈希的上下文
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

# 用于生成JWT的密钥
SECRET_KEY = "a_secret_key"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

# 用户模型
class User(BaseModel):
    username: str
    disabled: Optional[bool] = None

# 用户数据库模拟
fake_users_db = {
    "john": {
        "username": "john",
        "hashed_password": pwd_context.hash("john123"),
        "disabled": False,
    }
}

# JWT令牌模型
class Token(BaseModel):
    access_token: str
    token_type: str

# Token数据模型
class TokenData(BaseModel):
    username: Optional[str] = None

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

# 用户身份验证函数
async def authenticate_user(username: str, password: str):
    user = fake_users_db.get(username)
    if not user:
        return False
    if not pwd_context.verify(password, user['hashed_password']):
        return False
    if user.get('disabled'):
        return False
    return user

# 获取当前用户函数
async def get_current_user(token: str = Depends(oauth2_scheme)):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username: str = payload.get("sub")
        if username is None:
            raise credentials_exception
    except JWTError:
        raise credentials_exception
    user = fake_users_db.get(username)
    if user is None:
        raise credentials_exception
    return user

# 用户身份验证端点
@app.post("/token")
async def login(form_data: OAuth2PasswordRequestForm = Depends(), current_user: User = Security(get_current_user)):
    user = await authenticate_user(form_data.username, form_data.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    expires = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = jwt.encode(
        {
            "sub": user['username'],
            "exp": expires,
        }, SECRET_KEY, algorithm=ALGORITHM
    )
    return {"access_token": access_token, "token_type": "bearer"}

# 用户身份验证保护端点
@app.get("/users/me/\)
async def read_users_me(current_user: User = Security(get_current_user)):
    return current_user