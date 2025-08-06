# 代码生成时间: 2025-08-07 02:57:25
from typing import List
from fastapi import FastAPI, HTTPException, APIRouter
from pydantic import BaseModel, ValidationError
from starlette.responses import JSONResponse
import random

# Pydantic model for input data
class Numbers(BaseModel):
    numbers: List[int]

# FastAPI app instance
app = FastAPI(title="Sorting API")

# Sort numbers endpoint
@app.post("/sort/")
async def sort_numbers(numbers: Numbers):
    """
    Endpoint to sort a list of numbers.
    Args:
        numbers: Pydantic model, expects a list of integers.
    Returns:
        A JSON response with sorted numbers.
    Raises:
        HTTPException: If input validation fails.
    """
    try:
        # Validate input
        numbers_dict = numbers.dict()
        # Sort the list of numbers
        sorted_numbers = sorted(numbers_dict['numbers'])
        # Return the sorted list
        return JSONResponse(content={"sorted_numbers": sorted_numbers}, media_type="application/json")
    except ValidationError as e:
        # If input validation fails, raise an HTTPException with a 422 error
        raise HTTPException(status_code=422, detail=str(e))

# Error handling
@app.exception_handler(ValidationError)
async def validation_exception_handler(request, exc: ValidationError):
    return JSONResponse(
        status_code=422,
        content={"detail": exc.errors()[0]['msg'], "type": exc.errors()[0]['type']},
        media_type="application/json"
    )

# Test endpoint to generate a random list of numbers
@app.get("/test/")
async def test_sort():
    """
    Endpoint to test the sorting algorithm, generates a random list of numbers.
    """
    numbers = [random.randint(0, 100) for _ in range(10)]
    return JSONResponse(content={"numbers": numbers}, media_type="application/json")
