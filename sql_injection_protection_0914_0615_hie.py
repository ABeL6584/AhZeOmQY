# 代码生成时间: 2025-09-14 06:15:16
from fastapi import FastAPI, HTTPException, Depends, status
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from pydantic import BaseModel, EmailStr
from typing import Optional
from sqlalchemy import create_engine, select
from sqlalchemy.orm import sessionmaker
from sqlalchemy.exc import SQLAlchemyError
from passlib.context import CryptContext
from .database import Base, User
from .schemas import UserIn, UserInDB

app = FastAPI()

# 配置密码哈希库
pwd_context = CryptContext(schemes=["bcrypt"], deprecated=["auto"])

# 配置数据库连接
DATABASE_URL = "sqlite:///./test.db"
engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False})
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# 依赖项
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

# Pydantic模型
class UserIn(BaseModel):
    username: str
    password: str
    
class UserOut(BaseModel):
    username: str
    
# 错误处理
@app.exception_handler(SQLAlchemyError)
async def db_exception_handler(request, exc):
    return HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                        detail="Database error.")

@app.exception_handler(ValueError)
async def value_error_handler(request, exc):
    return HTTPException(status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
                        detail=str(exc))

# FastAPI端点
@app.post("/users/")
async def create_user(user: UserIn, db: SessionLocal = Depends(get_db)):
    # 防止SQL注入
    db_user = db.query(User).filter(User.username == user.username).first()
    if db_user:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                            detail="Username already exists.")
    db_user = User(username=user.username, hashed_password=pwd_context.hash(user.password))
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return UserOut(username=db_user.username)

# API文档
@app.get("/docs")
async def main():
    return {
        "detail": "API Documentation"
    }