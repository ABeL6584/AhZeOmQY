# 代码生成时间: 2025-10-09 02:53:20
from fastapi import FastAPI, HTTPException, status
from pydantic import BaseModel, ValidationError
from typing import Optional
from fastapi.responses import JSONResponse
import json

app = FastAPI()

# Pydantic model for color selection
class Color(BaseModel):
    r: int = 0  # Red component (0-255)
    g: int = 0  # Green component (0-255)
    b: int = 0  # Blue component (0-255)
    a: Optional[int] = None  # Alpha component (0-255), optional

    # Validate color components
    @property
    def is_valid(self) -> bool:
        return 0 <= self.r <= 255 and 0 <= self.g <= 255 and 0 <= self.b <= 255 and (self.a is None or 0 <= self.a <= 255)

# Endpoint for color selection
@app.post("/color")
async def select_color(color: Color):
    if not color.is_valid:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Invalid color components")
    return JSONResponse(content={"color": {"r": color.r, "g": color.g, "b": color.b, "a": color.a}}, media_type="application/json")

# Error handler for Pydantic validation errors
@app.exception_handler(ValidationError)
async def validation_exception_handler(request, exc: ValidationError):
    detail = json.loads(exc.body)
    return JSONResponse(status_code=status.HTTP_422_UNPROCESSABLE_ENTITY, content={"detail": detail})

# Error handler for general exceptions
@app.exception_handler(Exception)
async def exception_handler(request, exc):
    return JSONResponse(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, content={"message": str(exc)})
