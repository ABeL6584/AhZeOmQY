# 代码生成时间: 2025-08-23 17:58:40
from fastapi import FastAPI, HTTPException, status, Depends
from pydantic import BaseModel
from typing import Optional
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from jose import JWTError, jwt
from passlib.context import CryptContext
from datetime import datetime, timedelta
from fastapi.security import HTTPBasicCredentials
from fastapi import APIRouter
from fastapi.responses import JSONResponse
from fastapi.encoders import jsonable_encoder

# 定义一个Pydantic模型用于用户登录数据
class UserLogin(BaseModel):
    username: str
    password: str

# 定义一个Pydantic模型用于用户信息
class UserInfo(BaseModel):
    username: str
    password: Optional[str] = None
    is_active: Optional[bool] = True

# 定义一个用于验证用户登录的依赖函数
def get_current_user(token: str = Depends(oauth2_scheme)):
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
    user = get_user(username=username)
    if user is None:
        raise credentials_exception
    return user

# 定义一个用于获取用户的函数
def get_user(username: str):
    # 这里应该有一个从数据库中获取用户的实现
    # 为了示例简单，这里使用一个固定的用户
    return UserInfo(username="admin", password="password123", is_active=True)

# 安全方案配置
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")
SECRET_KEY = "09d25e094faa6ca2556c818166b7a9563b93f7099f6f0f4caa6cf63b88e8d3e7",
ALGORITHM = "HS256"
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

# 创建FastAPI应用
app = FastAPI()

# 创建一个依赖函数，用于获取当前用户
def get_current_active_user(current_user: UserInfo = Depends(get_current_user)):
    if current_user.disabled:
        raise HTTPException(status_code=400, detail="Inactive user")
    return current_user

# 用户登录路由
@app.post("/token")
async def login(form_data: OAuth2PasswordRequestForm = Depends(), response: JSONResponse = Depends()):
    user = authenticate_user(form_data.username, form_data.password)
    if not user:
        raise HTTPException(status_code=400, detail="Incorrect username or password")
    token = create_access_token(data={"sub": user.username}, expires_delta=timedelta(minutes=30))
    response = response
    response.headers["Content-Type"] = "application/json"
    response.status_code = status.HTTP_200_OK
    return jsonable_encoder({
        "access_token": token,
        "token_type": "bearer",
    })

# 用户验证函数
def authenticate_user(username: str, password: str) -> UserInfo:
    user = get_user(username)
    if not user or not pwd_context.verify(password, user.password):
        return False
    return user

# 创建JWT令牌函数
def create_access_token(data: dict, expires_delta: Optional[timedelta] = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=15)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt