# 代码生成时间: 2025-08-26 15:09:17
from fastapi import FastAPI, HTTPException, status
from pydantic import BaseModel
from typing import Dict, Any
from fastapi.responses import JSONResponse
def error_handler_422(request: Request, exc: HTTPException):
    """
    HTTP 422 Unprocessable Entity error handler.
    """
    return JSONResponse(
        status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
        content={
            "detail": exc.detail,
        },
    )

class FormatResponse(BaseModel):
    """
    Schema for the API's response payload.
    """
    data: Dict[str, Any]
    error: str = None
    success: bool = True

app = FastAPI()

@app.exception_handler(HTTPException)
async def http_exception_handler(request: Request, exc: HTTPException):
    """
    Custom error handler for HTTP exceptions.
    """
    return JSONResponse(
        status_code=exc.status_code,
        content={
            "detail": exc.detail,
        },
    )

@app.post("/format-response")
async def format_response(payload: FormatResponse):
    """
    Endpoint to format API responses.
    """
    return JSONResponse(
        content=payload.dict(),
        status_code=status.HTTP_200_OK,
        media_type="application/json"
    )

# Uncomment below to run the API
# if __name__ == "__main__":
#     import uvicorn
#     uvicorn.run(app, host="0.0.0.0", port=8000)