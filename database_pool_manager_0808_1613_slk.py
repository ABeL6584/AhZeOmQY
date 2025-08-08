# 代码生成时间: 2025-08-08 16:13:40
from typing import Optional
from fastapi import FastAPI, HTTPException, Depends
from pydantic import BaseModel, Field
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, Session
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.exc import SQLAlchemyError

# Pydantic Model
class DatabaseConfig(BaseModel):
    host: str = Field(default="localhost", description="Database host")
    port: int = Field(default=5432, description="Database port")
    username: str = Field(description="Database username")
    password: str = Field(description="Database password")
    database_name: str = Field(description="Database name")

# Database Session
engine = None
SessionLocal = sessionmaker(autocommit=False, autoflush=False)
Base = declarative_base()

def get_db(config: DatabaseConfig):
    global engine
    if engine is None:
        engine = create_engine(
            database_url=f"postgresql://{config.username}:{config.password}@{config.host}:"
            f"{config.port}/{config.database_name}"
        )
    try:
        conn = engine.connect()
        return conn
    except SQLAlchemyError as e:
        raise HTTPException(status_code=500, detail=str(e))

# FastAPI Application
app = FastAPI()

# Dependency
def get_session(db: Session = Depends(get_db)):
    try:
        yield db
    finally:
        db.close()

# API Endpoint for Database Connection Pool Management
@app.get("/pool")
async def read_pool_status(session: Session = Depends(get_session)):
    try:
        result = session.execute("SELECT * FROM pg_stat_activity;")
        return {"pool_status": result.fetchall()}
    except SQLAlchemyError as e:
        raise HTTPException(status_code=500, detail=str(e))
    
# Error Handling
@app.exception_handler(SQLAlchemyError)
async def sqlalchemy_exception_handler(request, exc):
    return JSONResponse(
        status_code=500,
        content={"detail": str(exc)}
    )

# Run Uvicorn Server
if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)