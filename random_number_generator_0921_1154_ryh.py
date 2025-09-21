# 代码生成时间: 2025-09-21 11:54:05
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field
from random import randint
from typing import Optional


class RandomNumberRange(BaseModel):
    start: int = Field(..., ge=0, description="The start of the range (inclusive)")
    end: int = Field(..., gt="start", description="The end of the range (inclusive)")

app = FastAPI()

@app.get("/random-number")
async def generate_random_number(range_model: RandomNumberRange):
    """Generate a random number within the specified range."""
    if range_model.end <= range_model.start:
        raise HTTPException(status_code=400, detail="End of range must be greater than start.")
    return {
        "random_number": randint(range_model.start, range_model.end)
    }

@app.exception_handler(ValueError)
async def value_error_handler(request, exc):
    return JSONResponse(
        status_code=400,
        content={"detail": str(exc)}
    )

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)