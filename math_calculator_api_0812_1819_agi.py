# 代码生成时间: 2025-08-12 18:19:52
from fastapi import FastAPI, HTTPException, status
from pydantic import BaseModel
from typing import List, Optional
from math import sqrt

app = FastAPI()

# Pydantic model for individual operation
class Operation(BaseModel):
    type: str
    numbers: List[float]

# Pydantic model for multiple operations
class Operations(BaseModel):
    operations: List[Operation]

# Helper function to perform operations
def perform_operation(op_type: str, numbers: List[float]) -> float:
    if op_type == "add":
        return sum(numbers)
    elif op_type == "subtract":
        return sum(numbers) - (sum(numbers[1:]) + numbers[0])
    elif op_type == "multiply":
        result = 1
        for num in numbers:
            result *= num
        return result
    elif op_type == "divide":
        total = sum(numbers)
        count = len(numbers)
        return total / count
    elif op_type == "square_root":
        return sqrt(numbers[0])
    else:
        raise ValueError("Unsupported operation")

# Endpoint for a single operation
@app.post("/calculate")
async def calculate(op: Operation):
    try:
        result = perform_operation(op.type, op.numbers)
        return {"result": result}
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))

# Endpoint for multiple operations
@app.post("/bulk_calculate")
async def bulk_calculate(operations: Operations):
    results = []
    for op in operations.operations:
        try:
            result = perform_operation(op.type, op.numbers)
            results.append({"operation": op.type, "result": result})
        except ValueError as e:
            results.append({"operation": op.type, "error": str(e)})
    return results
