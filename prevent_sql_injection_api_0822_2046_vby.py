# 代码生成时间: 2025-08-22 20:46:40
from fastapi import FastAPI, HTTPException, status
from fastapi.encoders import jsonable_encoder
from pydantic import BaseModel, conint
from fastapi.responses import JSONResponse
from sqlalchemy import create_engine, text
from sqlalchemy.orm import sessionmaker
from typing import Optional

# Define Pydantic model
class User(BaseModel):
    id: conint(ge=1)  # Integer ID greater than or equal to 1

    # Ensure id is always an integer
    class Config:
        schema_extra = {"example": {"id": 1}}

# Create FastAPI app
app = FastAPI()

# Database connection
DATABASE_URL = "sqlite:///./test.db"  # Replace with your actual database URL
engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False})
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Dependency to get database session
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# Define endpoint to prevent SQL injection
@app.get("/users/{user_id}")
async def read_user(user_id: int, db: SessionLocal = Depends(get_db)):
    # Use SQLAlchemy Core to prevent SQL injection
    stmt = text("SELECT * FROM users WHERE id = :user_id")
    user = db.execute(stmt, {"user_id": user_id}).fetchone()

    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")

    # Convert user to Pydantic model
    user_data = User(**user)
    return JSONResponse(content=jsonable_encoder(user_data))

# Error handler
@app.exception_handler(HTTPException)
async def http_exception_handler(request, exc):
    return JSONResponse(
        status_code=exc.status_code,
        content={"detail": exc.detail},
    )

# Start the API server
if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)